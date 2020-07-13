from random import randint, random


def dice(prob_six=1/6):
    if random() <= prob_six:
        return 6
    else:
        return randint(1, 5)

def game_print(before, iteration, throws, position, size):
    throws_print = str(throws)[1:-1]

    print(before, "->", str(position),
        "in round " + str(iteration), "(" + throws_print + ")")


def game(size, prob_six=1/6, output=True):
    if size <= 2 and output:
        print("Error: plan too small!")
        return

    iteration = 0
    position = 0
    throws = 0
    throw_count = []
    while True:
        iteration += 1
        for _ in range(3):
            throws = dice(prob_six)
            throw_count.append(throws)
            if throws == 6:
                break
        if throws == 6:
            break

        if output:
            game_print(0, iteration, throw_count, 0, size)

        throw_count = []
    if output:
        game_print(0, iteration, throw_count, 1, size)
    position = 1
    throw_count = []
    while position != size:
        iteration += 1
        before = position
        throws = dice(prob_six)
        throw_count.append(throws)
        if throws == 6:
            while throws == 6 and len(throw_count) < 3:
                throws = dice(prob_six)
                throw_count.append(throws)
        if position + sum(throw_count) <= size:
            before = position
            position += sum(throw_count)

        if output:
            game_print(before, iteration, throw_count, position, size)
        throw_count = []
    if output:
        print("Game finished in round " + str(iteration) + ".")
    return iteration


def average_game(size, games_count, prob_six=1/6):
    games = 0
    for _ in range(games_count):
        games += game(size, prob_six, output=False)
    return (games / games_count)



"""
HW2 - from university subject IB111.

Úkol 1 (1 bod)

Vytvořte funkci dice(prob_six=1/6), která simuluje hod (falešnou) šestistěnnou kostkou tak, že vrátí číslo 1, 2, 3, 4, 5, nebo 6. 
Parametr prob_six (předpokládejte, že jde o float v otevřeném intervalu (0, 1)) určuje pravděpodobnost, se kterou padá šestka. 
Ostatní čísla padají s rovnoměrnou pravděpodobností. 
(Pokud je tedy např. prob_six rovno 0.5, ostatní čísla padají s pravděpodobností 0.1.)


Tuto funkci používejte ve všech ostatních částech tohoto domácího úkolu, kde je potřeba házet kostkou. 
V testech dalších částí si tuto funkci nahradíme vlastní implementací.



Úkol 2 (4 body)

Vytvořte simulátor zjednodušené hry „Člověče, nezlob se!“ pro jednoho hráče reprezentovaný funkcí 
game(size, prob_six=1/6, output=True). Všimněte si, že parametry prob_six a output mají implicitní hodnotu. 
Funkce game se tedy dá volat i jen s jedním nebo dvěma parametry. Funkce vrátí počet odehraných kol. 
Pokud je parametr output (typu bool) nastavený na True, funkce vypisuje informace o průběhu hry (viz níže); 
v opačném případě (output je False) funkce nevypisuje nic. Parametr prob_six se předá funkci dice při házení
 kostkou.

Pravidla:
Hraje se na jednorozměrném hracím plánu o size polích + jednom speciálním poli navíc (tzv. „depo“). 
Pole jsou očíslovaná od 1 do size včetně; „depo“ má číslo 0.
Háže se kostkou (1-6).
    
Figurka začíná na poli 0 (v „depu“). Háže se do té doby, než padne šestka. Jakmile padne šestka, nasazuje se 
figurka na první pozici za depem a od dalšího kola začínají platit běžná pravidla. Každé 3 hody v depu se počítají
za samostatné kolo hry.
Když padne 6, hází se znovu. Jakmile však v jednom kole padnou tři šestky po sobě, hráč se posouvá o 18 políček a
kolo tím končí.
Figurka se posunuje o součet hodnot z hodů kostkou. Pokud by se figurka po tomto posunu ocitla 
za cílem, neposune se vůbec.
Hra končí, když figurka dorazí do cíle (na poslední pole s číslem size).
Poznámky:
Při délce hracího plánu < 2 vypište chybu Error: plan too small! (pokud je output=True, jinak nevypisujte nic)
a místo počtu odehraných kol vraťte None.


"""