import flet as ft
import os

def main(page: ft.Page):
    # ---------- Configurações gerais da página ----------
    page.title = "Calculadora de IMC"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO

    # Define um tema (claro e escuro) a partir de uma cor semente.
    # Com isso, Text/TextField/AppBar herdam automaticamente a cor
    # correta de texto ao trocar de tema, sem precisar setar cor
    # manualmente em cada widget (o código antigo fazia isso na "unha").
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.DEEP_PURPLE)
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.DEEP_PURPLE)

    # ---------- Funções ----------
    def calculate_imc(e):
        """Lê peso e altura, calcula o IMC e mostra a categoria."""
        try:
            weight = float(weight_input.value)
            height = float(height_input.value)
            if height > 0 and weight > 0:
                imc = weight / (height * height)
                category = (
                    "Abaixo do peso" if imc < 18.5 else
                    "Peso normal"    if imc < 24.9 else
                    "Sobrepeso"      if imc < 29.9 else
                    "Obesidade"
                )
                result_text.value = f"IMC: {imc:.2f}\nCategoria: {category}"
            else:
                result_text.value = "Por favor, insira valores válidos."
        except ValueError:
            result_text.value = "Por favor, insira valores válidos."
        # page.update() aqui é opcional em 1.0 (a tela já é atualizada
        # automaticamente ao final do handler), mas mantê-lo é inofensivo:
        # o Flet só evita mandar a atualização duplicada.
        page.update()

    def clear_fields(e):
        """Limpa os campos de entrada e o resultado exibido."""
        weight_input.value = ""
        height_input.value = ""
        result_text.value = ""
        page.update()

    def toggle_theme(e):
        """Alterna entre os temas claro e escuro."""
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        # Troca o ícone conforme o tema atual, sem precisar recolorir
        # manualmente nenhum outro widget da tela.
        theme_icon.icon = (
            ft.Icons.LIGHT_MODE
            if page.theme_mode == ft.ThemeMode.DARK
            else ft.Icons.DARK_MODE
        )
        page.update()

    # ---------- Componentes da UI ----------
    theme_icon = ft.IconButton(
        icon=ft.Icons.DARK_MODE,
        tooltip="Alternar tema",
        on_click=toggle_theme,
    )

    app_bar_title = ft.Text("Calculadora de IMC", size=22, weight=ft.FontWeight.W_500)
    title_text = ft.Text(
        "Informe seus dados",
        size=20,
        weight=ft.FontWeight.W_500,
        text_align=ft.TextAlign.CENTER,
    )

    weight_input = ft.TextField(
        label="Peso (kg)",
        prefix_icon=ft.Icons.FITNESS_CENTER,
        keyboard_type=ft.KeyboardType.NUMBER,
        width=300,
        # ft.InputBorder.UNDERLINE está depreciado desde 1.0.0 (será
        # removido na 1.3.0) — usamos a classe dedicada no lugar.
        border=ft.UnderlineInputBorder(),
        # Cor semântica do tema (Material 3): já vem branca no escuro
        # e escura no claro, sem precisar recolorir manualmente.
        border_color=ft.Colors.OUTLINE,
    )

    height_input = ft.TextField(
        label="Altura (m)",
        prefix_icon=ft.Icons.HEIGHT,
        keyboard_type=ft.KeyboardType.NUMBER,
        width=300,
        border=ft.UnderlineInputBorder(),
        border_color=ft.Colors.OUTLINE,
    )

    result_text = ft.Text("", size=18, weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER)

    # Imagem opcional: fica dentro de assets/. O "src" do ft.Image é
    # resolvido pelo próprio Flet relativo à pasta de assets, mas o
    # os.path.exists roda em Python puro e precisa do caminho real
    # no disco — por isso montamos o caminho a partir de __file__,
    # em vez do nome do arquivo sozinho (que checaria o diretório
    # de onde o app foi executado, não a pasta assets/).
    image_name = "Senai.png"
    image_full_path = os.path.join(os.path.dirname(__file__), "assets", image_name)
    image_control = (
        ft.Image(src=image_name, height=50, fit=ft.BoxFit.CONTAIN)
        if os.path.exists(image_full_path)
        else ft.Text(f"Imagem {image_name} não encontrada", italic=True, size=12)
    )

    # Botões de ação, com cantos arredondados.
    # ft.ElevatedButton foi REMOVIDO em 1.0.0 -> use ft.Button.
    # O texto continua podendo ser passado como 1º argumento posicional
    # (que agora corresponde ao parâmetro content, não mais text).
    calc_button = ft.Button(
        "Calcular IMC",
        bgcolor=ft.Colors.DEEP_PURPLE,
        color=ft.Colors.WHITE,
        width=140,
        height=50,
        on_click=calculate_imc,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25)),
    )

    clear_button = ft.Button(
        "Limpar",
        bgcolor=ft.Colors.RED_ACCENT,
        color=ft.Colors.WHITE,
        width=140,
        height=50,
        on_click=clear_fields,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25)),
    )

    # ---------- Layout principal ----------
    # AppBar fixa no topo + conteúdo em uma Column centralizada.
    page.add(
        ft.AppBar(
            title=app_bar_title,
            center_title=True,
            bgcolor=ft.Colors.TRANSPARENT,
            actions=[theme_icon],
        ),
        ft.Container(
            content=ft.Column(
                controls=[
                    title_text,
                    ft.Container(height=10),
                    weight_input,
                    ft.Container(height=10),
                    height_input,
                    ft.Container(height=10),
                    result_text,
                    ft.Container(height=10),
                    ft.Row(
                        controls=[calc_button, clear_button],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Container(height=10),
                    image_control,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                spacing=10,
            ),
            padding=ft.Padding.symmetric(horizontal=24, vertical=10),
        ),
    )


if __name__ == "__main__":
    ft.run(main)