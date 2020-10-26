# https://python101.readthedocs.io/pl/latest/index.html
# https://github.com/koduj-z-klasa/python101
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from peewee import *
from dane_my import pobierz_dane

#from ormpw import Klasa , Uczen

"""
if os.path.exists('test.db'):
	os.remove('test.db')
"""
# tworzymy instancję bazy używanej przez modele
baza = SqliteDatabase('test.db')  # ':memory:'


class BazaModel(Model):  # klasa bazowa
	class Meta:
		database = baza


# klasy Klasa i Uczen opisują rekordy tabel "klasa" i "uczen"
# oraz relacje między nimi


class Klasa(BazaModel):
	nazwa = CharField(null=False)
	profil = CharField(default='')


class Uczen(BazaModel):
	imie = CharField(null=False)
	nazwisko = CharField(null=False)
	klasa = ForeignKeyField(Klasa, related_name='uczniowie')

baza.connect()  # nawiązujemy połączenie z bazą
#baza.create_tables([Klasa, Uczen])  # tworzymy tabele

# zamiana tuple na listę dict aby dodać do bazy
pobrane = pobierz_dane('uczniowie.csv')
pola = ['imie','nazwisko','klasa_id']
uczniowie = [dict(zip(pola, d)) for d in pobrane]


# dodajemy dane wielu uczniów
Uczen.insert_many(uczniowie).execute()


# odczytujemy dane z bazy


def czytajdane():
	for uczen in Uczen.select().join(Klasa):
		print(uczen.id, uczen.imie, uczen.nazwisko, uczen.klasa.nazwa, uczen.klasa.profil)
	print()


czytajdane()

baza.close()
