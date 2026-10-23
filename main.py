import flet as ft

def main(page: ft.Page):
    page.title = "Marhba"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#f0f2f5"

    page.add(
        ft.Column(
            [
                ft.Icon(ft.Icons.WAVING_HAND, size=80, color="#1877F2"),
                ft.Text("أهلا وسهلا !", size=35, weight="bold"),
                ft.Text("مرحبا بك في تطبيقي الأول بـ Flet", size=18, color="grey"),
                ft.ElevatedButton(
                    "دخول",
                    icon=ft.Icons.LOGIN,
                    on_click=lambda e: page.show_snack_bar(ft.SnackBar(ft.Text("مرحبا بك مرة أخرى!")))
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )

ft.app(target=main)

