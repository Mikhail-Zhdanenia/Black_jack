# Black_jack

import random


class Deck():
    """Класс в котором реализована колода карт и метод выбора карты """

    deck_cards = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2'] * 4

    # колода из 42 карт

    def pick(self, num):
        picked = []
        for _ in range(num):
            choosen = random.randint(0, len(self.deck_cards) - 1)
            picked.append(self.deck_cards[choosen])

            self.deck_cards.pop(choosen)

        return picked


class Player(Deck):
    """Класс игрока, с деньгами, картами и состоянием победы или проигрыша"""

    cards = []
    burst = False

    def __init__(self):
        self.money = 500


class Dealer(Deck):
    """Класс компьютера"""

    cards = []
    burst = False


# Функции

def print_cards(cards):
    """отрисовка карт """

    for i in range(len(cards)):
        print("{0:^4}-----".format(''))
        print("{0:^4}|{1:^3}|".format('', cards[i]))
        print("{0:^4}-----".format(''))


def print_board(cards1, cards2):
    """отрисовка игрового поля"""

    print("\n" * 50)
    print("*************")
    print("Player cards:")
    print("*************")
    print_cards(cards1)
    print("*************")
    print("Dealer cards:")
    print("*************")
    print_cards(cards2)
    print("*************")


def find_value(cards):
    """значения карт"""

    card_value = []
    total = 0
    ace = False
    value_dict = {'A': 11, 'K': 10, 'Q': 10, 'J': 10, '10': 10,
                  '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2, }

    # подсчет значений карт
    for i in range(len(cards)):
        card_value.append(value_dict[cards[i]])
        if cards[i] == 'A':
            ace = True

    for i in range(len(card_value)):
        total += card_value[i]

    # проверка перебора и применение туза в значении 1

    if total > 21 and ace:
        total -= 10

    return total


# GAMEPLAY

p1 = Player()
d1 = Dealer()

while True:
    p1.cards = p1.pick(2)
    d1.cards = d1.pick(1)

    dealer_won = False

    print_board(p1.cards, d1.cards)

    # Проверка ставки
    while True:
        try:
            bet = int(input("Enter the amount of money you want to bet: "))
            if bet > p1.money:
                print("You dont have sufficient funds!")
                print("Your account balance is: {}".format(p1.money))
                raise ValueError
            break
        except ValueError as e:
            print("Please enter a valid amount!")

    p1.money -= bet

    # игрок выбирает карту до тех пор пока не проиграет или не пропустит
    while True:

        while True:
            try:
                choice = input("Do you want to hit or pass? [h/p]: ")
                if choice.lower() not in ['h', 'p']:
                    raise NameError
                break
            except NameError as e:
                print("Oops! Please enter a valid choice")

        if choice.lower() == 'h':
            p1.cards += p1.pick(1)
            print_board(p1.cards, d1.cards)
        else:
            break

        if find_value(p1.cards) > 21:
            p1.burst = True
            dealer_won = True
            break

    # Компьютер играет
    if not dealer_won:
        while True:
            d1.cards += d1.pick(1)
            if find_value(d1.cards) > 21:
                d1.burst = True
                break

            if find_value(d1.cards) > find_value(p1.cards):
                dealer_won = True
                break

    print("\n" * 50)
    print_board(p1.cards, d1.cards)

    # Определение победителя и вывод результата
    if dealer_won:
        print("_" * 50)
        print("Sorry you lost the game and the money.")
        if p1.burst:
            print("Your cards value exceeded 21. Be careful next time!")
            print("_" * 50)
        else:
            print("Dealer got very lucky! Better luck next time! :)")
            print("_" * 50)
    else:
        p1.money += 3 * bet
        print("_" * 67)
        print("Bingo! You won the game! Twice the bet is credited to your account.")
        if d1.burst:
            print("Dealer's total card value exceeded 21. You got lucky, well played!")
            print("_" * 67)

    print("Your account balance is: {}".format(p1.money))

    while True:
        try:
            play_again = input("Do you want to play again? [y/n]: ")
            if play_again.lower() not in ['y', 'n']:
                raise NameError
            break
        except NameError as e:
            print("Oops! Please enter a valid choice")

    if play_again == 'n':
        break
    elif p1.money == 0:
        print("You did not have sufficient to continue playing!")
