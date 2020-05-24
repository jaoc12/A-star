
""" definirea problemei """
import time


class Nod:
    def __init__(self, info, suparati, clasa, semn_mutare, h=0):
        self.info = info
        self.h = h
        self.suparati = suparati
        self.clasa = clasa
        self.semn_mutare = semn_mutare

    def __str__(self):
        return "({}, h={})".format(self.info, self.h)

    def __repr__(self):
        return f"({self.info}, h={self.h})"


class Problema:
    def __init__(self, filename):
        self.nod_start, self.nod_scop = read_input(filename)


""" Sfarsit definire problema """

""" Clase folosite in algoritmul A* """


class NodParcurgere:
    """O clasa care cuprinde informatiile asociate unui nod din listele open/closed
        Cuprinde o referinta catre nodul in sine (din graf)
        dar are ca proprietati si valorile specifice algoritmului A* (f si g).
        Se presupune ca h este proprietate a nodului din graf
    """

    problema = None		# atribut al clasei (se suprascrie jos in __main__)

    def __init__(self, nod_graf, parinte=None, f=None):
        self.nod_graf = nod_graf    # obiect de tip Nod
        self.parinte = parinte		# obiect de tip NodParcurgere
        self.g = 1					# costul drumului de la radacina pana la nodul curent
        if f is None :
            self.f = self.g + self.nod_graf.h
        else:
            self.f = f

    def funct_h(self, info):
        solutie = self.problema.nod_scop
        count = 0

        if euristica == 0:
            x_nod, y_nod = self.gaseste_elev(info)
            x_scop, y_scop = self.gaseste_elev(solutie)
            count = abs(x_nod - x_scop) + abs(y_nod - y_scop)

        if euristica == 1:
            x_nod, y_nod = self.gaseste_elev(info)
            x_scop, y_scop = self.gaseste_elev(solutie)
            count = abs(y_nod/2 - y_scop/2)

        if euristica == 3:
            x_nod, y_nod = self.gaseste_elev(info)
            x_scop, y_scop = self.gaseste_elev(solutie)
            x_tata, y_tata = self.gaseste_elev(self.nod_graf.info)
            count = abs(x_nod - x_scop) + abs(y_nod - y_scop)
            count /= (abs(x_tata - x_nod) + 1)

        return count

    def drum_arbore(self):
        """
            Functie care calculeaza drumul asociat unui nod din arborele de cautare.
            Functia merge din parinte in parinte pana ajunge la radacina
        """
        nod_c = self
        drum = [nod_c]
        while nod_c.parinte is not None:
            drum = [nod_c.parinte] + drum
            nod_c = nod_c.parinte
        return drum

    def contine_in_drum(self, nod):
        """
            Functie care verifica daca nodul "nod" se afla in drumul dintre radacina si nodul curent (self).
            Verificarea se face mergand din parinte in parinte pana la radacina
            Se compara doar informatiile nodurilor (proprietatea info)
            Returnati True sau False.

            "nod" este obiect de tip Nod (are atributul "nod.info")
            "self" este obiect de tip NodParcurgere (are "self.nod_graf.info")
        """

        drum = self.drum_arbore()
        for nod_c in drum:
            if nod_c.nod_graf.info == nod.info:
                return True
        return False

    def gaseste_elev(self, info):
        for i in range(len(self.nod_graf.clasa)):
            for j in range(6):
                if self.nod_graf.clasa[i][j] == info:
                    return i, j

    def suparati(self, elev_1, elev_2):
        for suparati in self.nod_graf.suparati:
            if suparati[0] == elev_1:
                if suparati[1] == elev_2:
                    return True
            if suparati[0] == elev_2:
                if suparati[1] == elev_1:
                    return True
        return False

    # se modifica in functie de problema
    def expandeaza(self):
        """Pentru nodul curent (self) parinte, trebuie sa gasiti toti succesorii (fiii)
        si sa returnati o lista de tupluri (nod_fiu, cost_muchie_tata_fiu),
        sau lista vida, daca nu exista niciunul.
        (Fiecare tuplu contine un obiect de tip Nod si un numar.)
        """

        succesori = []
        info = self.nod_graf.info
        clasa = self.nod_graf.clasa
        vecini = [[0, -1], [0, 1], [-1, 0], [1, 0]]
        x, y = self.gaseste_elev(info)
        for i, coordonate in enumerate(vecini):
            x_vecin = x + coordonate[0]
            y_vecin = y + coordonate[1]
            if 0 > x_vecin or x_vecin >= len(clasa) or 0 > y_vecin or y_vecin >= 6:
                continue
            vecin = clasa[x_vecin][y_vecin]
            ultima_banca = False
            if self.suparati(info, vecin) is True or vecin == 'liber':
                continue
            if x in list(range(len(clasa)))[-2:]:
                ultima_banca = True
            if i == 0:
                if y % 2 == 0 and ultima_banca is True:
                    succesori.append((Nod(vecin, self.nod_graf.suparati, clasa, "<<", self.funct_h(vecin)), 1))
                if y % 2 == 1:
                    succesori.append((Nod(vecin, self.nod_graf.suparati, clasa, "<", self.funct_h(vecin)), 1))
            if i == 1:
                if y % 2 == 1 and ultima_banca is True:
                    succesori.append((Nod(vecin, self.nod_graf.suparati, clasa, ">>", self.funct_h(vecin)), 1))
                if y % 2 == 0:
                    succesori.append((Nod(vecin, self.nod_graf.suparati, clasa, ">", self.funct_h(vecin)), 1))
            if i == 2:
                succesori.append((Nod(vecin, self.nod_graf.suparati, clasa, "^", self.funct_h(vecin)), 1))
            if i == 3:
                succesori.append((Nod(vecin, self.nod_graf.suparati, clasa, "v", self.funct_h(vecin)), 1))

        return succesori

    # se modifica in functie de problema
    def test_scop(self):
        return self.nod_graf.info == self.problema.nod_scop

    def __str__(self):
        parinte = self.parinte if self.parinte is None else self.parinte.nod_graf.info
        return f"({self.nod_graf}, parinte={parinte}, f={self.f}, g={self.g})"


""" Algoritmul A* """


def read_input(file_name):
    f = open(file_name, "rt")
    temp = f.read().splitlines()
    flag = 1
    clasa = []
    suparati = []
    info = ''
    for i in range(len(temp)):
        if temp[i] == 'suparati':
            flag = 2
            continue
        if 'mesaj' in temp[i]:
            info = temp[i].split(" ")[1]
            scop = temp[i].split(" ")[3]
        if flag == 1:
            clasa.append([x for x in temp[i].split(' ')])
        if flag == 2:
            suparati.append([x for x in temp[i].split(' ')])
    return Nod(info, suparati, clasa, ""), scop


def in_lista(lista, nod):
    """
    lista "l" contine obiecte de tip NodParcurgere
    "nod" este de tip Nod
    """
    for i in range(len(lista)):
        if lista[i].nod_graf.info == nod.info:
            return lista[i]
    return None


def afisare_elev(nod):
    sir = ""
    if nod.nod_graf.semn_mutare != "":
        sir += nod.nod_graf.semn_mutare + " "
    sir += nod.nod_graf.info + " "
    return sir


def afisare_simpla(lista):
    sir = ""
    for nod in lista:
        sir += afisare_elev(nod)
    return sir


def a_star():
    rad_arbore = NodParcurgere(NodParcurgere.problema.nod_start)
    open = [rad_arbore]		# open va contine elemente de tip NodParcurgere
    closed = []				# closed va contine elemente de tip NodParcurgere
    count = 0
    while len(open) > 0:
        nod_curent = open[0]
        count += 1
        if nod_curent.test_scop():
            break
        open = open[1:]
        closed.append(nod_curent)
        succersori = nod_curent.expandeaza()
        for s in succersori:
            flag = False
            nod_nou = NodParcurgere(s[0], nod_curent)
            if nod_curent.contine_in_drum(s[0]) is False:
                nod_open = in_lista(open, s[0])
                if nod_open is not None:
                    if nod_open.f > nod_nou.f:
                        open.remove(nod_open)
                        flag = True
                nod_closed = in_lista(closed, s[0])
                if nod_closed is not None:
                    if nod_closed.f > nod_nou.f:
                        closed.remove(nod_closed)
                        flag = True
                if nod_open is None and nod_closed is None:
                    flag = True
                if flag is True:
                    if len(open) == 0:
                        open.append(nod_nou)
                    else:
                        adaugat = False
                        for i in range(len(open)):
                            if open[i].f > nod_nou.f:
                                open = open[:i] + [nod_nou] + open[i:]
                                adaugat = True
                                break
                            elif open[i].f == nod_nou.f and open[i].g <= nod_nou.g:
                                open = open[:i] + [nod_nou] + open[i:]
                                adaugat = True
                                break
                        if adaugat is False:
                            open.append(nod_nou)

    mesaj = "\n------------------ Concluzie -----------------------\n"
    if len(open) == 0:
        return mesaj + "Lista open e vida, nu avem drum de la nodul start la nodul scop", count
    else:
        return mesaj + afisare_simpla(nod_curent.drum_arbore()), count


if __name__ == "__main__":
    lista_fisiere = ["input_1.txt", "input_2.txt", "input_3.txt", "input_4.txt"]
    for nr, fisier_intrare in enumerate(lista_fisiere):
        problema = Problema(fisier_intrare)
        NodParcurgere.problema = problema
        global euristica
        for i in range(3):
            euristica = i
            if i == 0:
                f = open(f"output_{nr + 1}.txt", "wt")
            else:
                f = open(f"output_{nr + 1}.txt", "at")
            t_inainte = int(round(time.time() * 1000))
            mesaj, count = a_star()
            t_dupa = int(round(time.time() * 1000))
            mesaj += f"\nTimpul necesar a fost {t_dupa - t_inainte} milisecunde.\n"
            mesaj += f"A fost nevoie de {count} de mutari.\n"
            f.write(mesaj)
            f.close()
