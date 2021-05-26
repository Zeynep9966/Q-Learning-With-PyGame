import random
from tkinter import *

ALFA = 0.1 
GAMA = 0.9

BOYUT = 25
DUVARLAR = set ()

k = random.randint(0,24)
m = random.randint(0,24)
DUVARLAR = {(k,m)}

#duvar belirler
while len(DUVARLAR) != 187:
    k = random.randint(0,24)
    m = random.randint(0,24)
    tut = (k,m)
    DUVARLAR.add(tut)

#duvarları dosyaya yazar
f = open("engel.txt", "w")
for duvar in DUVARLAR:
    print("(", duvar[0], ",", duvar[1], ", K )", file=f)
f.close()

epsilon_basla = 1.00
epsilon_bitir = 0.01

#yönler
YONLER = 8
DIRS = ["W", "E", "D", "C", "X", "Z", "A", "Q"]

ADIM_PUAN = -1.0
BITIRME_PUANI = 100.0

SEED = 12345678

#pygame ayarları
HUCRE_BOYUTU = 20
KENAR_BOYUT = 4
YAZI_BOYUTU = 16
DURUM_BOYUTU = YAZI_BOYUTU*2+5
BEYAZ = (255, 255, 255)
SIYAH = (0,0,0)
MAVI = (0,0,255)
KIRMIZI = (255,0,0)

ADIM_DURAKLAT = 0.5
OGRENME_DURAKLAT = 0.001
EPISODE_DURAKLAT = 0.1

#görselleştirme için
BAYRAK_YOK = 0
DUVAR_BAYRAK = 1
TUZAK_BAYRAK = 2
YOL_BAYRAK = 3
BITIS_BAYRAK = 4
