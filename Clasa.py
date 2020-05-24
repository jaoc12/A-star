# 242 Chitu Stefan Catalin
import time


class Nod:
    def __init__(self, info, suparati, clasa, semn_mutare, h=0):
        self.info = info                    # in info memoram la ce elev se afla biletul
        self.h = h
        self.suparati = suparati            # lista elevilor suparati unul pe celalalt
        self.clasa = clasa                  # matrice cu clasa
        self.semn_mutare = semn_mutare      # directia in care a fost dat biletul

    def __str__(self):
        return "({}, h={})".format(self.info, self.h)

    def __repr__(self):
        return f"({self.info}, h={self.h})"


class Problema:
    def __init__(self, filename):
        self.nod_start, self.nod_scop = read_input(filename)


class NodParcurgere:

    problema = None

    def __init__(self, nod_graf, parinte=None, f=None):
        self.nod_graf = nod_graf
        self.parinte = parinte
        self.g = 1
        if f is None :
            self.f = self.g + self.nod_graf.h
        else:
            self.f = f

    def funct_h(self, info):
        solutie = self.problema.nod_scop
        count = 0

        if euristica == 0:
            # folosim pentru h distanta manhattan de la elevul curent pana la cel scop
            # o sa subestimeze distanta deoarece nu ia in considerare restrictiile de deplasare
            x_nod, y_nod = self.gaseste_elev(info)
            x_scop, y_scop = self.gaseste_elev(solutie)
            count = abs(x_nod - x_scop) + abs(y_nod - y_scop)

        if euristica == 1:
            # h reprezinta cate randuri de banci se afla intre elevul curent si cel scop
            # o sa subestimeze distanta deoarece nu stie daca elevul scop este imediat pe coloana urmatoare
            # sau in capatul ei
            x_nod, y_nod = self.gaseste_elev(info)
            x_scop, y_scop = self.gaseste_elev(solutie)
            count = abs(y_nod/2 - y_scop/2)

        if euristica == 3:
            # prefera sa ramana pe aceeasi linie
            # poate supraestima daca elevul scop este in fata sau in spatele celui actual
            x_nod, y_nod = self.gaseste_elev(info)
            x_tata, y_tata = self.gaseste_elev(self.nod_graf.info)
            count = abs(x_tata - x_nod)

        return count

    def drum_arbore(self):
        # reface drumul de la nodul curent la radacina
        nod_c = self
        drum = [nod_c]
        while nod_c.parinte is not None:
            drum = [nod_c.parinte] + drum
            nod_c = nod_c.parinte
        return drum

    def contine_in_drum(self, nod):
        # verifica daca se afla in drum deja
        drum = self.drum_arbore()
        for nod_c in drum:
            if nod_c.nod_graf.info == nod.info:
                return True
        return False

    def gaseste_elev(self, info):
        # cauta coordonatele elevului dat ca argument
        for i in range(len(self.nod_graf.clasa)):
            for j in range(6):
                if self.nod_graf.clasa[i][j] == info:
                    return i, j

    def suparati(self, elev_1, elev_2):
        # verifica daca doi elevi dati sunt in lista celor suparati
        # relatia de suparare este reciproca
        for suparati in self.nod_graf.suparati:
            if suparati[0] == elev_1:
                if suparati[1] == elev_2:
                    return True
            if suparati[0] == elev_2:
                if suparati[1] == elev_1:
                    return True
        return False

    def expandeaza(self):
        succesori = []
        info = self.nod_graf.info
        clasa = self.nod_graf.clasa
        vecini = [[0, -1], [0, 1], [-1, 0], [1, 0]]     # lista cu cei 4 vecini posibili
        x, y = self.gaseste_elev(info)
        for i, coordonate in enumerate(vecini):
            x_vecin = x + coordonate[0]
            y_vecin = y + coordonate[1]
            if 0 > x_vecin or x_vecin >= len(clasa) or 0 > y_vecin or y_vecin >= 6:
                continue    # daca pozitia noua nu este in matrice trecem la urmatoarea
            vecin = clasa[x_vecin][y_vecin]
            ultima_banca = False
            if self.suparati(info, vecin) is True or vecin == 'liber':
                continue    # daca elevii sunt ceratati trecem la urmatoarea posibilitate
            if x in list(range(len(clasa)))[-2:]:
                ultima_banca = True     # testam daca se afla in ultimele doua randuri
            if i == 0:
                # daca da biletul in stanga ne asiguram ca se afla in spate sau e pe pozitia dreapta din rand
                if y % 2 == 0 and ultima_banca is True:
                    succesori.append((Nod(vecin, self.nod_graf.suparati, clasa, "<<", self.funct_h(vecin)), 1))
                if y % 2 == 1:
                    succesori.append((Nod(vecin, self.nod_graf.suparati, clasa, "<", self.funct_h(vecin)), 1))
            if i == 1:
                # analog cu stanga
                if y % 2 == 1 and ultima_banca is True:
                    succesori.append((Nod(vecin, self.nod_graf.suparati, clasa, ">>", self.funct_h(vecin)), 1))
                if y % 2 == 0:
                    succesori.append((Nod(vecin, self.nod_graf.suparati, clasa, ">", self.funct_h(vecin)), 1))
            if i == 2:
                succesori.append((Nod(vecin, self.nod_graf.suparati, clasa, "^", self.funct_h(vecin)), 1))
            if i == 3:
                succesori.append((Nod(vecin, self.nod_graf.suparati, clasa, "v", self.funct_h(vecin)), 1))

        return succesori

    def test_scop(self):
        # vedem daca am ajuns la elevul vizat
        return self.nod_graf.info == self.problema.nod_scop

    def __str__(self):
        parinte = self.parinte if self.parinte is None else self.parinte.nod_graf.info
        return f"({self.nod_graf}, parinte={parinte}, f={self.f}, g={self.g})"


def read_input(file_name):
    f = open(file_name, "rt")
    temp = f.read().splitlines()
    flag = 1
    clasa = []
    suparati = []
    info = ''
    # avem 3 etape de citit
    # pozitia in clasa - flag = 1
    # lista de elevi suparati - flag = 2
    # de la cine pentru cine este mesajul - flag = 3
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
    for i in range(len(lista)):
        if lista[i].nod_graf.info == nod.info:
            return lista[i]
    return None


def afisare_elev(nod):
    # afiseaza un elev plus directia din care a venit mesajul la el
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
    open = [rad_arbore]
    closed = []
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
            if nod_curent.contine_in_drum(s[0]) is False:   # verificam daca nodul e deja in drum
                nod_open = in_lista(open, s[0])
                if nod_open is not None:    # daca este in open testam daca f curent este mai bun
                    if nod_open.f > nod_nou.f:
                        open.remove(nod_open)
                        flag = True
                nod_closed = in_lista(closed, s[0])
                if nod_closed is not None:  # daca este in closed testam daca f curent este mai bun
                    if nod_closed.f > nod_nou.f:
                        closed.remove(nod_closed)
                        flag = True
                if nod_open is None and nod_closed is None:
                    flag = True
                if flag is True:
                    if len(open) == 0:  # daca nu este in nicio lista si open e gol il punem direct
                        open.append(nod_nou)
                    else:
                        adaugat = False
                        for i in range(len(open)):  # cautam locul potrivit in open
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

    # producem mesajul de output
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
        for i in range(3):  # testam inputul pentru fiecare euristica
            euristica = i
            if i == 0:
                f = open(f"output_{nr + 1}.txt", "wt")
            else:
                f = open(f"output_{nr + 1}.txt", "at")
            t_inainte = int(round(time.time() * 1000))
            mesaj, count = a_star()
            t_dupa = int(round(time.time() * 1000))
            mesaj += f"\nTimpul necesar a fost de {t_dupa - t_inainte} milisecunde.\n"
            mesaj += f"A fost nevoie de {count} de mutari.\n"
            f.write(mesaj)
            f.close()
