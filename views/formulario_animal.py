import datetime
import flet as ft

def formulario_animal(page, on_salvar, on_voltar):
    page.title = "Cadastrar Animal"
    page.clean()

    hoje = datetime.date.today()
    data_selecionada = [hoje]

    titulo = ft.Text(
        "Cadastrar Novo Animal",
        size=24,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    campo_nome = ft.TextField(
        label="Nome do Animal",
        width=300,
        autofocus=True,
    )

    dropdown_sexo = ft.Dropdown(
        label="Sexo",
        width=300,
        options=[
            ft.DropdownOption(key="M", text="Macho"),
            ft.DropdownOption(key="F", text="Fêmea"),
        ],
    )

    campo_data = ft.TextField(
        label="Data de Nascimento",
        value=hoje.strftime("%Y-%m-%d"),
        width=230,
        read_only=True,
    )

    btn_data = ft.Button(
        icon=ft.Icons.CALENDAR_MONTH,
        width=60,
        height=48,
        on_click=lambda e: page.show_dialog(date_picker),
    )

    def handle_date_change(e):
        data = e.control.value
        if data:
            data_selecionada[0] = data.date() if hasattr(data, 'date') else data
            campo_data.value = data_selecionada[0].strftime("%Y-%m-%d")
            campo_data.update()

    date_picker = ft.DatePicker(
        first_date=datetime.datetime(year=2010, month=1, day=1),
        last_date=datetime.datetime.now(),
        current_date=datetime.datetime.now(),
        on_change=handle_date_change,
    )

    btn_salvar = ft.Button(
        content="Salvar",
        icon=ft.Icons.SAVE,
        width=140,
        height=45,
        on_click=lambda e: on_salvar(
            campo_nome.value,
            data_selecionada[0].strftime("%Y-%m-%d"),
            dropdown_sexo.value,
        ),
    )

    btn_voltar = ft.Button(
        content="Voltar",
        icon=ft.Icons.ARROW_BACK,
        width=140,
        height=45,
        on_click=lambda e: on_voltar(),
    )

    linha_data = ft.Row(
        controls=[campo_data, btn_data],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    linha_botoes = ft.Row(
        controls=[btn_voltar, btn_salvar],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    conteudo = ft.Column(
        controls=[
            titulo,
            ft.Container(height=20),
            campo_nome,
            dropdown_sexo,
            linha_data,
            ft.Container(height=20),
            linha_botoes,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(ft.SafeArea(content=conteudo))
    page.update()