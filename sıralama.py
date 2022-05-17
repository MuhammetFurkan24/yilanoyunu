# -*- coding: utf-8 -*-

import sqlite3
import atexit

con = sqlite3.connect("./sıralama.db")
cursor = con.cursor()


def sorting():
    try:
        cursor.execute("SELECT * FROM Sıralama")

        data = cursor.fetchall()

        if len(data) == 0:
            raise sqlite3.Error

        for i in range(len(data) - 1):  # Sorting Algorithm (Bubble Sort)
            for j in range(len(data) - (i + 1)):
                if data[j][1] < data[j+1][1]:  # Skor
                    t = data[j]
                    data[j] = data[j+1]
                    data[j+1] = t
                if data[j][1] == data[j+1][1] and data[j][2] > data[j+1][2]:
                    t = data[j]
                    data[j] = data[j + 1]
                    data[j + 1] = t

        print("[*] Sıralama:\n")
        a = 1
        for i in (data if len(data) <= 10 else data[0:10]):  # Type(i) = Tuple
            print((f"{a}.   " if a != 10 else f"{a}.  ") + str(int(i[1])) + " Puan " +
                  " " * (3 - (len(list(str(i[1]))) - 4)) + "|  " + str(i[2]) + f" dk\t[ {i[3]} ]")
            a += 1

    except sqlite3.OperationalError as _err:
        print(f"[!] Tablo bulunamadı. Silinmiş veya değiştirilmiş olabilir.\n <{_err}>")

    except sqlite3.Error:
        print(f"[!] Hiç oyun kaydı bulunamadı.\n")


def del_table():
    cursor.execute("DROP TABLE Sıralama")


if __name__ == '__main__':
    sorting()
    con.close()
    atexit.register(input, '\nPress enter the continue')
