from PIL import Image

def ukryj_wiadomosc(sciezka_wejsciowa, wiadomosc, sciezka_wyjsciowa):
    img = Image.open(sciezka_wejsciowa)
    img = img.convert('RGB')
    piksele = list(img.get_flattened_data())
    
    # 2. Konwertujemy wiadomość na ciąg bitów.
    # Dodajemy znacznik "#####", aby wiedzieć, gdzie kończy się tekst.
    wiadomosc += "#####"
    bity_wiadomosci = ''.join([format(ord(znak), '08b') for znak in wiadomosc])
    
    # Sprawdzamy czy obraz pomieści naszą wiadomość
    if len(bity_wiadomosci) > len(piksele) * 3:
        raise ValueError("Wiadomość jest zbyt długa, aby ukryć ją w tym obrazku!")

    nowe_piksele = []
    indeks_bitu = 0
    
    for piksel in piksele:
        r, g, b = piksel
        nowy_piksel = [r, g, b]
        
        for i in range(3):
            if indeks_bitu < len(bity_wiadomosci):
                nowy_piksel[i] = (nowy_piksel[i] & ~1) | int(bity_wiadomosci[indeks_bitu])
                indeks_bitu += 1
                
        nowe_piksele.append(tuple(nowy_piksel))
        
    img_ukryte = Image.new(img.mode, img.size)
    img_ukryte.putdata(nowe_piksele)
    img_ukryte.save(sciezka_wyjsciowa, format="PNG")
    print(f"Pomyślnie ukryto wiadomość. Zapisano jako: {sciezka_wyjsciowa}")

def odczytaj_wiadomosc(sciezka_wejsciowa):
    img = Image.open(sciezka_wejsciowa)
    img = img.convert('RGB')
    piksele = list(img.get_flattened_data())
    
    bity_odczytane = ""
    ukryta_wiadomosc = ""
    
    for piksel in piksele:
        r, g, b = piksel
        bity_odczytane += str(r & 1)
        bity_odczytane += str(g & 1)
        bity_odczytane += str(b & 1)
        
    bity_na_bajty = [bity_odczytane[i:i+8] for i in range(0, len(bity_odczytane), 8)]
    
    for bajt in bity_na_bajty:
        if len(bajt) == 8:
            znak = chr(int(bajt, 2))
            ukryta_wiadomosc += znak
            
            if ukryta_wiadomosc.endswith("#####"):
                return ukryta_wiadomosc[:-5]

    return "Nie znaleziono wiadomości lub obraz jest uszkodzony."

if __name__ == "__main__":
    ukryj_wiadomosc('test.png', 'Ukryta wiadomość', 'test_tajny.png')
    
    odzyskany_tekst = odczytaj_wiadomosc('test_tajny.png')
    print("Odzyskany tekst:", odzyskany_tekst)
    pass