import sqlite3
from contextlib import contextmanager
from itertools import product, combinations
from math import factorial, comb, prod


def pro_1(n, r):
    return factorial(r)/factorial(n)


@contextmanager
def closing(thing):
    try:
        yield thing
    finally:
        thing.close()


def fac(r, n, end):
    end -= 1
    return (r/n) * end * (r-1/n)


if __name__ == '__main__':
    deck = product(range(2, 15), 'cdrs')
    deck_str = ["".join([str(card[0]) + card[1]]) for card in deck]

    combos = combinations(deck_str, 5)
    # c = combinations(range(5), 3)

    with closing(sqlite3.connect('db.sqlite3')) as conn:

        cursor: sqlite3.Cursor = conn.cursor()
        # for card in deck:
        #     card_id = str(card[0]) + str(card[1])
        #     cursor.execute("""
        #     INSERT INTO card (id, nominal, suit) VALUES (?, ?, ?)
        #     """, (card_id, card[0], card[1]))
        # conn.commit()
        # for combo in combos:
        #     print(''.join(combo))
        #     cursor.execute("""
        #     INSERT INTO CombosFive (id) VALUES (?)
        #     """, ("".join(combo),))
        # conn.commit()
