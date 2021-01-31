import random
import sqlite3

class Bank:
    def create(self, n):
        random.seed()
        s1 = str(random.randrange(0, 10 ** 9)).zfill(9)
        num = 8
        for i in range(9):
            if (i + 1) % 2 == 1:
                num1 = int(s1[i]) * 2
                if num1 > 9:
                    num1 = num1 - 9
                num = num + num1
            else:
                num = num + int(s1[i])
        s1 = "400000" + s1 + str((10 - num % 10) % 10)
        s2 = str(random.randrange(0, 10 ** 4)).zfill(4)
        print("\nYour card number:", s1, "Your card PIN:", s2, sep = '\n')
        cur.execute("INSERT INTO card(id, number, pin) VALUES ({}, {}, {})".format(n, s1, s2))
        conn.commit()
    def show(self):
        print("\nEnter your card number:")
        s1 = input()
        print("Enter your PIN:")
        s2 = input()
        cur.execute("SELECT number, pin, balance FROM card WHERE number = {}".format(s1))
        card = cur.fetchone()
        if card is not None:
            card_num, card_pin, card_balance = [i for i in card]
            card_pin = "0" * (4 - len(card_pin)) + card_pin
            if card_num == s1:
                if card_pin == s2:
                    print("\nYou have successfully logged in!\n")
                    flag = 1
                    while flag == 1:
                        print("1. Balance","2. Add income", "3. Do transfer", "4. Close account", "5. Log out", "0. Exit", sep = '\n')
                        num = input()
                        if num == "1":
                            print("\nBalance: {}\n".format(card_balance))
                        elif num == "2":
                            income = int(input("\nEnter income:\n"))
                            card_balance += income
                            cur.execute("UPDATE card SET balance = {} WHERE number = {}".format(card_balance, card_num))
                            conn.commit()
                            print("Income was added!\n")
                        elif num == "3":
                            transfer = input("\nTransfer\nEnter card number:\n")
                            num = 0
                            if s1 == transfer:
                                print("\nYou can't transfer money to the same account!\n")
                                continue
                            for i in range(15):
                                if (i + 1) % 2 == 1:
                                    num1 = int(transfer[i]) * 2
                                    if num1 > 9:
                                        num1 = num1 - 9
                                    num = num + num1
                                else:
                                    num = num + int(transfer[i])
                            num += int(transfer[15])
                            if num % 10 != 0:
                                print("Probably you made a mistake in the card number. Please try again!\n")
                                continue
                            cur.execute("SELECT number FROM card WHERE number = {}".format(transfer))
                            card_transfer = cur.fetchone()
                            if card_transfer is None:
                                print("Such a card does not exist.\n")
                                continue
                            else:
                                print("Enter how much money you want to transfer:")
                                num_t = int(input())
                                if num_t > card_balance:
                                    print("Not enough money!\n")
                                else:
                                    card_balance -= num_t
                                    cur.execute("UPDATE card SET balance = {} WHERE number = {}".format(card_balance, card_num))
                                    cur.execute("UPDATE card SET balance = {} WHERE number = {}".format(num_t, transfer))
                                    conn.commit()
                                    print("\nSuccess!\n")
                        elif num == "4":
                            cur.execute("DELETE FROM card WHERE number = {}".format(s1))
                            conn.commit()
                            print("\nThe account has been closed!\n")
                            return 1
                        elif num == "5":
                            return 1
                        else:
                            return 0
                else:
                    print("\nWrong card number or PIN!")
                    return 1
            else:
                print("\nWrong card number or PIN!")
                return 1
        else:
            print("\nWrong card number or PIN!")
            return 1

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS card(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
conn.commit()
flag = 1
card = Bank()
n = 0
while flag == 1:
    print("\n1. Create an account", "2. Log into account", "0. Exit", sep = '\n')
    s1 = input()
    if s1 == "1":
        card.create(n)
        n = n + 1
    elif s1 == "2":
        flag = card.show()
    else:
        flag = 0
print("\nBey!")
