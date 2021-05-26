from dataclasses import dataclass
from tkinter import *
from matplotlib import pyplot as plt
import numpy as np
import pygame
import sys
import time
from ayarlar import *


def durum(x,y):
    #hücre sayısını döndürür
    return x+y*BOYUT

@dataclass
class Pos:
    #pozisyon koordinatları
    x: int
    y: int

def main():
    np.random.seed(SEED) # PRNG etkinleştir
    episode_max = int(input("Max Episode sayısı: "))
    q = np.empty((YONLER, BOYUT*BOYUT), dtype= float) # q tablosu oluştur
    q[:] = 0.0 # q tablosu elemanlarının başlatılması
    reward_listesi = []
    adim_listesi = []
    
    def secim():
        secimPaneli = Tk()
        secimPaneli.title('Seçim')
        secimPaneli.geometry('300x200')
        secimPaneli.resizable(width = FALSE, height = FALSE)
        text1 = Text(secimPaneli, height = 1, width=10)
        text2 = Text(secimPaneli, height = 1, width=10)
        label1 = Label(secimPaneli, text = "Başlangıç noktası")
        label1.config(font =("Calibra", 14))
        label2 = Label(secimPaneli, text = "Bitiş noktası")
        label2.config(font =("Calibra", 14))

        def girdiAl():
            result1=text1.get("1.0","end")
            list1 = result1.split(',')
            result2=text2.get("1.0","end")
            list2 = result2.split(',')
            X_BASLA = int(list1[0])
            Y_BASLA = int(list1[1])
            X_BITIR = int(list2[0])
            Y_BITIR = int(list2[1])
            for duvar in DUVARLAR:
                if (X_BASLA == int(duvar[0]) ):
                    if(Y_BASLA == int(duvar[1])):
                        print("Duvar: ", duvar)
                        quit()
                elif (X_BITIR == int(duvar[0]) ):
                    if(Y_BITIR == int(duvar[1])):
                        print("duvar: ", duvar)    
                        quit()
            
            def yon(x, y, a):
                #yeni pozisyon hesapla
                bonus = ADIM_PUAN 
                bayrak = BAYRAK_YOK #resetle

                #delta başlat
                dx = 0
                dy = 0
                if(a == 0): #Kuzey
                    if( y > 0):
                        dy = -1
                elif (a == 1): # kuzeydoğu
                    if ((y > 0) and (x < (BOYUT-1))):
                        dy = -1
                        dx = 1
                elif (a == 2): # doğu
                    if (x < (BOYUT-1)):
                        dx = 1
                elif (a == 3): # güneydoğu 
                    if ((y < (BOYUT-1)) and (x < (BOYUT-1))):
                        dy = 1
                        dx = 1
                elif (a == 4): # güney
                    if (y < (BOYUT-1)):
                        dy = 1
                elif (a == 5): # güneybatı
                    if ((y < (BOYUT-1)) and (x > 0)):
                        dy = 1
                        dx = -1
                elif (a == 6): # batı
                    if (x > 0):
                        dx = -1
                elif (a == 7): # kuzeybatı
                    if ((y > 0) and (x >0)):
                        dy = -1
                        dx = -1
                if ((dx == 0) and (dy == 0)): # yol
                    bayrak = YOL_BAYRAK
                if ((x+dx, y+dy) in DUVARLAR): # duvar
                    dx = 0
                    dy = 0
                    bayrak = DUVAR_BAYRAK
                    #bonus -=5
                
                #bonus hesapla
                if (x+dx) == X_BITIR and (y+dy) == Y_BITIR:
                    bonus = bonus + BITIRME_PUANI
                    bayrak = BITIS_BAYRAK
                return dx, dy, bonus, bayrak
            
            pygame.init() #oyunu başlat
            pygame.display.set_caption("Q-learning ile Yol Planlaması")
            
            canvas = pygame.display.set_mode((BOYUT*HUCRE_BOYUTU+(BOYUT-1)*KENAR_BOYUT, BOYUT*HUCRE_BOYUTU+(BOYUT-1)*KENAR_BOYUT+DURUM_BOYUTU))
            canvas.fill(BEYAZ)
            font = pygame.font.SysFont("comicsansms", YAZI_BOYUTU)
            #resimleri yükle
            ikon = pygame.image.load("yuru.png")
            ayakizi = pygame.image.load("ayakizi.png")
            duvar_foto = pygame.image.load("duvar_foto.png")
            kutu = pygame.image.load("kutu.png")
            basla = pygame.image.load("basla.png")
            bitir = pygame.image.load("bitis.png")
            yuru = pygame.image.load("yuru.png")

            ikon.convert()
            pygame.display.set_icon(ikon) #sayfa ikonu belirle
            ayakizi.convert()
            duvar_foto.convert()
            kutu.convert()
            basla.convert()
            bitir.convert()
            yuru.convert()

            # hücreleri çiz
            i = 1
            while(i<BOYUT):
                pygame.draw.line(canvas, SIYAH, (i*HUCRE_BOYUTU + (i-1)*KENAR_BOYUT+1,0), (i*HUCRE_BOYUTU + (i-1)*KENAR_BOYUT + 1, BOYUT*HUCRE_BOYUTU + (BOYUT-1)*KENAR_BOYUT-1), KENAR_BOYUT)
                i+=1
            i = 1
            while (i < BOYUT):
                pygame.draw.line(canvas, SIYAH, (0, i * HUCRE_BOYUTU + (i-1) * KENAR_BOYUT + 1), (BOYUT*HUCRE_BOYUTU+(BOYUT-1)*KENAR_BOYUT - 1, i * HUCRE_BOYUTU + (i-1) * KENAR_BOYUT + 1), KENAR_BOYUT)
                i += 1
            episode = 0 # episode resetle
            for episode in  range(episode_max):
            #while (episode < episode_max): # episode döngüsü
                #epsilon hesapla
                if (episode == (episode_max-1)):
                    #son episode
                    epsilon = 0.0
                else:
                    epsilon = ((episode_max-1) - episode)/(episode_max - 1) *(epsilon_basla-epsilon_bitir) + epsilon_bitir
                #print("EPSILON: ", format(epsilon, '.2f')) 
                i = 0
                while (i<BOYUT):
                    j = 0
                    while (j<BOYUT):
                        canvas.blit(kutu, (j*(HUCRE_BOYUTU+KENAR_BOYUT) , i*(HUCRE_BOYUTU+KENAR_BOYUT)))
                        j += 1
                    i += 1
                #duvarları çiz
                for duvar in DUVARLAR:
                    canvas.blit(duvar_foto, (duvar[0]*(HUCRE_BOYUTU+KENAR_BOYUT) , duvar[1]*(HUCRE_BOYUTU+KENAR_BOYUT)))
                
                moving = True # bayrak hareketi
                pos = Pos(X_BASLA, Y_BASLA) # pozisyon başlat
                canvas.blit(yuru, (pos.x*(HUCRE_BOYUTU+KENAR_BOYUT) , pos.y*(HUCRE_BOYUTU+KENAR_BOYUT))) # ajanı çiz
                f = BAYRAK_YOK
                adim = 0 # adim sıfırla
                skor = 0.0 # reward skor resetle
                canvas.blit(bitir, (X_BITIR*(HUCRE_BOYUTU+KENAR_BOYUT) , Y_BITIR*(HUCRE_BOYUTU+KENAR_BOYUT))) # bitiş konumu

                while (moving):
                    pygame.event.pump()
                    # çizim
                    canvas.blit(kutu, (pos.x*(HUCRE_BOYUTU+KENAR_BOYUT) , pos.y*(HUCRE_BOYUTU+KENAR_BOYUT)))
                    canvas.blit(yuru, (pos.x*(HUCRE_BOYUTU+KENAR_BOYUT) , pos.y*(HUCRE_BOYUTU+KENAR_BOYUT)))
                    canvas.fill(BEYAZ, pygame.Rect(0, BOYUT*HUCRE_BOYUTU+BOYUT*KENAR_BOYUT, BOYUT*HUCRE_BOYUTU+(BOYUT-1)*KENAR_BOYUT, DURUM_BOYUTU))
                    text = font.render("E:"+str(episode + 1),True,(MAVI))
                    canvas.blit(text,(1, BOYUT*HUCRE_BOYUTU+BOYUT*KENAR_BOYUT+5))
                    text = font.render("S:"+str(adim),True,(MAVI))
                    canvas.blit(text,((BOYUT*HUCRE_BOYUTU+BOYUT*KENAR_BOYUT) // 5, BOYUT*HUCRE_BOYUTU+BOYUT*KENAR_BOYUT+5))
                    text = font.render("X:"+str(pos.x)+" Y:"+str(pos.y),True,(MAVI))
                    canvas.blit(text,((BOYUT*HUCRE_BOYUTU+BOYUT*KENAR_BOYUT) * 2 // 5, BOYUT*HUCRE_BOYUTU+BOYUT*KENAR_BOYUT+5))
                    text = font.render(format(skor, '.2f'),True,(KIRMIZI))
                    canvas.blit(text,((BOYUT*HUCRE_BOYUTU+BOYUT*KENAR_BOYUT) * 3 // 5, BOYUT*HUCRE_BOYUTU+BOYUT*KENAR_BOYUT+5))
                    if ((episode == (episode_max-1)) and ((f == YOL_BAYRAK) or (f == DUVAR_BAYRAK))):
                        text = font.render("LOCK",True,(KIRMIZI))
                        canvas.blit(text,((BOYUT*HUCRE_BOYUTU+BOYUT*KENAR_BOYUT) *4 // 5, BOYUT*HUCRE_BOYUTU+BOYUT*KENAR_BOYUT+5))
                        pygame.display.flip() # display update
                        print("LOCK") # total scores
                        break
                    if (f==BITIS_BAYRAK): #Bitise geldiyse
                        #optimal yol
                        i = 0
                        while (i < BOYUT*BOYUT):
                            zero = True
                            # keşfedilen ilk yeri ara
                            j = 0
                            while (j < YONLER):
                                if (q[j, i] !=  0.0):
                                    zero = False # keşfedilen yer bulundu
                                    break
                                j += 1 # sıradaki hareket
                            if (zero == False): # keşfedilen yer çıkış 
                                max = q[j, i] # mevcut max q 
                                k = j # mevcut optimal hareket
                                j += 1 # sıradaki hareket
                                while (j < YONLER):
                                    # kontrol et
                                    if (q[j, i] !=  0.0):
                                        # max al
                                        if (q[j, i] > max):
                                            max = q[j, i] # yeni max q değeri
                                            k = j # yeni optimal yol
                                    j += 1 # sıradaki hareket
                                print(DIRS[k], end = '')
                            else:
                                print("-", end = '')
                            i += 1
                            if ((i % BOYUT) == 0):
                                print("")
                        text = font.render("BİTTİ",True,(MAVI))
                        canvas.blit(text,((BOYUT*HUCRE_BOYUTU+BOYUT*KENAR_BOYUT) *4 // 5, BOYUT*HUCRE_BOYUTU+BOYUT*KENAR_BOYUT+5))
                        pygame.display.flip() # güncelle
                        #print("SKOR = " + format(skor, '.2f')) # total skor
                        
                        #time.sleep(EPISODE_DURAKLAT)
                        break
                    if (f == DUVAR_BAYRAK):
                        text = font.render("DUVAR",True,(KIRMIZI))
                        canvas.blit(text,((BOYUT*HUCRE_BOYUTU+BOYUT*KENAR_BOYUT) *4 // 5, BOYUT*HUCRE_BOYUTU+BOYUT*KENAR_BOYUT+5))
                
                    elif (f == YOL_BAYRAK):
                        text = font.render("YOL",True,(KIRMIZI))
                        canvas.blit(text,((BOYUT*HUCRE_BOYUTU+BOYUT*KENAR_BOYUT) *4 // 5, BOYUT*HUCRE_BOYUTU+BOYUT*KENAR_BOYUT+5))
                    pygame.display.flip() # güncelle
                    pygame.event.pump()

                    if (episode == (episode_max-1)):
                        time.sleep(ADIM_DURAKLAT) # adımı duraklat
                    #else:
                        #time.sleep(OGRENME_DURAKLAT) # öğrenmeyi duraklat
                    # random strateji seçimi
                    if (np.random.rand() < epsilon):
                        # keşfet
                        a = np.random.randint(0, YONLER)
                    else:
                        zero = True
                        # ilk blunan non degil
                        j = 0
                        # Q-Learning hesapla
                        while (j < YONLER):
                            if (q[j, durum(pos.x, pos.y)] !=  0.0):
                                zero = False # keşfedilen yol bulundu
                                break
                            j += 1 # sıradaki
                        if (zero == False): # çıkışa geldi
                            max = q[j, durum(pos.x, pos.y)] # mevcut max q
                            k = j # mevcut optimal yol
                            j += 1 # sıradaki
                            while (j < YONLER):
                                # kontrol et 
                                if (q[j, durum(pos.x, pos.y)] !=  0.0):
                                    # max ı kontrol et
                                    if (q[j, durum(pos.x, pos.y)] > max):
                                        max = q[j, durum(pos.x, pos.y)] # yeni max q
                                        k = j # yeni optimal yol
                                j += 1 # sıradaki
                            a = k # optimal yol seç
                        else: # hiç yol yok
                            # keşfet
                            a = np.random.randint(0, YONLER) # random yön

                    dx, dy, r, f = yon(pos.x, pos.y, a)
                    adim += 1
                   
                    if ((dx != 0) or (dy != 0)): # ajan hareketi
                        canvas.blit(kutu, (pos.x*(HUCRE_BOYUTU+KENAR_BOYUT) , pos.y*(HUCRE_BOYUTU+KENAR_BOYUT))) # temiz hücre
                        canvas.blit(ayakizi, (pos.x*(HUCRE_BOYUTU+KENAR_BOYUT) , pos.y*(HUCRE_BOYUTU+KENAR_BOYUT))) # ayakizi çiz
                    # q-tablo güncelle
                    if (episode != (episode_max-1)):
                        if f == DUVAR_BAYRAK:
                            r -= 5

                        #formül
                        #if (np.isneginf(q[a, durum(pos.x, pos.y)]) ==  False):
                        #    if (np.isneginf(np.max(q[:, durum(pos.x+dx, pos.y+dy)])) == False):
                        #        q[a, durum(pos.x, pos.y)] = q[a, durum(pos.x, pos.y)] + ALFA*(r + GAMA*np.max(q[:, durum(pos.x+dx, pos.y+dy)])
                        #        - q[a, durum(pos.x, pos.y)])
                        #    else:
                        #        q[a, durum(pos.x, pos.y)] = q[a, durum(pos.x, pos.y)] + ALFA*(r - q[a, durum(pos.x, pos.y)])
                        #else:
                        #    if (np.isneginf(np.max(q[:, durum(pos.x+dx, pos.y+dy)])) == False):
                        #        q[a, durum(pos.x, pos.y)] = ALFA*(r + GAMA*np.max(q[:, durum(pos.x+dx, pos.y+dy)]))
                        #    else:
                        #        q[a, durum(pos.x, pos.y)] = ALFA*r
                        q[a, durum(pos.x, pos.y)] = q[a, durum(pos.x, pos.y)] + ALFA * (
                                    r + GAMA * np.max(q[:, durum(pos.x + dx, pos.y + dy)])- q[a, durum(pos.x, pos.y)])

                    skor += r # skor güncelle
                    print("skor: ", skor)
                    print("episode",episode)
                    # yeni hücreye taşı
                    pos.x = pos.x + dx
                    pos.y = pos.y + dy
                    reward_listesi.append(skor)
                    adim_listesi.append(adim)
                    if f == DUVAR_BAYRAK:
                        break
                
                    pygame.event.pump()
                    for event in pygame.event.get(): # eventi kontrol et
                        if event.type == pygame.QUIT:
                            sys.exit(0) # quite basınca çık
                
                #episode += 1 # episode u artır

            while (True): # pencerenin kapanmasını bekle
                pygame.event.pump()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        
                        fig, axs = plt.subplots(1,2)
                        axs[0].plot(reward_listesi)
                        axs[0].set_xlabel("episode")
                        axs[0].set_ylabel("reward")
                        
                        
                        axs[1].plot(adim_listesi)
                        axs[1].set_xlabel("episode")
                        axs[1].set_ylabel("step")
                        
                        axs[0].grid(True)
                        axs[1].grid(True)
                        
                        plt.show()
                        
                        sys.exit(0) # programdan çık
    
        buton1 = Button(secimPaneli, text = "Başla", command=girdiAl) 
        label1.pack()
        text1.pack()
        label2.pack()
        text2.pack()
        buton1.pack()
        secimPaneli.mainloop()          

    secim()

if (__name__ == "__main__"):
    main()