from datetime import datetime, date
from typing import Dict, Tuple, Set, List


# ========================================
# Task 1: Bank (4 points)
# ========================================


def interpret_file(file_name: str, accounts: Dict[str, int]) -> None:
    num_line = 0
    lst_instructions = {
        "CREATE": (CREATE, 2),
        "ADD": (ADD, 2),
        "SUB": (SUB, 2),
        "FILTER_OUT": (FILTER_OUT, 2),
        "AGGREGATE": (AGGREGATE, 2),
        "NATIONALIZE": (NATIONALIZE, 2),
        "PRINT": (PRINT, 0)
    }

    with open(file_name, "r") as text_file:
        for line in text_file:
            num_line += 1
            line = line.strip()
            if len(line) == 0:
                continue
            args = line.split(' ')
            arg_count = len(args)
            found_instruction = False
            for instr_key in lst_instructions:
                if (args[0].startswith(instr_key)):
                    if (arg_count - 1 == lst_instructions[instr_key][1]):
                        x = lst_instructions[instr_key][0](accounts, args)
                        found_instruction = True
                        if x is None:
                            print('Instruction "{}" called with an invalid argument on line {}.'.format(args[0],
                                                                                                        num_line))
                            return
                    else:
                        print('Invalid number of arguments on line {}.'.format(num_line))
                        return
            if not found_instruction:
                print('Invalid instruction "{}" on line {}.'.format(args[0],
                                                                    num_line))
                return


def CREATE(accounts, args):
    name = args[1]
    amount = args[2]
    if not amount.isdigit():
        return
    if name not in accounts.keys() and int(amount) >= 0:
        accounts[name] = int(amount)
        return accounts


def ADD(accounts, args):
    name = args[1]
    amount = args[2]
    if not amount.isdigit():
        return
    if name in accounts and int(amount) >= 0:
        accounts[name] = int(amount) + accounts.get(name)
        return True


def SUB(accounts, args):
    name = args[1]
    amount = args[2]
    if not amount.isdigit():
        return False
    if name in accounts and int(amount) >= 0:
        accounts[name] = accounts.get(name) - int(amount)
        return True


def GetNAccs(accounts, n, richest):
    account_names = list(accounts.keys())
    return_name_accounts = []
    for account in sorted(account_names, key=lambda x: accounts[x], reverse=richest):
        if account != "STATE":
            return_name_accounts.append(account)
            if n <= 1:
                break
            n -= 1
        else:
            pass
    return return_name_accounts


def FILTER_OUT(accounts, args):
    count = args[1]
    mode = args[2]
    if not count.lstrip("-").isdigit():
        return
    count = int(count)
    if int(count) >= 0 and (mode == 'MIN' or mode == 'MAX'):

        filtered_accounts = GetNAccs(accounts, count, mode == 'MAX')
        if count > len(accounts):
            accounts = {}
        for account_name in filtered_accounts:
            del accounts[account_name]
        return accounts


def AGGREGATE(accounts, args):
    name1 = args[1]
    name2 = args[2]
    if name1 in accounts and name2 in accounts:
        accounts[name1] += accounts[name2]
        del accounts[name2]
        return accounts
    return


def NATIONALIZE(accounts, args):
    amount = args[1]
    count = args[2]
    if not amount.lstrip("-").isdigit() and not count.lstrip("-").isdigit():
        return
    amount = int(amount)
    count = int(count)
    if amount < 0 or count < 0:
        return
    state_name = "STATE"
    if state_name in accounts:
        accounts[state_name] = 0

    richest_accounts = GetNAccs(accounts, count, True)
    for account_name in richest_accounts:
        if accounts[account_name] - amount < 0:
            accounts[state_name] += accounts[account_name]
            accounts[account_name] = 0
        else:
            accounts[state_name] += amount
            accounts[account_name] -= amount
    return accounts


def PRINT(accounts, args):
    for name, value in sorted(accounts.items(), key=lambda x: (x[1], x[0])):
        print("{}: {}".format(name, value))
    return True


# ========================================
# Task 2: Chat (4 points)
# ========================================

Message = Tuple[datetime, str, str]


def to_datetime(value: str) -> datetime:
    return datetime.utcfromtimestamp(int(value))


def parse_message(line: str) -> Message:
    split_message = line.split(',')
    return to_datetime(split_message[0]), split_message[1], split_message[2]


def shortest_messages(chat: List[Message], count: int) -> List[Message]:
    sorted_messages = sorted(chat, key=lambda i: len(i[2]))
    return sorted_messages[:count]


def messages_at(chat: List[Message], day: date) -> List[Message]:
    my_list = []
    for message in chat:
        print(datetime.date(message[0]))
        if datetime.date(message[0]) == day:
            my_list.append(message)
    return my_list


def senders(chat: List[Message]) -> Set[str]:
    my_senders = set()
    for (timestamp, sender, message) in chat:
        my_senders.add(sender)
    return my_senders


def message_counts(chat: List[Message]) -> Dict[str, int]:
    my_dict = {}
    for message in chat:
        my_dict[message[1]] = my_dict.get(message[1], 0) + 1
    return my_dict


def mentions(chat: List[Message], user: str) -> List[str]:
    mentions_message_list = []
    mention_message = '@' + user
    for message in chat:
        if mention_message in message[2]:
            mentions_message_list.append(message[2])
    return mentions_message_list


# ========================================
# Task 3: Longest Word (2 points)
# ========================================

def words_in_text(text: str, words_in_txt: list):
    word = []
    for letter in text:
        if letter.isalnum():
            word.append(letter)
        else:
            words_in_txt.append(word)
            word = []
        words_in_txt.append(word)


def longest_word(text: str, provided_letters: Set[str], case_insensitive: bool = False) -> str:
    if case_insensitive:
        allowed_characters = provided_letters
        provided_letters = set()
        for word in allowed_characters:
            provided_letters.add(word.lower())
            provided_letters.add(word.upper())
    longest_word_in_text = ""
    words_in_txt = []
    words_in_text(text, words_in_txt)
    for word in words_in_txt:
        new_sets = set(word)
        if len(new_sets.difference(provided_letters)) == 0:
            if len(longest_word_in_text) <= len(word):
                longest_word_in_text = "".join(word)
    return longest_word_in_text


# ========================================
# Task 4: Parentheses Check (2 points)
# ========================================

def get_opposite_parentheses(char):
    open_bracket = ["(", "{", "["]
    close_bracket = [")", "}", "]"]
    if char in open_bracket:
        return close_bracket[open_bracket.index(char)]
    if char in close_bracket:
        return open_bracket[close_bracket.index(char)]


def parentheses_check(text, output=False):
    stacklist = []
    open_bracket = ["(", "{", "["]
    close_bracket = [")", "}", "]"]
    c = 0
    for char in text:
        if char in open_bracket:
            stacklist.append((c, get_opposite_parentheses(char)))
        if char in close_bracket:
            if len(stacklist) == 0:
                if output:
                    print("'{}' at position {} does not have an opening "
                          "paired bracket".format(char, c))
                return False
            found_at, expected_char = stacklist.pop()
            if char != expected_char:
                if output:
                    print("'{}' at position {} does not match '{}' at position {}".format(
                        get_opposite_parentheses(expected_char), found_at, char, c))
                return False
        c += 1
    if len(stacklist) != 0:
        if output:
            found_at, expected_char = stacklist.pop()
            print("'{}' at position {} does not have a closing paired bracket".format(
                get_opposite_parentheses(expected_char), found_at))
        return False

    return True


"""
HW4 from university:


Úloha 1: Interpret bankovních příkazů (4 body)

Naprogramujte interpret fiktivních bankovních příkazů – funkci interpret_file:

def interpret_file(file_name: str, accounts: Dict[str, int]) -> None

    file_name – řetězec s cestou k souboru obsahujícímu příkazy, jež mají být interpretovány
        každý neprázdný řádek se pokusí interpretovat jako příkaz
        prázdné řádky (neobsahující žádné znaky) neinterpretuje jako příkazy, ale počítá s nimi v celkovém počtu řádků
        předpokládejte, že žádný řádek nebude obsahovat pouze bílé znaky
        (poznámky přidány 26. 11.)
    accounts – databáze bankovních účtů
        slovník, kde klíče jsou jména účtů, a hodnoty jsou příslušné zůstatky
        obsahuje iniciální stav bankovních účtů, které funkce modifikuje
        může být prázdná

Příkazy

    Každý příkaz, kromě příkazu PRINT, vyžaduje právě dva argumenty.
    Předpokládejte, že jak mezi názvem příkazu a prvním argumentem, tak mezi prvním argumentem a druhým argumentem se nachází právě jedna mezera. (poznámka přídána 30. 11.)
    Předpokládejte, že před příkazem ani po příkazu se nenachází žádné bílé znaky kromě znaku nového řádku. (poznámka přídána 30. 11.)
    Pokud program narazí na neznámou instrukci, vypíše Invalid instruction "<jméno příkazu>" on line <číslo řádku>. a ukončí se.
    Pokud program narazí na příkaz s nesprávným počtem argumentů, vypíše: Invalid number of arguments on line <číslo řádku>. a ukončí se.
    Pokud je v popisu řečeno, že příkaz selže, program vypíše: Instruction "<jméno příkazu>" called with an invalid argument on line <číslo řádku>. a ukončí se.
    Kontrola argumentů příkazu probíhá až těsně před jeho provedením.
        Pokud např. třetí příkaz selže, první a druhý příkaz už byly provedeny.
    Pokud je potřeba v příkazu účty seřadit, seřaďte je pouze jednou během vykonávání příkazu (ne po každé transakci).
    Pokud příkaz řadí účty podle jejich jména, řadí je podle operátoru < na řetězcích.
        Intuitivně: Příkaz řadí účty podle jména abecedně (od A po Z). (poznámka přidána 3. 12.)
    Pokud příkaz bere číselný argument, předpokládejte, že dostanete řetězec ve tvaru celého čísla (např.: "42" nebo "-7").
    Všechny výpisy musí být ukončeny znakem nového řádku "\n".

Implementujte následující příkazy:

    CREATE <jméno účtu> <iniciální depozit>
        vytvoří účet se jménem <jméno účtu>
        pokud účet <jméno účtu> již existuje nebo je <iniciální depozit> záporný, příkaz selže
    ADD <jméno účtu> <částka>
        připíše na účet <jméno účtu> částku <částka>
        pokud účet <jméno účtu> neexistuje nebo je <částka> záporná, příkaz selže
    SUB <jméno účtu> <částka>
        strhne z účtu <jméno účtu> částku <částka>
        pokud účet <jméno účtu> neexistuje nebo je <částka> záporná, příkaz selže
    FILTER_OUT <n> <MIN|MAX>
        obdrží-li jako druhý argument řetězec "MIN" smaže <n> nejchudších účtů
        analogicky, obdrží-li jako druhý argument řetězec "MAX" smaže <n> nejbohatších účtů
        pokud je nejchudších/nejbohatších účtů se stejným zůstatkem více, bere je podle jména účtu
        <n> smí být vyšší než celkový počet všech účtů; v takovém případě se smažou všechny
        pokud je <n> záporné nebo je druhý argument něco jiného než "MIN" nebo "MAX", příkaz selže
    AGGREGATE <účet 1> <účet 2>
        přesune celý zůstatek účtu <účet 2> na účet <účet 1> a smaže účet<účet 2>
        pokud <účet 1> nebo <účet 2> neexistuje, příkaz selže
    NATIONALIZE <částka> <n>
        převede z každého z prvních <n> nejbohatších účtů nejvýše částku <částka> na účet STATE
        pokud je zůstatek účtu, ze kterého je prováděn převod, menší než <částka>, ale je kladný, převede se celý na účet STATE (poznámka přidána 4. 12.)
        účet STATE není počítán mezi <n> nejbohatších účtů
        pokud je nejbohatších účtů se stejným zůstatkem více, bere je podle jména účtu
        pokud je <n> vyšší než celkový počet všech účtů, převede částku <částka> z každého účtu pouze jednou
        pokud účet STATE neexistuje, příkaz ho nejprve vytvoří
        pokud je <částka> nebo číslo <n> záporné, příkaz selže
    PRINT
        vypíše stav každého účtu na samostatném řádku v sestupném pořadí dle zůstatku ve formátu:

    <jméno účtu>: <zůstatek>

        účty se stejným zůstatkem vypište seřazené podle jména účtu

Příklad výstupu
Příliš mnoho argumentů

Soubor s příkazy test.txt:

ADD ALICE 500
CREATE BOB 100
CREATE CECIL 450 badf00d
ADD ALICE 1000

Interaktivní příkazová řádka Pythonu:

>>> accounts = {'ALICE': 500}
>>> interpret_file('test.txt', accounts)
Invalid number of arguments on line 3.
>>> print(accounts)
{'ALICE': 1000, 'BOB': 100}

Pokus o vytvoření existujícího účtu

Soubor s příkazy test.txt:

CREATE TEST 150
ADD TEST 50
PRINT

Interaktivní příkazová řádka Pythonu:

>>> accounts = {'TEST': 42}
>>> interpret_file('test2.txt', accounts)

Instruction "CREATE" called with an invalid argument on line 1.
>>> print(accounts)
{'TEST': 42}

Tipy

    Pro načtení obsahu celého souboru můžete využít pomocnou funkci load_file.
    Důkladně zkontrolujte, zda správně vypisujete interpunkci a bílé znaky.

Úloha 2: Chat (4 body)

Analyzujte zprávy chatové konverzace.
Formát zpráv

Zprávy jsou uloženy ve formátu comma-separated values (CSV) (viz tipy pro načtení zpráv ze souboru) (poznámka upřesněna 28. 11.):

<timestamp>,<sender>,<message>

    <timestamp> – POSIXový timestamp – počet sekund od 1. 1. 1970 00:00 v UTC
    <sender> – jméno odesílatele
    <message> – tělo zprávy
    Předpokládejte, že <sender> a <message> obsahují pouze znaky "A" až "Z", "a" až "z", "0" až "9", "-", "_" a " " a že <message> navíc může obsahovat znaky "@". (poznámka upřesněna 30. 11.)

Funkce

Pokud funkce bere jako parametr seznam zpráv, nemůžete předpokládat, že zprávy jsou jakkoli seřazeny. (poznámka přidána 3.12.)

Implementujte následující funkce:

def parse_message(line: str) -> Message

    Rozdělí řetězec line na seznam podřetězců podle znaku "," (čárka) a vrátí hodnotu typu Message.
    Typ Message se shoduje s typem Tuple[datetime, str, str], kde prvky trojice odpovídají zleva doprava <timestamp>, <sender> a <message>.
    První podřetězec převede na datetime (např.: pomocí funkce to_datetime z kostry).
    Podřetězce odpovídající odesílateli a tělu zprávy uloží do trojice beze změny.

def shortest_messages(chat: List[Message], count: int) -> List[Message]

    Vrátí seznam obsahující prvních count nejkratších zpráv z chat seřazený od nejkratší zprávy po nejdelší. (poznámka upřesněna 3. 12.)
    Zachovává pořadí zpráv se stejnou délkou. (Pokud je zpráva a před zprávou b v chat, bude a před b i ve výstupním seznamu.)
    Pokud je zpráv méně než count, vrátí všechny.

def messages_at(chat: List[Message], day: date) -> List[Message]

    Vrátí zprávy odeslány dne day.
    (Datum z hodnoty datetime dostanete pomocí metody date.)
    Pořadí zpráv je zachováno. (Např.: pokud byly zprávy a a b odeslány dne day a a je v seznamu chat před b, bude a před b i ve vráceném seznamu.) (poznámka přidána 6. 12.)

def senders(chat: List[Message]) -> Set[str]

    Vrátí množinu odesílatelů zpráv.

def message_counts(chat: List[Message]) -> Dict[str, int]

    Vytvoří a vrátí slovník, kde klíčem je jméno odesílatele a hodnotou je celkový počet zpráv, které tento odesílatel odeslal.

def mentions(chat: List[Message], user: str) -> List[str]

    Vrátí těla zpráv, která zmiňují uživatele user, ve stejném pořadí, v jakém jsou v chat.
    Zmínce v textu zprávy musí bezprostředně předcházet znak "@". Například zpráva Dobre rano @-kuba-1 zmiňuje uživatele -kuba-1.
    Předpokládejte, že user je neprázdný řetězec. (poznámka přídána 28. 11.)
    Zmínka nemusí být oddělena od zbytku zprávy. Například příklad výše zmiňuje mimo jiné i uživatele -kub. (poznámka přidána 28. 11.)

Tipy

    Pro otestování vašeho řešení na vlastním souboru se zprávami můžete využít pomocnou funkci load_file z úlohy 1 a rozdělit zprávy podle znaku nového řádku "\n". (poznámka upřesněna 28. 11.)
    Hodnoty typů datetime, date i time se dají porovnávat běžnými operátory (např.: <, >=, ==).
    Typ datetime však nelze porovnávat s date, jelikož obsahuje datum i čas. Datum z hodnoty datetime se dostanete pomocí metody date.

Úloha 3: Nejdelší slovo (2 body)

Najděte nejdelší slovo v řetězci tvořené danými znaky.
Znaky a slova

Za alfanumerické znaky považujeme všechna písmena a číslice. V této úloze to budou všechny znaky, pro které funkce isalnum vrátí True.

Slovo je pak nejdelší možná posloupnost alfanumerických znaků.

    To znamená, že např.: v řetězci "A long time ago in a galaxy far, far away..." se nachází tyto slova: "A", "long", "time", "ago", "in", "a", "galaxy", "far", "far", "away"

    Z definice vyplývá, že slova nemusí být nutně oddělena bílými znaky: "text_with_underscores" obsahuje slova: "text", "with", "underscores"

longest_word

Napište funkci longest_word, která nalezne nejdelší slovo podle výše uvedené definice složené z dané množiny znaků.

def longest_word(text: str, provided_letters: Set[str],
                 case_insensitive: bool = False) -> str

    text reprezentuje prohledávaný textový řetězec.
        Pokud je tento řetězec prázdný nebo neobsahuje žádné slovo, funkce vrátí prázdný řetězec.
    provided_letters je množina znaků, ze kterých se hledané slovo smí skládat.
        Předpokládejte, že obsahuje jen řetězce obsahující právě jeden alfanumerický znak.
        Tuto množinu nemodifikujte.
        Pokud je tato množina prázdná, nebo se v řetězci text nenachází slovo sestávající pouze z jejích prvků, funkce vrátí prázdný řetězec.
    case_insensitive – pokud je True, pak při hledání nezáleží na velikosti písmen.
    Vrací nejdelší slovo (resp. slovo maximální délky) složené pouze ze znaků v provided_letters.
    Pokud nalezne více nejdelších slov stejné délky, vrátí první nalezené (při prohledávání zleva doprava).

Příklad výstupu

>>> longest_word("ale, alpha, apple, pea, plea", { "a", "l", "p", "e" })
"apple"

>>> longest_word("Adam went mad.", { "a", "d", "m" })
"mad"

>>> longest_word("Adam went mad.", { "a", "d", "m" }, case_insensitive=True)
"Adam"

Úloha 4: Kontrola závorek (2 body)

Zkontrolujte, zda je řetězec správně uzávorkován.
Správně uzávorkované řetězce

    Za levé závorky považujeme znaky '(', '[' a '{'.
    Za pravé závorky považujeme znaky ')', ']' a '}'.
    Řekneme, že '(' odpovídá ')', '[' odpovídá ']' a '{' odpovídá '}'.
    Každý řetězec, který neobsahuje levé ani pravé závorky, je správně uzávorkovaný.
    Pokud x, y a z jsou správně uzávorkované řetězce, pak x(y)z, x[y]z a x{y}z jsou také správně uzávorkované.
    Žádný jiný řetězec není správně uzávorkovaný.
    Tedy intuitivně:
        Závorky mohou být vnořené (např. v "({[]})").
        Po každé levé závorce se v řetězci (ne nutně bezprostředně) musí nacházet odpovídající pravá závorka.
        Počet levých závorek se musí rovnat počtu pravých závorek.
        Znaky řetězce, které nejsou levými ani pravými závorkami, můžete ignorovat.
        Např.: řetězec "( [ ] ) { }" je správně uzávorkován, zatímco "( [ ) ]" není, jelikož ')' neodpovídá '['.
        Prázdný řetězec je správně uzávorkován.

parentheses_check

Napište funkci parentheses_check, která zkontroluje, zda je řetězec správně uzávorkován:

def parentheses_check(text : str, output: bool = False) -> bool

    text – řetězec, jehož uzávorkování je třeba zkontrolovat
    output – pokud je True a řetězec není správně uzávorkovaný, funkce vypíše na výstup hlášku, která popíše první nalezenou chybu při prohledávaní zleva doprava.
    Vrátí True pokud je výraz správně uzávorkovaný; False pokud není.
    Pokud narazí na chybu v uzávorkování, neprochází zbytek řetězce.

Chybové hlášky

    Do chybových hlášek níže dosaďte:
        za LEVÁ_ZÁVORKA levou závorku, pro niž hledáte pravou závorku,
        za PRAVÁ_ZÁVORKA pravou závorku, kterou jste nalezli,
        za POZICE_LEVÉ_ZÁVORKY index LEVÁ_ZÁVORKA v prohledávaném řetězci,
        za POZICE_PRAVÉ_ZÁVORKY index PRAVÁ_ZÁVORKA v prohledávaném řetězci.
    Pokud nastane chyba v typu nalezené pravé závorky, funkce vypíše chybu: 'LEVÁ_ZÁVORKA' at position POZICE_LEVÉ_ZÁVORKY does not match 'PRAVÁ_ZÁVORKA' at position POZICE_PRAVÉ_ZÁVORKY
    Pokud k pravé závorce neexistuje levá závorka, funkce vypíše chybu: 'PRAVÁ_ZÁVORKA' at position POZICE_PRAVÉ_ZÁVORKY does not have an opening paired bracket
    Pokud k levé závorce neexistuje pravá závorka, funkce vypíše chybu: 'LEVÁ_ZÁVORKA' at position POZICE_LEVÉ_ZÁVORKY does not have a closing paired bracket
        Na tento případ narazíte až po prohledání celého řetězce.
        Pokud existuje více takových levých závorek, vypište pozici té nejpravější.

Příklad výstupu

Funkci lze v interaktivním shellu Pythonu použít takto:

>>> parentheses_check("( ( { } ) ) [ ]")
True

>>> parentheses_check("{ I'm a set. }", output=True)
True

>>> parentheses_check("({)}", output=True)
'{' at position 1 does not match ')' at position 2
False

>>> parentheses_check("()})", output=True)
'}' at position 2 does not have an opening paired bracket
False

(„True“ a „False“ vypisuje interaktivní shell Pythonu.)

>>> parentheses_check("({[[[hey]]]", output=True)
'{' at position 1 does not have a closing paired bracket
False

Tipy

    Může se vám hodit datová struktura zásobník, která byla blíže popsána na 8. přednášce.

"""
