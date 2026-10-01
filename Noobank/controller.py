"""
===============================================================================
CONTROLLER — camada que ORQUESTRA o Model e a View (padrão MVC)
===============================================================================
Este é o ÚNICO arquivo de Controller do projeto: a classe `NoobankController`.

O Controller é o "meio de campo" do MVC:
    • recebe as ações do usuário que vêm da View (clique em um botão,
      texto digitado, navegação entre telas);
    • decide o que fazer: chama métodos do MODEL para ler/alterar dados
      (ex.: `model.transfer(...)`);
    • manda a VIEW se redesenhar com o resultado.

Repare que o Controller NUNCA desenha widgets do Flet diretamente (quem
faz isso é a View) e NUNCA guarda regra de negócio (quem faz isso é o
Model). Ele só "liga os fios".

"""
import asyncio
import flet as ft

from view import HomeView, LockView, PixView, StatementView

class NoobankController:

    def __init__(self, model):
        self.model = model
        self.page: ft.Page | None = None

    def run(self, page: ft.Page) -> None:
        self.page = page
        page.title = "Noobank — exercício de clone de app bancário"
        page.theme_mode = ft.ThemeMode.LIGHT

        page.window.width = 320
        page.window.height = 600

        page.on_route_change = self.route_change
        page.on_view_pop = self.view_pop
        self.route_change()

    def route_change(self, e=None) -> None:
        page = self.page
        page.views.clear()

        if page.route == "/home":
            page.views.append(HomeView().build(self) if self.model.unlocked else LockView().build(self))
        elif page.route == "/pix":
            page.views.append(PixView().build(self) if self.model.unlocked else LockView().build(self))
        elif page.route == "/statement":
            page.views.append(
                StatementView().build(self) if self.model.unlocked else LockView().build(self)
            )
        else:
            page.views.append(LockView().build(self))

        page.update()

    async def view_pop(self, e: ft.ViewPopEvent) -> None:
        if e.view is not None and len(self.page.views) > 1:
            self.page.views.remove(e.view)
            await self.page.push_route(self.page.views[-1].route)

    def navigate(self, route: str) -> None:
        self.page.navigate(route)

    async def device_authenticate(self, reason: str) -> tuple[bool, str]:
        await asyncio.sleep(1.0)
        return True, "⚠️ Simulado"

    async def unlock(self, status_control: ft.Text) -> None:
        status_control.value = "🔎 Verificando digital..."
        self.page.update()

        ok, message = await self.device_authenticate("Desbloqueie o Noobank para continuar")
        status_control.value = message
        self.page.update()

        if ok:
            await asyncio.sleep(0.5)
            self.model.unlocked = True
            await self.page.push_route("/home")

    def toggle_balance_visibility(self) -> None:
        self.model.toggle_balance_visibility()

    def confirm_pix(self, pix_view: PixView, amount_field: ft.TextField) -> bool:
        texto = (amount_field.value or "0").replace(",", ".")
        try:
            valor = float(texto)
        except ValueError:
            amount_field.error_text = "Digite um valor válido"
            self.page.update()
            return False

        try:
            self.model.transfer(pix_view.contact.name, valor)
        except ValueError as erro:
            amount_field.error_text = str(erro)
            self.page.update()
            return False

        pix_view.go_to_success(self)
        return True