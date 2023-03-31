import pygame
import random
import math

pygame.init()  # inicjalizacja

# tworzy ekran
screen = pygame.display.set_mode((700, 600))
clock = pygame.time.Clock()  # tworzy obiekt pomagajacy sledzic czas

# timer
licznik = 45
font3 = pygame.font.SysFont('Comic Sans MS', 25)
text3 = font3.render(str(licznik), True, (0, 0, 0))
timer_event = pygame.USEREVENT + 1  # pewien event stworzony przez uzytkownika
pygame.time.set_timer(timer_event, 1000)  # event pokazuje sie co 1 sekunde (1000 mili sekund) od rozpoczecia programu

# nazwa gry
pygame.display.set_caption("Duck Hunt")

# postacie
tlo = pygame.image.load("assets/tlo.jpg").convert_alpha()  # convert aplha poprawia wydajnosc
duckImg = pygame.image.load("assets/rubber-duck.png").convert_alpha()  # zamiana formatu pixeli obrazka
bulletImg = pygame.image.load("assets/bullet.png").convert_alpha()  # na taki sam jakich uzywa ekran
hunterImg = pygame.image.load("assets/hunter2.png").convert_alpha()

hunterX = 315  # wspolrzedne postaci
hunterY = 450
hunterV = 3

duckX = random.randint(1, 635)  # kaczka
duckY = random.randint(0, 150)
duckV = 4

bulletX = 0  # strzal
bulletY = 0
bulletV = 6
bulletS = "ready"


def hunter(x, y):  # definiowanie postaci
    screen.blit(hunterImg, (x, y))


def duck(x, y):
    screen.blit(duckImg, (x, y))


def bullet(x, y):
    global bulletS
    bulletS = "fire"
    screen.blit(bulletImg, (x - 21, y + 10))


def hit(duckX, duckY, bulletX, bulletY):
    distance = math.sqrt((math.pow(duckX - bulletX, 2) + math.pow(duckY - bulletY, 2)))
    if distance < 20:
        return True
    return False


pkt = '0'
font = pygame.font.SysFont('Comic Sans MS', 25)
font1 = pygame.font.SysFont('Comic Sans MS', 25)
punkty = font1.render('Punkty', True, (0, 0, 0))


def pkt1():
    tekst1 = font.render(pkt, True, (0, 0, 0))
    tekst2 = tekst1.get_rect(center=(110, 550))  # pobiera szerokosc i wysokosc
    screen.blit(tekst1, tekst2)


font2 = pygame.font.SysFont('Comic Sans MS', 50)
pause = True


def unpaused():
    global pause
    pause = False


def end():
    koniec = font2.render('Koniec gry', True, (0, 0, 0))
    efg = koniec.get_rect(center=(350, 300))
    screen.blit(koniec, efg)
    napis = font1.render('Aby wyjsc nacisnij q', True, (0, 0, 0))
    abc = napis.get_rect(center=(350, 400))
    screen.blit(napis, abc)
    koniecgry = True
    while koniecgry:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:  # nacisniecie przycisku q powoduje zamkniecie
                if event.key == pygame.K_q:
                    raise SystemExit
        duck(duckX, duckY)
        hunter(hunterX, hunterY)
        screen.blit(text3, text3_rect)
        pkt1()
        bullet(bulletX, bulletY)
        screen.blit(punkty, (10, 530))
        pygame.display.flip()


def paused():
    pauza2 = font2.render('Pauza', True, (0, 0, 0))
    tekst0 = pauza2.get_rect(center=(350, 300))
    screen.blit(pauza2, tekst0)
    napis = font1.render('q - wyjscie    p - powrot', True, (0, 0, 0))
    abc = napis.get_rect(center=(350, 400))
    screen.blit(napis, abc)
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:  # nacisniecie przycisku q powoduje zamkniecie
                if event.key == pygame.K_q:
                    raise SystemExit
                elif event.key == pygame.K_p:
                    unpaused()
        duck(duckX, duckY)
        hunter(hunterX, hunterY)
        screen.blit(text3, text3_rect)
        pkt1()
        bullet(bulletX, bulletY)
        screen.blit(punkty, (10, 530))
        pygame.display.flip()


run = True

while run:  # petla by ekran pokazywal sie bez przerwy
    screen.blit(tlo, (0, 0))
    clock.tick(120)  # klatki na sekunde
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # wylaczenie programu
            run = False
        elif event.type == pygame.KEYDOWN:  # nacisniecie przycisku q powoduje zamkniecie
            if event.key == pygame.K_q:
                raise SystemExit
            if event.key == pygame.K_p:
                pause = True
                paused()
        elif event.type == timer_event:  # co sekunde licznik zmniejsza sie o 1
            licznik = licznik - 1
            text3 = font.render(str(licznik), True, (0, 0, 0))  # renderowanie liczby punktow
            if licznik == 0:
                pygame.time.set_timer(timer_event, 0)  # zatrzymanie naliczania czasu
                end()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if bulletS == "ready":  # strzal
                    bulletY = hunterY
                    bulletX = hunterX
                    bullet(bulletX, bulletY)
    pkt1()
    screen.blit(punkty, (10, 530))
    if pygame.key.get_pressed()[pygame.K_LEFT]:  # ruch postaci
        hunterX -= hunterV
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        hunterX += hunterV

    if hunterX <= 0:  # ograniczenia co do obszaru
        hunterX = 0
    elif hunterX >= 636:
        hunterX = 636

    if duckX <= 0:  # ograniczenie kaczki
        duckX = 0
    elif duckX >= 636:
        duckX = 636

    if duckX <= 0:  # ruch kaczki
        duckV *= -1
    elif duckX >= 636:
        duckV *= -1
    duckX = duckX + duckV

    if bulletY <= -32:
        bulletY = -50
        bulletS = "ready"

    if bulletS == "fire":  # strzal ciagla zmiana wspolrzednych pociusku
        bullet(bulletX, bulletY)
        bulletY -= bulletV

    point = hit(duckX, duckY, bulletX, bulletY)  # trafienie

    if point:  # w momencie zdobycia punktu
        bulletS = "ready"
        bulletY = -50
        pkt = str(int(pkt) + 1)
        duckX = random.randint(1, 635)  # losowe wspolrzedne kaczki i predkosc
        duckY = random.randint(0, 150)
        los = random.randint(1, 2)
        if los == 1:
            duckV = random.randint(-4, -1)
        elif los == 2:
            duckV = random.randint(1, 4)

    text3_rect = text3.get_rect(center=(550, 549))  # get rect pobiera wymiary powierzchni
    duck(duckX, duckY)
    hunter(hunterX, hunterY)
    screen.blit(text3, text3_rect)
    pygame.display.flip()  # updatuje powierzchnie ekranu
