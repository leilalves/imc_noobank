"""
===============================================================================
VIEW — camada de INTERFACE (padrão MVC)
===============================================================================
Este é o ÚNICO arquivo de View do projeto. Cada tela do app é uma CLASSE
que sabe montar (`build`) o seu próprio `ft.View`. As Views:

    • SÓ desenham a tela (nenhuma regra de negócio mora aqui);
    • leem dados do Model através do `controller.model` (ex.: saldo,
      lista de transações);
    • quando o usuário clica em algo, chamam um método do CONTROLLER
      (ex.: `controller.unlock(...)`), nunca mexem no Model diretamente.
      
"""
from abc import ABC, abstractmethod
import flet as ft

# Cores principais do app (roxo, característico desse tipo de banco digital).
PURPLE = "#8A05BE"

# ------------------------------------------------------------------------
# Classe ABSTRATA: contrato comum + comportamento compartilhado (herança)
# ------------------------------------------------------------------------
class ScreenView(ABC):
    """Toda tela do Noobank é uma subclasse de ScreenView."""

    @abstractmethod
    def build(self, controller) -> ft.View:
        """Monta e devolve o `ft.View` desta tela. Cada tela implementa o seu."""
        raise NotImplementedError

    # ----- métodos utilitários HERDADOS por todas as telas -----------
    def detail_line(self, label, value) -> ft.Row:
        """Uma linha 'rótulo à esquerda / valor à direita' (usada no diálogo)."""
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(label, color=ft.Colors.OUTLINE, size=12),
                ft.Text(str(value), size=12),
            ],
        )

    def show_transaction_details(self, controller, tx) -> None:
        """Abre um AlertDialog com os detalhes completos de UMA transação."""
        color = ft.Colors.GREEN_700 if tx.is_income else ft.Colors.RED_700
        sign = "+" if tx.is_income else "-"

        def close(e):
            controller.page.pop_dialog()

        dialog = ft.AlertDialog(
            modal=True,  # só fecha pelo botão "Fechar", não clicando fora
            title=ft.Row(controls=[ft.Text(tx.emoji, size=24), ft.Text("Detalhes")]),
            content=ft.Column(
                tight=True,
                spacing=10,
                controls=[
                    ft.Text(tx.description, weight=ft.FontWeight.BOLD, size=16),
                    self.detail_line("Categoria", tx.category),
                    self.detail_line("Data", tx.date),
                    self.detail_line("Identificador", tx.id),
                    ft.Divider(),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text("Valor", weight=ft.FontWeight.BOLD),
                            ft.Text(
                                f"{sign} R$ {abs(tx.amount):.2f}",
                                color=color,
                                weight=ft.FontWeight.BOLD,
                                size=16,
                            ),
                        ],
                    ),
                ],
            ),
            actions=[ft.TextButton("Fechar", on_click=close)],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        controller.page.show_dialog(dialog)

    def transaction_row(self, controller, tx, hide_value: bool = False) -> ft.Container:
        """
        Renderiza UMA linha de transação (emoji + descrição/categoria +
        valor colorido + seta). Clicável: abre o diálogo de detalhes.
        Compartilhado entre a tela Início e a tela de Extrato (herança).

        `hide_value`: quando True, mostra "••••" no lugar do valor — usado
        pela tela Início para esconder os valores junto com o saldo.
        """
        color = ft.Colors.GREEN_700 if tx.is_income else ft.Colors.RED_700
        sign = "+" if tx.is_income else "-"
        valor_texto = "••••" if hide_value else f"{sign} R$ {abs(tx.amount):.2f}"
        return ft.Container(
            padding=ft.Padding(0, 8, 0, 8),
            # t=tx "trava" o valor de tx no momento da criação do lambda,
            # evitando o bug clássico de closures em loops.
            on_click=lambda e, t=tx: self.show_transaction_details(controller, t),
            content=ft.Row(
                spacing=12,
                controls=[
                    ft.Text(tx.emoji, size=22),
                    ft.Column(
                        expand=True,
                        spacing=0,
                        controls=[
                            ft.Text(tx.description, weight=ft.FontWeight.W_600, size=13),
                            ft.Text(f"{tx.category} • {tx.date}", size=11, color=ft.Colors.OUTLINE),
                        ],
                    ),
                    ft.Text(
                        valor_texto,
                        color=color,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, size=16, color=ft.Colors.OUTLINE),
                ],
            ),
        )


# ------------------------------------------------------------------------
# Tela: Bloqueio biométrico (primeira tela do app)
# ------------------------------------------------------------------------
class LockView(ScreenView):
    """Tela de bloqueio (rota "/"), sempre a primeira a aparecer."""

    def build(self, controller) -> ft.View:
        # Texto de status/feedback exibido durante e após a tentativa de login.
        status = ft.Text()

        async def unlock(e: ft.Event[ft.Button]):
            """Executado ao tocar no ícone de digital ou no botão 'Desbloquear'."""
            await controller.unlock(status)

        return ft.View(
            route="/",
            bgcolor=PURPLE,
            padding=0,
            controls=[
                ft.SafeArea(
                    expand=True,
                    content=ft.Container(
                        expand=True,
                        bgcolor=PURPLE,
                        alignment=ft.Alignment.CENTER,
                        padding=24,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=18,
                            controls=[
                                ft.Text("💜", size=56),  # "logo" fictício (emoji)
                                ft.Text(
                                    "Noobank",
                                    size=30,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE,
                                ),
                                ft.Text(
                                    "Desbloqueie com biometria para continuar",
                                    # Flet 1.0: constantes de cor com número agora usam "_"
                                    # antes do número (ex.: WHITE70 -> WHITE_70,
                                    # BLACK54 -> BLACK_54). Antes dava AttributeError.
                                    color=ft.Colors.WHITE_70,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.Container(height=20),
                                ft.IconButton(
                                    ft.Icons.FINGERPRINT,
                                    icon_size=64,
                                    icon_color=ft.Colors.WHITE,
                                    on_click=unlock,
                                ),
                                ft.Button(
                                    "Desbloquear",
                                    icon=ft.Icons.LOCK_OPEN,
                                    bgcolor=ft.Colors.WHITE,
                                    color=PURPLE,
                                    on_click=unlock,
                                ),
                                status,
                            ],
                        ),
                    ),
                )
            ],
        )


# ------------------------------------------------------------------------
# Tela: Início — saldo, atalhos e extrato recente
# ------------------------------------------------------------------------
class HomeView(ScreenView):
    """Tela Início (rota "/home")."""

    def build(self, controller) -> ft.View:
        model = controller.model

        balance_text = ft.Text(
            model.formatted_balance(),
            size=30,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        )

        def toggle_balance(e):
            """
            Mostra/esconde o saldo ao tocar no ícone de olho — e, junto com
            ele, os valores das transações listadas abaixo em "Últimas
            movimentações" (redesenhados com `hide_value=model.balance_hidden`).
            """
            controller.toggle_balance_visibility()
            balance_text.value = model.formatted_balance()
            eye_btn.icon = ft.Icons.VISIBILITY_OFF if model.balance_hidden else ft.Icons.VISIBILITY
            recent.controls = [
                self.transaction_row(controller, t, hide_value=model.balance_hidden)
                for t in model.recent_transactions(4)
            ]
            controller.page.update()

        eye_btn = ft.IconButton(ft.Icons.VISIBILITY, icon_color=ft.Colors.WHITE, on_click=toggle_balance)

        balance_card = ft.Container(
            padding=20,
            border_radius=18,
            bgcolor=PURPLE,
            content=ft.Column(
                spacing=6,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[ft.Text("Saldo em conta", color=ft.Colors.WHITE_70), eye_btn],
                    ),
                    balance_text,
                    ft.Text(model.account_number, color=ft.Colors.WHITE_70, size=12),
                ],
            ),
        )

        def quick_action(icon, label, route):
            """Botão de atalho (ex.: Pix, Extrato) que navega para 'route'."""
            return ft.Container(
                expand=True,
                padding=12,
                border_radius=14,
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                on_click=lambda e: controller.navigate(route),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=6,
                    controls=[ft.Icon(icon, color=PURPLE), ft.Text(label, size=12)],
                ),
            )

        actions_row = ft.Row(
            spacing=10,
            controls=[
                quick_action(ft.Icons.SWAP_HORIZ, "Pix", "/pix"),
                quick_action(ft.Icons.RECEIPT_LONG, "Extrato", "/statement"),
            ],
        )

        # Só as 4 transações mais recentes (o extrato completo fica em /statement).
        recent = ft.Column(
            controls=[self.transaction_row(controller, t) for t in model.recent_transactions(4)]
        )

        appbar = ft.AppBar(
            title=ft.Text(f"Olá, {model.owner_name} 👋"),
            bgcolor=ft.Colors.SURFACE,
            actions=[
                ft.IconButton(
                    ft.Icons.SETTINGS_OUTLINED,
                    on_click=lambda e: controller.page.show_dialog(
                        ft.SnackBar(ft.Text("Configurações — fora do escopo deste exercício."))
                    ),
                )
            ],
        )

        body = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(padding=16, content=balance_card),
                ft.Container(padding=ft.Padding(16, 0, 16, 0), content=actions_row),
                ft.Container(
                    padding=16,
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text("Últimas movimentações", weight=ft.FontWeight.BOLD),
                                    ft.TextButton(
                                        "Ver tudo",
                                        on_click=lambda e: controller.navigate("/statement"),
                                    ),
                                ],
                            ),
                            recent,
                        ]
                    ),
                ),
            ],
        )

        return ft.View(
            route="/home",
            controls=[ft.SafeArea(expand=True, content=ft.Column(expand=True, controls=[appbar, body]))],
        )


# ------------------------------------------------------------------------
# Tela: Pix — escolher contato + valor (mini-wizard de 3 passos)
# ------------------------------------------------------------------------
class PixView(ScreenView):
    """
    Tela de Pix (rota "/pix"), com 3 passos dentro da MESMA View:
        1. "contacts" -> escolher para quem enviar
        2. "amount"   -> digitar o valor e confirmar
        3. "success"  -> tela de confirmação

    O passo atual e o contato escolhido ficam guardados em atributos da
    própria instância (`self.step`, `self.contact`) — ENCAPSULAMENTO do
    estado do wizard dentro do objeto da tela.
    """

    def __init__(self):
        self.step = "contacts"
        self.contact = None
        self.content_column = ft.Column()

    def build(self, controller) -> ft.View:
        self.render(controller)  # desenha o passo inicial assim que a tela abre

        appbar = ft.AppBar(
            title=ft.Text("Pix"),
            # Sem navegação automática "voltar", cada tela interna precisa
            # do seu próprio botão explícito.
            leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: controller.navigate("/home")),
        )
        body = ft.Container(
            padding=16,
            expand=True,
            content=ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
                controls=[self.content_column],
            ),
        )
        return ft.View(
            route="/pix",
            controls=[ft.SafeArea(expand=True, content=ft.Column(expand=True, controls=[appbar, body]))],
        )

    def render(self, controller) -> None:
        """Redesenha `content_column` de acordo com o passo atual."""
        if self.step == "contacts":
            self.content_column.controls = self.render_contacts(controller)
        elif self.step == "amount":
            self.content_column.controls = self.render_amount(controller)
        else:
            self.content_column.controls = self.render_success(controller)
        if controller.page:
            controller.page.update()

    def render_contacts(self, controller):
        """Passo 1: lista de contatos fictícios para escolher o destinatário."""

        def pick(c):
            self.contact = c
            self.step = "amount"
            self.render(controller)

        cards = [
            ft.Container(
                padding=12,
                border_radius=12,
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                on_click=lambda e, c=contact: pick(c),
                content=ft.Row(
                    spacing=12,
                    controls=[
                        ft.CircleAvatar(
                            content=ft.Text(contact.initial, color=ft.Colors.WHITE),
                            bgcolor=contact.color,
                        ),
                        ft.Column(
                            spacing=0,
                            controls=[
                                ft.Text(contact.name, weight=ft.FontWeight.W_600),
                                ft.Text(f"{contact.key_type}: {contact.key_masked}", size=12),
                            ],
                        ),
                    ],
                ),
            )
            for contact in controller.model.contacts
        ]
        return [ft.Text("Para quem você quer transferir?", weight=ft.FontWeight.BOLD), *cards]

    def render_amount(self, controller):
        """Passo 2: campo de valor + confirmação da transferência."""
        amount_field = ft.TextField(
            label="Valor (R$)",
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix=ft.Text("R$ "),
            autofocus=True,
        )

        def back(e):
            """Volta ao passo 1 (escolher outro contato)."""
            self.step = "contacts"
            self.render(controller)

        def confirm(e):
            """
            Pede ao Controller para efetivar o Pix. Passamos o próprio
            `amount_field` (não só o texto) para que o Controller possa
            escrever a mensagem de erro de validação diretamente no campo,
            caso o valor digitado seja inválido.
            """
            controller.confirm_pix(self, amount_field)

        return [
            ft.Row(
                controls=[
                    ft.IconButton(ft.Icons.ARROW_BACK, on_click=back),
                    ft.Text("Quanto você quer enviar?", weight=ft.FontWeight.BOLD),
                ]
            ),
            ft.Row(
                spacing=12,
                controls=[
                    ft.CircleAvatar(
                        content=ft.Text(self.contact.initial, color=ft.Colors.WHITE),
                        bgcolor=self.contact.color,
                    ),
                    ft.Text(self.contact.name, weight=ft.FontWeight.W_600),
                ],
            ),
            amount_field,
            ft.Button(
                "Transferir",
                icon=ft.Icons.SEND,
                width=400,
                bgcolor=PURPLE,
                color=ft.Colors.WHITE,
                on_click=confirm,
            ),
        ]

    def render_success(self, controller):
        """Passo 3: confirmação visual de que o Pix foi 'enviado'."""

        def back_home(e):
            controller.navigate("/home")

        return [
            ft.Container(height=20),
            ft.Icon(ft.Icons.CHECK_CIRCLE, size=72, color=ft.Colors.GREEN),
            ft.Text("Transferência enviada!", size=18, weight=ft.FontWeight.BOLD),
            ft.Text(f"para {self.contact.name}", text_align=ft.TextAlign.CENTER),
            ft.Container(height=10),
            ft.Button("Voltar para o início", width=400, on_click=back_home),
        ]

    # Chamado pelo Controller depois que a transferência é efetivada com sucesso.
    def go_to_success(self, controller) -> None:
        self.step = "success"
        self.render(controller)


# ------------------------------------------------------------------------
# Tela: Extrato completo com busca e filtro
# ------------------------------------------------------------------------
class StatementView(ScreenView):
    """Tela de Extrato (rota "/statement"): busca + filtro + lista completa."""

    def __init__(self):
        self.filter_value = "Todas"
        self.search_text = ""
        self.list_column = ft.Column()
        self.chips_row = ft.Row()

    def build(self, controller) -> ft.View:
        self.render_chips(controller)
        self.render_list(controller)

        appbar = ft.AppBar(
            title=ft.Text("Extrato completo"),
            leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: controller.navigate("/home")),
        )
        body = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    padding=16,
                    content=ft.Column(
                        spacing=12,
                        controls=[
                            ft.TextField(
                                hint_text="Buscar movimentação...",
                                prefix_icon=ft.Icons.SEARCH,
                                on_change=lambda e: self.on_search(controller, e.control.value),
                            ),
                            self.chips_row,
                            self.list_column,
                        ],
                    ),
                )
            ],
        )
        return ft.View(
            route="/statement",
            controls=[ft.SafeArea(expand=True, content=ft.Column(expand=True, controls=[appbar, body]))],
        )

    def render_list(self, controller) -> None:
        """Refaz a lista de transações visíveis conforme o filtro/busca atual."""
        found = controller.model.search_transactions(self.search_text, self.filter_value)
        rows = [self.transaction_row(controller, t) for t in found]
        self.list_column.controls = rows or [ft.Text("Nenhuma movimentação encontrada.", italic=True)]
        if controller.page:
            controller.page.update()

    def render_chips(self, controller) -> None:
        """Redesenha os botões de filtro, destacando o que está selecionado."""

        def select(e, f):
            self.filter_value = f
            self.render_chips(controller)
            self.render_list(controller)

        self.chips_row.controls = [
            (ft.Button if f == self.filter_value else ft.OutlinedButton)(
                f, on_click=lambda e, ff=f: select(e, ff)
            )
            for f in ("Todas", "Entradas", "Saídas")
        ]
        if controller.page:
            controller.page.update()

    def on_search(self, controller, text: str) -> None:
        """Atualiza o texto buscado a cada tecla digitada no campo de busca."""
        self.search_text = text
        self.render_list(controller)
