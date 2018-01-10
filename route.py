#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import random
from random import randint


class fitness():
    values = 10000

    def __init__(self, values):
        values = 10000


class Individual(object):
    values = []  # tu trzymamy nasz kompletna droge
    edges = []  # tutaj trzymamy wszystkie krawedzie z pliku
    start_edge = 0  # poczatkowa krawedz od 0 do n-1 (n ilosc elementow tablicy edges)
    start_peak = 0  # poczatkowy wierzcholek
    status_key = 4
    fitness = fitness(10000)

    def __init__(self, edges, start_edge_index=0):
        # self.edges = [
        #     [1, 2, 2, 4, 0], # 1 2 - wierzcholki, 2,4 - wagi(bez znaczenia tutaj). Ostatni element to status 0/1
        #     [1, 5, 3, 5, 0],
        #     [1, 6, 3, 5, 0],
        #     [2, 3, 3, 5, 0],
        #     [2, 6, 3, 5, 0],
        #     [3, 4, 3, 5, 0],
        #     [3, 6, 3, 5, 0],
        #     [3, 7, 3, 5, 0],
        #     [4, 5, 3, 5, 0],
        #     [5, 6, 3, 5, 0],
        #     [7, 8, 3, 5, 0]
        # ]  # tu trzeba wczytac plik nie mam pojecia jak wiec na pale dalem na razie tablice jaka musi byc
        self.prepareEdges(edges)

    """Zwraca znaleziona droge"""

    def getRoute(self):
        self.values = []
        self.resetEdgesStatuses()
        self.start_edge = randint(0, len(self.edges) - 1)  # ustawia startowa "krawedz"
        self.values.append(self.edges[self.start_edge][0])  # dodajemy startowy wierzcholek
        self.values.append(self.edges[self.start_edge][1])  # i kolejny polaczony krawedzia z nim jako poczatek naszej drogi
        self.start_peak = self.edges[self.start_edge][0]  # ustawiamy ktory wierzcholek jest poczatkiem naszej drogi
        self.edges[self.start_edge][self.status_key] = 1  # ustawiamy status startowej krawedzi na 1 czyli ze juz zostala co najmniej raz uzyta
        self.findRoute()  # odpalamy metode szukajaca naszej drogi w grafie

    def prepareEdges(self, edges):
        for edge in edges:
            try:
                check = edge[self.status_key]
            except IndexError:
                edge.append(0)

            self.edges.append(edge)

    def resetEdgesStatuses(self):
        for edge in self.edges:
            edge[self.status_key] = 0

    """metoda odpalajaca metody ktore szuakaj drogi"""

    def findRoute(self):
        current_position = len(self.values) - 1  # tutaj ustawiamy "aktualna pozycje na naszej drodze"

        self.findRouteFromCurrentPosition(current_position)  # szuka drogi zawierajacej wszystkie krawedzie
        self.findBackRoadFromLastPeakInRoute()  # szuka drogi powrotnej do punktu startowego

    """ Szuka krawedzi od danego wierzcholka 
    ktore nie zostaly jeszcze przez nas odwiedzone"""

    def findRouteFromCurrentPosition(self, current_position):
        if self.checkRoute():
            return False

        peak = self.values[current_position]  # bierzemy wierzcholek z aktualnej pozycji

        next_peak = self.findPeakConnectedWithGivenPeak(peak)  # szukamy kolejnego wierzcholka polaczonego krawedzia z aktualnym wierzcholkiem

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

    """Szuka wierzcholka polaczonego z podanym wierzchokiem,
     krawedzia ktora nie zostala jeszcze uzyta w drodze"""

    def findPeakConnectedWithGivenPeak(self, peak):

        found = []

        for edge in self.edges:
            if edge[0] == peak and edge[self.status_key] == 0:
                found.append(edge[1])  # jak znaleziono to dodaj do tablicy znalezionych

            if edge[1] == peak and edge[self.status_key] == 0:
                found.append(edge[0])  # jak znaleziono to dodaj do tablicy znalezionych

        if found:
            return random.choice(found)  # wybierz losowy wierzcholek docelowy
        else:
            return False

    """Znajduje droge powrota do wierzcholka poczatkowego 
    z ostatniego wierzcholka w drodze"""

    def findBackRoadFromLastPeakInRoute(self):
        back_road = self.values[::-1]  # odwracamy tablice (droge) bo bedziemy wracac

        for i in range(len(back_road)):  # lecimy po koleji z kazdego wierzcholka w drodze
            key = self.findRow(back_road[i], self.start_peak, True)  # sprawdzamy czy aktualny wierzcholek sasiaduje z poczatkowym

            if key:  # jezeli sasiaduje
                self.values.append(self.start_peak)  # dodajemy go do naszej drogi
                break  # i konczymy dalsze szukanie
            else:  # jesli nie sasiaduje
                if i < len(back_road) - 1:
                    self.values.append(back_road[i + 1])  # to dodajemy kolejny wierzcholek w na drodze powrotnej
                else:
                    self.values.append(
                        back_road[i])  # w najgorszym wypadku wrocimy sie "po nitce do k?ebka" do poczatkowego punktu

                # i szukamy dalej czy ten kolejny sasiaduje z poczatkowym

    """sprawdza czy wyznaczana droga zawiera w sobie wszystkie krawedzie"""

    def checkRoute(self):
        for edge in self.edges:
            if edge[self.status_key] == 0:
                return False  # jesli znaleziono jakas nieodwiedzona krawedz zwraca false

        return True  # odwiedzilismy wszystkie krawedzie wiec jest ok

    """Zmienia status krawedzi na 1 (odwiedzono) dla dwoch podanych wierzcholkow"""

    def changeEdgeStatus(self, peak1, peak2):
        key = self.findRow(peak1, peak2)
        self.edges[key][self.status_key] = 1

    """Szuka krawedzi dla danych dwoch wierzcholkow i zwraca klucz lub false"""

    def findRow(self, peak1, peak2, ignore_status=False):
        for key, edge in enumerate(self.edges):
            # sprawdz czy istnieje krawedz peak1-peak2 lub peak2-peak1 i czy jej status=0 lub jesli ignore_status=TRUE to nie sprawdzaj statusu
            if (edge[0] == peak1 and edge[1] == peak2) or (edge[0] == peak2 and edge[1] == peak1) and (
                    (ignore_status == False and edge[self.status_key] == 0) or ignore_status == True):
                return key  # zwroc klucz w tablicy

        return False
