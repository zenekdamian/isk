import random
import numpy

from random import randint
from route import Individual


class FixRoute(Individual):
    values = []  # tu trzymamy nasz kompletna droge
    edges = []  # tutaj trzymamy wszystkie krawedzie z pliku
    start_edge = 0  # poczatkowa krawedz od 0 do n-1 (n ilosc elementow tablicy edges)
    start_peak = 0  # poczatkowy wierzcholek
    status_key = 4  # kolumna ze statusem
    end_peak = None  # wierzcholek koncowy

    def __init__(self, edges):
        Individual.__init__(self, edges)
        self.prepareEdges(edges)

    def repair(self, route):
        result = self.checkFixedRoute(route)

        if result is False:
            route = self.addMissingEdges(route)

        return self.getFixedRoute(route)

    def getFixedRoute(self, route):
        result = self.checkIfGraphContainAllEdgesInRoute(route)

        if (result is not True):  # jezeli nie znaleziono takiej krawedzi w grafie
            if (result[0] == result[1]):  # i jezeli mamy droge z tego samego do tego samego wierzcholka np aa, bb, cc
                route = numpy.delete(route, result[2])  # usuwamy duplikat

            else:  # a jak nie to szukamy drogi miedzy tymi wierzcholkami
                route_between = self.__getRouteBetween2Peaks(result[0], result[1])
                counter = 1

                for peak in route_between:
                    route = numpy.insert(route, result[2] + counter, peak)
                    counter += 1

                # print([result[0], result[1]], result[2], route_between)

            return self.getFixedRoute(route)
        else:
            return route


    def addMissingEdges(self, route):
        for edge in self.edges:
            if (edge[self.status_key] == 0):
                route = numpy.insert(route, 1, edge[0])
                route = numpy.insert(route, 2, edge[1])

                # print('--------------------')
                # print('brakuje', edge)
                # print('w drodze', route)
                # print('--------------------')

                return route

    def checkFixedRoute(self, route):
        self.resetEdgesStatuses()

        for i in range(len(route)):  # lecimy po koleji po kazdym wierzcholku
            try:
                res = self.findRow(route[i], route[i + 1])  # sprawdzamy czy istnieje taki wierzcholek ktory nie byl jeszcze odwiedzony

                if res is not False:
                    self.changeEdgeStatus(route[i], route[i + 1])  # jesli tak to ustawimy mu status na odwiedzony

            except IndexError:
                pass

        for edge in self.edges:
            if edge[self.status_key] == 0:
                return False  # jesli istnieje jakas nieodwiedzona krawedz to zwroc false

        return True  # inaczej zwroc true

    def checkIfGraphContainAllEdgesInRoute(self, route):
        for i in range(len(route)):  # lecimy po koleji po kazdym wierzcholku
            try:
                res = self.findRow(route[i], route[i + 1], True)
                if res is False:
                    return [route[i], route[i + 1], i]  # zwroc wierzcholki miedzy ktorymi trzeba znalezc droge oraz indeks pierwszego znalezionego wierzcholka
            except IndexError:
                pass

        return True

    def __getRouteBetween2Peaks(self, start_peak, end_peak):
        self.__findRoute(start_peak, end_peak)

        result = self.values[1:-1]  # usun pierwszy i ostatni element tablicy
        return result

    def __findRoute(self, start_peak, end_peak):
        self.values = []
        self.values.append(start_peak)  # ustaw startowy wierzcholek
        self.resetEdgesStatuses()  # zresetuj odwiedzone krawedzie
        self.start_peak = start_peak  # ustawiamy ktory wierzcholek jest poczatkiem naszej drogi
        self.end_peak = end_peak  # ustaw koncowy punkt
        current_position = len(self.values) - 1  # tutaj ustawiamy "aktualna pozycje na naszej drodze"

        self.findRouteFromCurrentPosition(current_position)
        pass

    def findRouteFromCurrentPosition(self, current_position):
        if self.checkRoute() or self.values[-1] == self.end_peak:
            return False

        peak = self.values[current_position]  # bierzemy wierzcholek z aktualnej pozycji

        next_peak = self.findPeakConnectedWithGivenPeak(
            peak)  # szukamy kolejnego wierzcholka polaczonego krawedzia z aktualnym wierzcholkiem

        if next_peak:  # jezeli znaleziono kolejny wierzcholek z ktorym jest polaczony jakas nieuzyta jeszcze krawedzia z aktualnym wierzcholkiem to dodajemy go do drogi
            self.changeEdgeStatus(peak,
                                  next_peak)  # ustaw krawedz laczaca wierzcholek aktualny ze znalezionym jako odwiedzone
            self.values.append(next_peak)  # dodaj nasz znaleziony wierzcholek do drogi
            current_position = len(self.values) - 1  # przeskakujemy w pozycji do dodanego wierzcholka

            self.findRouteFromCurrentPosition(
                current_position)  # i odpalamy szukanie krawedzi dla tego wlasnie nowo dodanego wierzcholka
        else:  # aktualny wierzcholek nie posiada krawedzi laczacych go z innymi wierzcholkami ktore byly by nieuzyte wczesniej
            current_position -= 1  # wiec cofamy sie do tylu
            self.values.append(
                self.values[current_position])  # dodajemy wierzcholek do ktorego sie cofnelismy do naszej drogi

            self.findRouteFromCurrentPosition(
                current_position)  # i sprawdzamy czy ma nieuzyte jeszcze drogi z innymi wierzcholkami...

    def findPeakConnectedWithGivenPeak(self, peak):

        found = []

        for edge in self.edges:
            if edge[0] == peak and edge[self.status_key] == 0:
                found.append(edge[1])  # jak znaleziono to dodaj do tablicy znalezionych

            if edge[1] == peak and edge[self.status_key] == 0:
                found.append(edge[0])  # jak znaleziono to dodaj do tablicy znalezionych

        if found:
            neighbors = self.checkIfCurrentPeakIsNeighborWithEndPeak(found)

            if (neighbors is True):  # jezeli sasiaduje to go zwroc
                return self.end_peak

            return random.choice(found)  # a jak nie to zwroc losowy z dostepnych
        else:
            return False

    def checkIfCurrentPeakIsNeighborWithEndPeak(self, found):
        for edge in found:
            if edge == self.end_peak:  # jezeli w znalezionych sasiadujacych wierzcholkach znajduje sie nasz wierzcholek zamykajacy
                return True  # to zwroc True

        return False  # inaczej zwroc False jezeli nie ma sasiaujacego
