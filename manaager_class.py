import os



class Manager:
    def __init__(self):
        self.saldo = 10000
        self.magazyn = {
            "Łódka": {"stan magazynu(sztuk)": 4, "cena": 1500},
            "Wędka": {"stan magazynu(sztuk)": 8, "cena": 400},
            "Przynęta": {"stan magazynu(sztuk)": 200, "cena": 15}
        }
        self.historia_operacji = self.odczytaj_historie_operacji()
        self.saldo_dodaj_odejmij = False
        self.historia_operacji = self.odczytaj_historie_operacji() or []
        self.actions = self.assign()

    def assign(self):
        return {
            "saldo": self.wyswietl_saldo,
            "dodaj saldo": self.modyfikuj_saldo_dodaj,
            "odejmij saldo": self.modyfikuj_saldo_odejmij,
            "sprzedaż": self.zarejestruj_sprzedaz,
            "zakup": self.zarejestruj_zakup,
            "konto": self.wyswietl_konto,
            "lista": self.historia_operacji_wyswietl,
            "stan magazynu": self.wyswietl_magazyn,
            "przegląd": self.przeglad
        }

    def execute(self, komenda):
        action = self.actions.get(komenda)
        if action:
            action()
        else:
            print("Niepoprawna komenda. Spróbuj ponownie.")

            if komenda == "saldo":
                self.wyswietl_saldo()
            elif komenda == "dodaj saldo":
                self.modyfikuj_saldo("dodaj saldo")
            elif komenda == "odejmij saldo":
                self.modyfikuj_saldo("odejmij saldo")
            elif komenda == "sprzedaż":
                self.zarejestruj_sprzedaz()
            elif komenda == "zakup":
                self.zarejestruj_zakup()
            elif komenda == "konto":
                self.wyswietl_konto()
            elif komenda == "lista":
                self.historia_operacji_wyswietl()
            elif komenda == "stan magazynu":
                self.wyswietl_magazyn()
            elif komenda == "przeglad":
                self.przeglad()
            else:
                print("Niepoprawna komenda. Spróbuj ponownie.")


    def zarejestruj_zakup(self):
        produkt = input("Podaj nazwę zakupionego produktu: ")
        cena = float(input("Podaj cenę produktu (PLN): "))
        ilosc = int(input("Podaj ilość zakupionych produktów: "))
        kwota_zakupu = cena * ilosc
        self.saldo -= kwota_zakupu
        if produkt in self.magazyn:
            self.magazyn[produkt]["stan magazynu(sztuk)"] += ilosc
        else:
            print("Produkt nie istnieje w magazynie. Dodano nowy produkt.")
            self.magazyn[produkt] = {"stan magazynu(sztuk)": ilosc, "cena": cena}
        operacja = f"Zakup: {ilosc} sztuk {produkt} za {kwota_zakupu} PLN"
        self.historia_operacji.append(operacja)
        self.zapisz_magazyn()
        print(f"Zarejestrowano zakup {ilosc} sztuk {produkt} za {kwota_zakupu} PLN")

    def historia_operacji_wyswietl(self):
        print("Historia operacji:")
        for operacja in self.historia_operacji:
            print(operacja)

    def wyswietl_magazyn(self):
        print("Stan magazynu:")
        for produkt, dane in self.magazyn.items():
            print(f"{produkt}: Stan magazynu: {dane['stan magazynu(sztuk)']} sztuk, Cena: {dane['cena']} PLN/sztuka")

    def wyswietl_konto(self):
        print(f"Saldo konta firmy: {self.saldo} PLN")
        print("Szczegóły konta firmy:")
        for produkt, dane in self.magazyn.items():
            print(f"{produkt}: Stan magazynu: {dane['stan magazynu(sztuk)']} sztuk, Cena: {dane['cena']} PLN/sztuka")

    def zarejestruj_sprzedaz(self):
        try:
            produkt = input("Podaj nazwę sprzedawanego produktu: ")
            cena = float(input("Podaj cenę produktu (PLN): "))
            ilosc = int(input("Podaj ilość sprzedanych produktów: "))
            kwota_sprzedazy = cena * ilosc
            self.saldo += kwota_sprzedazy
            operacja = f"Sprzedaż: {ilosc} sztuk {produkt} za {kwota_sprzedazy} PLN"
            self.historia_operacji.append(operacja)
            self.zapisz_operacje(operacja)
            self.zapisz_saldo_do_pliku()
            print(f"Zarejestrowano sprzedaż {ilosc} sztuk {produkt} za {kwota_sprzedazy} PLN")
        except ValueError:
            print("Wprowadzono niepoprawne dane. Spróbuj ponownie.")

    def przeglad(self):
        self.historia_operacji_wyswietl()
        self.wyswietl_konto()
        self.wyswietl_magazyn()

    def zapisz_saldo_do_pliku(self):
        try:
            with open("saldo_magazyn.txt", "w") as file:
                file.write(f"Saldo twojego konta wynosi: {self.saldo} PLN\n")
            print("Saldo zostało zapisane do pliku saldo_magazyn.txt.")
        except Exception as e:
            print(f"Wystąpił błąd podczas zapisywania salda: {str(e)}")

    def zapisz_magazyn(self):
        try:
            with open("magazyn.txt", "w") as file:
                for produkt, dane in self.magazyn.items():
                    file.write(
                        f"{produkt}: Stan magazynu: {dane['stan magazynu(sztuk)']} sztuk, Cena: {dane['cena']} PLN/sztuka\n")
        except Exception as e:
            print(f"Błąd podczas zapisu magazynu: {e}")

    def odczytaj_saldo(self):
        try:
            if os.path.exists("saldo_magazyn.txt"):
                with open("saldo_magazyn.txt", "r") as saldo_file:
                    self.saldo = float(saldo_file.read())
            else:
                print("Plik saldo_magazyn.txt nie istnieje.")
                self.saldo = None
        except Exception as e:
            print(f"Błąd odczytu salda: {e}")

    def zapisz_operacje(self, operacja):
        try:
            with open("historia_operacji.txt", "a") as historia_file:
                historia_file.write(f"{operacja}\n")
        except Exception as e:
            print(f"Błąd podczas zapisu operacji: {e}")

    def odczytaj_historie_operacji(self):
        try:
            if os.path.exists("historia_operacji.txt"):
                with open("historia_operacji.txt", "r") as historia_file:
                    return [line.strip() for line in historia_file.readlines()]
            else:
                print("Plik historia_operacji.txt nie istnieje.")
        except Exception as e:
            print(f"Błąd odczytu historii operacji: {e}")
        return []

    def wyswietl_saldo(self):
        print(f"Aktualne saldo konta firmy wynosi: {self.saldo} PLN")

    def modyfikuj_saldo(self, operacja):
        if not self.saldo_dodaj_odejmij:
            print("Nie można modyfikować salda.")
            return

        kwota = float(input("Podaj kwotę (PLN): "))
        if operacja == "dodaj saldo":
            self.saldo += kwota
            print("Saldo zostało zaktualizowane i wynosi", self.saldo)
        elif operacja == "odejmij saldo":
            if kwota <= self.saldo:
                self.saldo -= kwota
                print("Saldo zostało zaktualizowane i wynosi", self.saldo)
            else:
                print("Brak wystarczających środków na koncie.")
        else:
            print("Niepoprawna operacja.")

    def modyfikuj_saldo_dodaj(self):
            self.modyfikuj_saldo("dodaj saldo")

    def modyfikuj_saldo_odejmij(self):
            self.modyfikuj_saldo("odejmij saldo")



