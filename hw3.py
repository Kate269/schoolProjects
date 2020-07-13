from typing import List, Tuple, Optional


def new_playground(size: int) -> List[List[str]]:
    plan = []
    for _ in range(size):
        plan_row = []
        for _ in range(size):
            plan_row.append(' ')
        plan.append(plan_row)
    return plan


def init_playground(playground: List[List[str]]) -> List[List[str]]:
    start_position = len(playground) // 2
    if start_position-1:
        playground[start_position-1][start_position-1] = "X"
        playground[start_position-1][start_position] = "O"
    if start_position:
        playground[start_position][start_position] = "X"
        playground[start_position][start_position - 1] = "O"
    return playground


def get(playground: List[List[str]], row: int, col: int) -> str:
    return playground[row][col]


def set_symbol(playground: List[List[str]], row: int,
               col: int, symbol: str) -> None:
    playground[row][col] = symbol


def inside_playground(playground: List[List[str]], row: int, col: int) -> bool:
    size = len(playground)
    if row >= size or col >= size or row < 0 or col < 0:
        return False
    return True


def other_sym(symbol: str) -> str:
    if symbol == "X":
        return "O"
    else:
        return "X"


def check_direction(playground: List[List[str]], row: int, col: int, symbol:
                    str, direction: Tuple[int, int]) -> List[Tuple[int, int]]:
    x = col + direction[0]
    y = row + direction[1]
    count = 0
    will_change: List[Tuple[int, int]] = []
    while inside_playground(playground, y, x) and \
            get(playground, y, x) == other_sym(symbol):
        x += direction[0]
        y += direction[1]
        count += 1
    if not inside_playground(playground, y, x):
        return will_change
    if get(playground, y, x) == symbol:
        for _ in range(count):
            x -= direction[0]
            y -= direction[1]
            will_change.append((x, y))
    return will_change


def play(playground: List[List[str]], row: int,
         col: int, symbol: str) -> Optional[int]:
    to_flip = []
    for x_direction, y_direction in [(1, 0), (0, 1), (-1, 0), (0, -1),  # 1
                                     (-1, -1), (1, 1), (-1, 1), (1, -1)]:
        to_flip.extend(check_direction(playground, row, col,
                                       symbol, (x_direction, y_direction)))
    if len(to_flip) == 0 or get(playground, row, col) != " ":
        return None
    else:
        for other_symbol in to_flip:
            set_symbol(playground, other_symbol[1], other_symbol[0], symbol)
        set_symbol(playground, row, col, symbol)
        return len(to_flip)


def separator_line_print(playground: List[List[str]]) -> None:
    size = len(playground)
    print("   +" + "---+"*size, end="")
    print()


def head_of_table(playground: List[List[str]]) -> None:
    print("   ", end="")
    size = len(playground)
    for start_position in range(size):
        letter = (chr(ord('A') + start_position))
        print("  " + letter, end=" ")
    print()
    separator_line_print(playground)


def print_line_of_table(playground: List[List[str]]) -> None:
    size = len(playground)
    for row in range(size):
        print("{:>2}".format(row), end=" ")
        for col in range(size):
            print("| " + playground[row][col] + " ", end="")
        print("|")
        separator_line_print(playground)


def draw(playground: List[List[str]]) -> None:
    head_of_table(playground)
    print_line_of_table(playground)


def game_over(playground: List[List[str]], current_symbol: str) -> bool:
    for y in range(len(playground)):
        for x in range(len(playground)):
            if get(playground, y, x) != ' ':
                continue
            for x_direction, y_direction in [(1, 0), (0, 1), (-1, 0),
                                             (0, -1), (-1, -1), (1, 1),
                                             (-1, 1), (1, -1)]:
                if len(check_direction(playground, y, x, current_symbol,
                                       (x_direction, y_direction))) != 0:
                    return False
    return True


def count_X(playground: List[List[str]]) -> int:
    X_score = 0
    for y in range(len(playground)):
        for x in range(len(playground)):
            if get(playground, y, x) == 'X':
                X_score += 1
    return X_score


def count_O(playground: List[List[str]]) -> int:
    O_score = 0
    for y in range(len(playground)):
        for x in range(len(playground)):
            if get(playground, y, x) == 'O':
                O_score += 1
    return O_score


def count(playground: List[List[str]]) -> Tuple[int, int]:
    X_count = int(count_X(playground))
    O_count = int(count_O(playground))
    return X_count, O_count


def rules_print(size: int) -> None:
    rules = input("Do you want to read the rules? Write Y/N: ")
    if rules.lower() == "y":
        print("""Reversi Rules!
        Each reversi piece has a X side and a O side. On your turn,
        you place one piece on the board with your symbol facing up.
        You must place the piece so that your opponent's piece
        or row of opponent's pieces is flanked by your pieces.
        If one of the players can't have change symbol of the
        other player or the plan is full the game is over!
        The player who has more symbols on the plan wins!
        """)


def welcome_reversi_print(size: int) -> None:
    print("Welcome in...")
    print("    ", "╔═════════════╗")
    print("    ", "║   Reversi!  ║")
    print("    ", "╚═════════════╝")


def game(size: int) -> None:
    welcome_reversi_print(size)
    rules_print(size)
    name_player_one = input("Player one with symbol 'X': write your name: ")
    name_player_two = input("Player two with symbol 'O': write your name: ")
    name_X = str(name_player_one)
    name_O = str(name_player_two)
    playground = new_playground(size)
    init_playground(playground)
    current_player = "X"
    other_symbol = "O"
    while game_over is not True:
        draw(playground)
        print("Current score:")
        print("  ", name_X + ":", count_X(playground))
        print("  ", name_O + ":", count_O(playground))
        print("Now play:", name_player_one, "(" + current_player + ")!")
        col_input = input("Select the column, please: ")
        try:
            row_play = int(input("Select the row, please: "))
        except ValueError:
            print("For row write only numbers!")
            continue
        col_play = int(ord(col_input.lower()) - ord('a'))
        if not inside_playground(playground, row_play, col_play):
            print("Invalid enter! Try again.")
            continue
        play_game = play(playground, row_play, col_play, current_player)
        if play_game is not None:
            name_player_one, name_player_two = name_player_two, name_player_one
            current_player, other_symbol = other_symbol, current_player
            if game_over(playground, current_player):
                draw(playground)
                print("  ", name_X + ":", count_X(playground),
                      "|", name_O + ":", count_O(playground))
                break
        else:
            print("Invalid enter! Try again.")
    points_X, points_O = count(playground)
    if points_X == points_O:
        print("You both won! Congratulations!")
    if points_X > points_O:
        print(name_X, "won! Congratulations!")
    else:
        print(name_O, "won! Congratulations!")


if __name__ == "__main__":
    game(4)

"""
--- HW3 from university ---

Reversi – hra dvou hráčů

V tomto domácím úkolu si naimplementujete hru Reversi, a to ve variantě hry dvou hráčů.

Část 1 (1 bod) – Reprezentace herního plánu
Způsob reprezentace herního plánu je na vás. Naše testy o této reprezentaci nebudou nic předpokládat,
a budou k ní přistupovat jen pomocí níže popsaných funkcí.

    new_playground(size) – vytvoří a vrátí prázdný herní plán o zadané velikosti. 
    Předpokládejte, že parametr size je kladné sudé číslo větší nebo rovno 4.
    
    init_playground(playground) – nastaví herní plán do počáteční situace, kdy jsou uprostřed plánu 
    dva kameny každého hráče do kříže (viz odkaz na Wikipedii výše nebo příklad vykreslení níže). 
    Předpokládejte, že playground je prázdný herní plán (vzniklý voláním new_playground).
    
    get(playground, row, col) – vrátí reprezentaci políčka na zadaném řádku a sloupci 
    (obojí budou přirozená čísla; levý horní roh plánu má souřadnice (0, 0)). 
    Prázdné políčko je reprezentováno jednou mezerou " ", políčka s křížkem řetězcem "X" (velké X) 
    a políčka s kolečkem řetězcem "O" (velké O). Předpokládejte, že zadané souřadnice jsou platné 
    (tj. nejsou mimo rozsah herního plánu).
    
    set_symbol(playground, row, col, symbol) – přidá do herního plánu zadaný symbol na zadané 
    souřadnice. Tato funkce nepřebarvuje soupeřovy kameny! Je určena pouze pro účely testování.
     Funkce nic nevrací. Pokud je políčko již obsazené, je jeho obsah změněn na zadaný symbol.
      Předpokládejte, že row, col jsou platné souřadnice a že symbol je buď "X" (velké X)
      nebo "O" (velké O).

Ani jedna z těchto funkcí nic nevypisuje.
Část 2 (2 body) – Vykreslení herního plánu

Vytvořte funkci draw(playground), která herní plán textově vykreslí podle následujícího vzoru:

     A   B   C   D   E   F   G   H   I   J   K   L
   +---+---+---+---+---+---+---+---+---+---+---+---+
 0 |   |   |   |   |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+---+---+---+---+
 1 |   |   |   |   |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+---+---+---+---+
 2 |   |   |   |   |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+---+---+---+---+
 3 |   |   |   |   |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+---+---+---+---+
 4 |   |   |   |   |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+---+---+---+---+
 5 |   |   |   |   |   | X | O |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+---+---+---+---+
 6 |   |   |   |   |   | O | X |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+---+---+---+---+
 7 |   |   |   |   |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+---+---+---+---+
 8 |   |   |   |   |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+---+---+---+---+
 9 |   |   |   |   |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+---+---+---+---+
10 |   |   |   |   |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+---+---+---+---+
11 |   |   |   |   |   |   |   |   |   |   |   |   |
   +---+---+---+---+---+---+---+---+---+---+---+---+

Pro účely této funkce předpokládejte, že počet řádků a sloupců herního plánu je maximálně 26 (totéž můžete předpokládat v části 5,
ale ostatní části musí fungovat s libovolně velkým herním plánem). Výsledek musí přesně odpovídat tomuto vzoru včetně počtu mezer
(mezery na koncích řádků ignorujeme).
Poslední řádek musí být ukončen znakem nového řádku (tak, aby další výstup začínal hned na dalším novém řádku). Všimněte si dobře,
kde a jak jsou popsány řádky a sloupce a jak jsou zarovnána čísla.

Funkce nic nevrací ani nijak nemodifikuje herní plán.
Část 3 (2 body) – Tah hráče

Vytvořte funkci play(playground, row, col, symbol), která provede tah hráče se zadaným symbolem na pole o zadaných souřadnicích.
Pokud je tah neplatný (zadané pole již je obsazeno nebo tahem na zadané pole nedojde k přebarvení žádných protivníkových kamenů),
pak funkce vrátí None a nezmění herní plán. V opačném případě funkce kameny přebarví a vrátí jejich počet.
Část 4 (2 body) – Zjištění konce hry a počítání kamenů

Vytvořte funkci game_over(playground, current_symbol), která odpoví na otázku, zda je hra v současné situaci u konce,
pokud je na tahu hráč se symbolem current_symbol (předpokládejte, že je to buď velké "X" nebo velké "O"). Funkce vrací True nebo False. Funkce nic nevypisuje ani nemění stav herního plánu.

Dále vytvořte funkci count(playground), která vrátí dvojici (počet kamenů hráče X, počet kamenů hráče O).
Část 5 (2 body) – Samotná hra

Napište funkci game(size), která spustí hru. Přesná podoba hry je na vás – zde máte možnost být kreativní. Požadujeme pouze, aby byla hra uživatelsky příjemná, tedy by měla splňovat následující body:

    uživatel by měl být jasně informován o průběhu hry (včetně průběžného vykreslování herního plánu),
    pokud načítáte od uživatele vstup, mělo by mu být jasné, co se po něm chce,
    v případě, že uživatel zadá nevalidní vstup, tak by se s tím hra měla nějak rozumně vypořádat (např. napsat, co bylo špatně, a zeptat se znovu),
    na konci hry by měl uživatel dostat jasnou informaci o tom, kdo vyhrál, případně, že došlo k remíze.
"""
