import flet as ft

def tela_acompanhamento(page, lista_animais, dicionario, on_aplicar, on_excluir, on_voltar):
    page.title = "Acompanhar Animais"
    page.clean()

    titulo = ft.Text(
        "Acompanhar Animais",
        size=24,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    btn_voltar = ft.Button(
        content="Voltar",
        icon=ft.Icons.ARROW_BACK,
        width=140,
        height=45,
        on_click=lambda e: on_voltar(),
    )

    if not lista_animais:
        mensagem = ft.Text(
            "Nenhum animal cadastrado.",
            size=16,
            color=ft.Colors.GREY,
            text_align=ft.TextAlign.CENTER,
        )
        conteudo = ft.Column(
            controls=[titulo, ft.Container(height=20), mensagem, ft.Container(height=20), btn_voltar],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        page.add(conteudo)
        page.update()
        return

    def abrir_dialog_aplicar(animal_ref, vacina_ref):
        def on_sim(e):
            page.pop_dialog()
            on_aplicar(animal_ref, vacina_ref)

        def on_nao(e):
            page.pop_dialog()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Aplicação"),
            content=ft.Text(f"Vacina {vacina_ref.nome} foi aplicada em {animal_ref.nome}?"),
            actions=[
                ft.TextButton("Sim", on_click=on_sim),
                ft.TextButton("Não", on_click=on_nao),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.show_dialog(dialog)

    def abrir_dialog_excluir(animal_ref):
        def on_sim(e):
            page.pop_dialog()
            on_excluir(animal_ref)

        def on_nao(e):
            page.pop_dialog()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text(f"Excluir {animal_ref.nome}? Esta ação não pode ser desfeita."),
            actions=[
                ft.TextButton("Sim", on_click=on_sim),
                ft.TextButton("Não", on_click=on_nao),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.show_dialog(dialog)

    animais_widgets = []

    for animal in lista_animais:
        periodos = dicionario.get(animal, [])
        periodos_visiveis = [p for p in periodos if p.nivel in ("no_prazo", "atrasado")]

        idade = animal.calcular_idade_meses()
        sexo_texto = "Macho" if animal.sexo == "M" else "Fêmea"

        detalhes_controls = [
            ft.Text(f"Nome: {animal.nome}", size=14),
            ft.Text(f"Sexo: {sexo_texto}", size=14),
            ft.Text(f"Data de Nascimento: {animal.data_nascimento}", size=14),
            ft.Text(f"Idade: {idade} meses", size=14),
            ft.Container(height=10),
        ]

        if not periodos_visiveis:
            detalhes_controls.append(
                ft.Text(
                    "Nenhuma vacina no prazo no momento",
                    size=13,
                    color=ft.Colors.GREY,
                    italic=True,
                )
            )
        else:
            for periodo in periodos_visiveis:
                vacina_nome = periodo.vacina.nome
                nivel = periodo.nivel

                if nivel == "no_prazo":
                    cor = ft.Colors.GREEN
                    status_texto = "No prazo"
                else:
                    cor = ft.Colors.RED
                    status_texto = "Atrasado"

                data_inicio_fmt = periodo.data_inicio.strftime("%d/%m/%Y") if periodo.data_inicio else "—"
                data_fim_fmt = periodo.data_fim.strftime("%d/%m/%Y") if periodo.data_fim else "Sem prazo"

                btn_aplicar = ft.Button(
                    icon=ft.Icons.VACCINES,
                    width=45,
                    height=32,
                    tooltip="Confirmar aplicação",
                    on_click=lambda e, a=animal, v=periodo.vacina: abrir_dialog_aplicar(a, v),
                )

                badge = ft.Container(
                    content=ft.Text(status_texto, size=12, color=ft.Colors.WHITE),
                    bgcolor=cor,
                    padding=ft.Padding.only(left=8, right=8, top=4, bottom=4),
                    border_radius=4,
                )

                coluna_vacina = ft.Column(
                    controls=[
                        ft.Text(vacina_nome, size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Início: {data_inicio_fmt}", size=11, color=ft.Colors.GREY),
                        ft.Text(f"Fim: {data_fim_fmt}", size=11, color=ft.Colors.GREY),
                    ],
                    spacing=2,
                    expand=True,
                )

                linha_periodo = ft.Row(
                    controls=[
                        coluna_vacina,
                        badge,
                        btn_aplicar,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )

                detalhes_controls.append(linha_periodo)

        btn_excluir = ft.Button(
            content=ft.Text("Excluir Animal", size=12),
            icon=ft.Icons.DELETE,
            width=140,
            height=38,
            style=ft.ButtonStyle(
                color=ft.Colors.RED,
                bgcolor=ft.Colors.RED_50,
            ),
            on_click=lambda e, a=animal: abrir_dialog_excluir(a),
        )

        detalhes_controls.append(ft.Container(height=10))
        detalhes_controls.append(btn_excluir)

        detalhes = ft.Container(
            content=ft.Column(
                controls=detalhes_controls,
                visible=False,
                spacing=8,
            ),
            padding=ft.Padding.only(left=16, right=16, top=8, bottom=16),
        )

        def criar_toggle(detalhes_ref):
            def toggle(e):
                inner = detalhes_ref.content
                inner.visible = not inner.visible
                page.update()
            return toggle

        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(
                        animal.nome,
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK87,
                    ),
                    ft.Icon(ft.Icons.EXPAND_MORE, color=ft.Colors.GREY),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=16,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=8,
            on_click=criar_toggle(detalhes),
        )

        bloco = ft.Column(
            controls=[header, detalhes],
            spacing=0,
        )

        animais_widgets.append(bloco)

    lista_scroll = ft.Column(
        controls=animais_widgets,
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    conteudo = ft.Column(
        controls=[
            titulo,
            ft.Container(height=20),
            lista_scroll,
            ft.Container(height=10),
            btn_voltar,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    page.add(ft.SafeArea(content=conteudo))
    page.update()
