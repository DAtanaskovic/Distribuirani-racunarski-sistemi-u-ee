import random
from time import sleep
from Zid import Maze
import pygame

def move_enemy_online(randomEnemy_x1, randomEnemy_x2, randomEnemy_y1, randomEnemy_y2, nivo, red):
    # treba dodati da se pre svakog menjanja koordinata, na svakom starom mestu iscrtavaju tragovi/trava
    #print('neprijateljproces')
    pygame.init()
    maze = Maze()
    matrica = maze.maze
    brzina = 1 #2 / nivo.value
    broj = 0
    start_ticks = 0
    lista1 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    lista2 = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    broj_prvog = 0
    broj_drugog = 0
    while True:
        sleep(brzina)
        if broj != 0:
            print('sekundepocetak')
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # calculate how many seconds
            print('sekundekraj',seconds)
            if seconds > 5:
                broj = 0

        if not red.empty():
            broj = red.get()
            start_ticks = pygame.time.get_ticks()

        if broj != 3:

            random_generator = lista2[broj_drugog]
            broj_drugog = broj_drugog + 1
            if broj_drugog >= 20:
                broj_drugog = 0
            if (random_generator == 4):
                temprandomEnemy_x1 = randomEnemy_x1.value - 1    #levo
                number_of_first_enemy = int(temprandomEnemy_x1 + randomEnemy_y1.value * 20)
                # if (matrica[int(number_of_first_enemy)] != 0):  # da je zid
                #     continue
                # elif (int(number_of_first_enemy) == 1):  # ako je mesto 2 igraca
                #     continue
                # elif (int(number_of_first_enemy) == 2):  # ako je mesto 1 igraca
                #     continue
                # elif (matrica[int(number_of_first_enemy)] == 5):  # ako je zamka
                #     continue
                randomEnemy_x1.value = temprandomEnemy_x1

            elif (random_generator == 2):  # gore
                temprandomEnemy_y1 = randomEnemy_y1.value - 1
                number_of_first_enemy = int(randomEnemy_x1.value + temprandomEnemy_y1 * 20)
                # if (matrica[int(number_of_first_enemy)] != 0):  # da je zid
                #     continue
                # elif (int(number_of_first_enemy) == 61):  # ako je mesto 2 igraca
                #     continue
                # elif (int(number_of_first_enemy) == 41):  # ako je mesto 1 igraca
                #     continue
                # elif (matrica[int(number_of_first_enemy)] == 5):  # ako je zamka
                #     continue
                randomEnemy_y1.value = temprandomEnemy_y1

            elif (random_generator == 1):  # desno
                temprandomEnemy_x1 = randomEnemy_x1.value + 1
                number_of_first_enemy = int(temprandomEnemy_x1 + randomEnemy_y1.value * 20)
                # if (matrica[int(number_of_first_enemy)] != 0):  # da je zid
                #     continue
                # elif (int(number_of_first_enemy) == 61):  # ako je mesto 2 igraca
                #     continue
                # elif (int(number_of_first_enemy) == 41):  # ako je mesto 1 igraca
                #     continue
                # elif (matrica[int(number_of_first_enemy)] == 5):  # ako je zamka
                #     continue
                randomEnemy_x1.value = temprandomEnemy_x1

            elif (random_generator == 3):  #dole
                #print('gore')
                temprandomEnemy_y1 = randomEnemy_y1.value + 1
                # number_of_first_enemy = int(randomEnemy_x1.value + temprandomEnemy_y1 * 20)
                # if (matrica[int(number_of_first_enemy)] != 0):  # da je zid
                #     continue
                # elif (int(number_of_first_enemy) == 61):  # ako je mesto 2 igraca
                #     continue
                # elif (int(number_of_first_enemy) == 41):  # ako je mesto 1 igraca
                #     continue
                # elif (matrica[int(number_of_first_enemy)] == 5):  # ako je zamka
                #     continue
                randomEnemy_y1.value = temprandomEnemy_y1


        if broj != 4:
            random_generator = lista1[broj_prvog]
            broj_prvog = broj_prvog + 1
            if broj_prvog >= 30:
                broj_prvog = 0

            if (random_generator == 4):
                temprandomEnemy_x2 = randomEnemy_x2.value - 1
                number_of_second_enemy = int(temprandomEnemy_x2 + randomEnemy_y2.value * 20)
                # print(number_of_first_enemy,number_of_second_enemy)
                # if (matrica[int(number_of_second_enemy)] != 0):
                #     continue
                # elif (int(number_of_second_enemy) == 61):
                #     continue
                # elif (int(number_of_second_enemy) == 41):
                #     continue
                # elif (matrica[int(number_of_second_enemy)] == 5):
                #     continue
                randomEnemy_x2.value = temprandomEnemy_x2

            elif (random_generator == 2):
                temprandomEnemy_y2 = randomEnemy_y2.value - 1
                number_of_second_enemy = int(randomEnemy_x2.value + temprandomEnemy_y2 * 20)
                # if (matrica[int(number_of_second_enemy)] != 0):
                #     continue
                # elif (int(number_of_second_enemy) == 61):
                #     continue
                # elif (int(number_of_second_enemy) == 41):
                #     continue
                # elif (matrica[int(number_of_second_enemy)] == 5):
                #     continue
                randomEnemy_y2.value = temprandomEnemy_y2

            elif (random_generator == 1):
                temprandomEnemy_x2 = randomEnemy_x2.value + 1
                number_of_second_enemy = int(temprandomEnemy_x2 + randomEnemy_y2.value * 20)
                # if (matrica[int(number_of_second_enemy)] != 0):
                #     continue
                # elif (int(number_of_second_enemy) == 61):
                #     continue
                # elif (int(number_of_second_enemy) == 41):
                #     continue
                # elif (matrica[int(number_of_second_enemy)] == 5):
                #     continue
                randomEnemy_x2.value = temprandomEnemy_x2

            elif (random_generator == 3):
                temprandomEnemy_y2 = randomEnemy_y2.value + 1
                number_of_second_enemy = int(randomEnemy_x2.value + temprandomEnemy_y2 * 20)
                # if (matrica[int(number_of_second_enemy)] != 0):
                #     continue
                # elif (int(number_of_second_enemy) == 61):
                #     continue
                # elif (int(number_of_second_enemy) == 41):
                #     continue
                # elif (matrica[int(number_of_second_enemy)] == 5):
                #     continue
                randomEnemy_y2.value = temprandomEnemy_y2
