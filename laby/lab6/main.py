import numpy as np
from PIL import Image
import random

def stworz_udzialy(sciezka_do_obrazu):
    img = Image.open(sciezka_do_obrazu).convert('1')
    img = img.resize((100, 100))
    piksele = np.array(img)

    wysokosc, szerokosc = piksele.shape
    
   
    udzial1 = np.zeros((wysokosc, szerokosc * 2), dtype=np.uint8)
    udzial2 = np.zeros((wysokosc, szerokosc * 2), dtype=np.uint8)

    for y in range(wysokosc):
        for x in range(szerokosc):
            jest_bialy = piksele[y, x] # Zwraca True jeśli biały, False jeśli czarny
            
            wzorzec = random.choice([0, 1])
            
            if jest_bialy:
                if wzorzec == 0:
                    u1_lewy, u1_prawy = 0, 255
                    u2_lewy, u2_prawy = 0, 255
                else:
                    u1_lewy, u1_prawy = 255, 0
                    u2_lewy, u2_prawy = 255, 0
            else:
                if wzorzec == 0:
                    u1_lewy, u1_prawy = 0, 255
                    u2_lewy, u2_prawy = 255, 0
                else:
                    u1_lewy, u1_prawy = 255, 0
                    u2_lewy, u2_prawy = 0, 255

            udzial1[y, x*2], udzial1[y, x*2+1] = u1_lewy, u1_prawy
            udzial2[y, x*2], udzial2[y, x*2+1] = u2_lewy, u2_prawy

    Image.fromarray(udzial1, mode='L').save('udzial_1.png')
    Image.fromarray(udzial2, mode='L').save('udzial_2.png')

    zlozenie = np.minimum(udzial1, udzial2)
    Image.fromarray(zlozenie, mode='L').save('zlozenie_wynik.png')
    

if __name__ == "__main__":
    stworz_udzialy('test.png')

