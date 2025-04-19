from datetime import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._selected_airportP = None
        self._selected_airportA = None

    def handle_analyze_airports(self, e):
        nMinStr = self._view._txt_minAirlines.value
        try:
            nMin = int(nMinStr)
        except ValueError:
            self._view._txt_result.controls.append(ft.Text("Il valore inserito nel campo nMin non è un intero."))
            self._view.update_page()
            return

        self._model.buildGraph(nMin)
        self._view._txt_result.controls.append(ft.Text(f"Grafo correttamente creato."))
        self._view._txt_result.controls.append(ft.Text(f"Numero nodi: {self._model.getNumNodi()}"))
        self._view._txt_result.controls.append(ft.Text(f"Numero archi: {self._model.getNumArchi()}"))

        # FILL DROPDOWN PARTENZA/ARRIVO

        self._view._ddPartenza.disabled = False
        self._view._btnConnAirports.disabled = False
        self._view._ddArrivo.disabled = False
        self._view._btnTestConn.disabled = False

        self._view._txtMaxTratte.disabled = False
        self._view._btnFindRoute.disabled = False

        allNodes = self._model.getConnNodes()
        for c in allNodes:
            self._view._ddPartenza.options.append(
                ft.dropdown.Option(data=c, on_click=self.handleDDPartenza,text=c.AIRPORT))
            self._view._ddArrivo.options.append(
                ft.dropdown.Option(data=c, on_click=self.handleDDArrivo, text=c.AIRPORT))

        # ddOpts = self._model.getConnNodes()


        self._view.update_page()
        pass

    def handleDDPartenza(self, e):
        if e.control.data is None:
            self._selected_airportP = None
        else:
            self._selected_airportP = e.control.data
        pass

    def handleDDArrivo(self, e):
        if e.control.data is None:
            self._selected_airportA = None
        else:
            self._selected_airportA = e.control.data
        pass

    def handle_connected_airports(self, e):
        if self._selected_airportP is None:
            self._view._txt_result.append(ft.Text('Selezionare un aeroporto di partenza'))
            return
        v0 = self._selected_airportP
        neighbors = self._model.getNeighborNodes(v0)
        self._view._txt_result.controls.append(ft.Text(f"Aeroporti più vicini a {v0} in ordine di peso:"))
        for n in neighbors:
            self._view._txt_result.controls.append(ft.Text(f"Aeroporto: {n[0]} - Peso: {n[1]}"))
        self._view.update_page()
        pass

    # Alla pressione del bottone "test connessione":
    #   - verificare se è pèossibile raggiungere l'aeroporto di arrivo a partire da quello di partenza
    #   - stempare un possibile percorso (se esiste) tra i due aeroporti
    def handle_test_connection(self, e):
        vp = self._selected_airportP
        va = self._selected_airportA
        # res = self._model.check_path_existence(vp, va)
        # if not res[0]:
        #     self._view._txt_result.controls.append(ft.Text(
        #         f"Non è possibile raggiungere l'aeroporto {va} dall'aeroporto {vp}"))
        #     self._view.update_page()
        # else:
        #     self._view._txt_result.controls.append(ft.Text(
        #         f"Ecco un possibile percorso per raggiungere l'aeroporto {va} dall'aeroporto {vp}:"))
        #     i = 0
        #     for n in res[1]:
        #         i += 1
        #         self._view._txt_result.controls.append(ft.Text(f"Tappa {i} - {n}"))
        #     self._view.update_page()
        if (not self._model.check_path_existence(vp, va)):
            self._view._txt_result.controls.append(ft.Text(
                f"Non è possibile raggiungere l'aeroporto {va} dall'aeroporto {vp}"))
            return
        else:
            self._view._txt_result.controls.append(ft.Text(
                f"Ecco il percorso con minor numero di tratte per raggiungere l'aeroporto {va} dall'aeroporto {vp}:"))

        path = self._model.find_path_BFS(vp, va)
        for p in path:
            self._view._txt_result.controls.append(ft.Text(f"{p}"))
        self._view.update_page()
        pass

    def handle_find_route(self, e):
        vp = self._selected_airportP
        va = self._selected_airportA
        nMax = self._view._txtMaxTratte.value

        try: nMaxInt = int(nMax)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Il valore inserito non è un numero"))
            self._view.update_page()
            return

        tic = datetime.now()
        solBest, weightBest = self._model.get_best_path(vp, va, nMaxInt)
        self._view._txt_result.controls.append(ft.Text(
            f"Ecco il percorso che comprende la maggior disponibilità di voli"
            f"congiungente {vp} e {va}: "))
        for n in solBest:
            self._view._txt_result.controls.append(ft.Text(f"{n}"))
        self._view._txt_result.controls.append(ft.Text(
            f"Numero totale di voli: {weightBest}"
        ))
        self._view._txt_result.controls.append(ft.Text(
            f"Tempo impiegato per la ricerca: {datetime.now() - tic} secondi"))

        self._view.update_page()

        pass

    def clear_page(self, e):
        self._view._txt_result.controls.clear()
        self._view.update_page()
        pass