import flet as ft

def tela_inicial(page, on_cadastrar, on_acompanhar):
    page.title = "Vacinação Bovina"
    page.clean()

    titulo = ft.Text(
        "Controle de Vacinação Bovina",
        size=24,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    btn_cadastrar = ft.Button(
        content="Cadastrar Animal",
        icon=ft.Icons.ADD,
        width=250,
        height=50,
        on_click=lambda e: on_cadastrar(),
    )

    btn_acompanhar = ft.Button(
        content="Acompanhar Animais",
        icon=ft.Icons.LIST,
        width=250,
        height=50,
        on_click=lambda e: on_acompanhar(),
    )

    conteudo = ft.Column(
        controls=[
            titulo,
            ft.Container(height=30),
            btn_cadastrar,
            btn_acompanhar,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(ft.SafeArea(content=conteudo))
    page.update()