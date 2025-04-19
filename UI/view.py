import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.DARK
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        #row 1
        self._txt_minAirlines = None
        self.btn_hello = None
        # row 2
        self._ddPartenza= None
        self._btnConnAirports = None
        # row 3
        self._ddArrivo = None
        self._btnTestConn = None
        # row 4
        self._txtMaxTratte = None
        self._btnFindRoute = None

        self._txt_result = None
        self.txt_container = None

        # controls
        self._btn_clear = None

    def load_interface(self):
        # title
        self._title = ft.Text("Flight Delays", color="blue", size=24)
        self._page.controls.append(self._title)

        #ROW 1

        self._txt_minAirlines = ft.TextField(
            label="Min Airlines",
            width=200,
            hint_text="Insert a number"
        )
        self.btn_analyze = ft.ElevatedButton(text="Analyze airports", on_click=self._controller.handle_analyze_airports)

        row1 = ft.Row([self._txt_minAirlines, self.btn_analyze],
                      alignment=ft.MainAxisAlignment.CENTER)

        # ROW 2

        self._ddPartenza = ft.Dropdown(
            label="Departure", width=400, hint_text='Select the departure airport', disabled=True)
        self._btnConnAirports = ft.ElevatedButton(
            text="Connected Airports", on_click=self._controller.handle_connected_airports, disabled=True)

        row2 = ft.Row([self._ddPartenza, self._btnConnAirports], alignment=ft.MainAxisAlignment.CENTER)

        # ROW 3

        self._ddArrivo = ft.Dropdown(label="Arrival", width=400, hint_text='Select the arrival airport', disabled=True)
        self._btnTestConn = ft.ElevatedButton(
            text="Test Connection", on_click=self._controller.handle_test_connection, disabled=True)

        row3 = ft.Row([self._ddArrivo, self._btnTestConn], alignment=ft.MainAxisAlignment.CENTER)

        # ROW 4

        self._txtMaxTratte = ft.TextField(label='Max num routes', width=200, disabled=True)
        self._btnFindRoute = ft.ElevatedButton(
            text="Find Itinerary", on_click=self._controller.handle_find_route, disabled=True)

        row4 = ft.Row([self._txtMaxTratte, self._btnFindRoute], alignment=ft.MainAxisAlignment.CENTER)

        # controls

        self._btn_clear = ft.ElevatedButton(text='CLEAR', width=100, bgcolor='red', on_click=self._controller.clear_page)
        controls_row = ft.Row([self._btn_clear], alignment=ft.MainAxisAlignment.CENTER)


        self._page.controls.append(row1)
        self._page.controls.append(row2)
        self._page.controls.append(row3)
        self._page.controls.append(row4)
        self._page.controls.append(controls_row)

        # List View where the reply is printed
        self._txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
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
