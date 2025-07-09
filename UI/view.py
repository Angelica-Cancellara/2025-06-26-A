import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Esame del 26/06/2025 - Turno A"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_name = None
        self.btn_hello = None
        self.txt_result = None
        self.txt_container = None

    def load_interface(self):
        # title
        self._title = ft.Text("Esame del 26/06/2025 - Turno A", color="green", size=24)
        self._page.controls.append(self._title)

        #ROW 1
        self._ddYear1 = ft.Dropdown(label="Year start", width=150)
        self._controller.fillDDAnnoInizio()
        self._ddYear2 = ft.Dropdown(label="Year end", width=150)
        self._controller.fillDDAnnoFine()
        self._btnBuildGraph = ft.ElevatedButton(text="Crea grafo", on_click=self._controller.handleBuildGraph)
        self._btnPrintDetails = ft.ElevatedButton(text="Stampa dettagli", on_click=self._controller.handlePrintDetails)
        row1 = ft.Row([self._ddYear1, self._ddYear2, self._btnBuildGraph, self._btnPrintDetails],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        #ROW2
        self._txtGraphDetails = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)
        self._page.controls.append(self._txtGraphDetails)

        #ROW3
        self._txtInSoglia = ft.TextField(label="Soglia", width=200)
        self._txtInNumDiEdizioni = ft.TextField(label="Num di Edizioni", width=200)
        self._btnCalcolaSoluzione = ft.ElevatedButton(text="Cerca Dream Championship", on_click=self._controller.handleCercaDreamChampionship)

        row3 = ft.Row([self._txtInSoglia, self._txtInNumDiEdizioni, self._btnCalcolaSoluzione],
                      alignment=ft.MainAxisAlignment.CENTER)

        self._page.controls.append(row3)

        # List View where the reply is printed
        self._txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)
        self._page.controls.append(self._txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
