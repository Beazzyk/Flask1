from manaager_class import Manager




def dostepne_komendy(manager):
    komendy = ["saldo", "sprzedaż", "zakup", "konto", "lista", "stan magazynu", "przeglad", "koniec"]
    if manager.saldo_dodaj_odejmij:
        komendy.extend(["dodaj saldo", "odejmij saldo"])
    return komendy


def main():
    manager = Manager()
    while True:
        wszystkie_komendy = dostepne_komendy(manager)
        for komenda in wszystkie_komendy:
            print(komenda)

        komenda = input("Podaj komendę: ").strip().lower()
        if komenda == "koniec":
            break
        else:
            manager.execute(komenda)


if __name__ == "__main__":
    main()