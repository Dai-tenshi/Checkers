from tkinter import *
import random
import time
import copy
from tkinter import messagebox
from tkinter import font
from form import username
from form import is_loginned


is_game_stoped = False
move_order = False # False игрок, True компьютер
move_list = [] # Список возможных ходов
is_turns_exist = False # Если ходы на шашке еще есть
prediction = 0
last_checker = ()
#Счет
player_points = 0
bot_points = 0
def img_checkers():  # загружаем изображения пешек
    global peshki
    i1 = PhotoImage(file="images\\1b.gif")
    i2 = PhotoImage(file="images\\1bk.gif")
    peshki = [0, i1, i2]
def startGame():
    global doska
    global window
    global kabinet

    window = Toplevel(kabinet)  # создаём окно
    window.title('Артамоновы шашки. Заикин Михаил')  # заголовок окна
    doska = Canvas(window, width=800, height=800, bg='#FFFFFF')
    doska.pack()

    img_checkers()  # здесь загружаем изображения пешек
    new_game()  # начинаем новую игру
    rendering()  # рисуем игровое поле
    doska.bind("<Motion>", cell_hover)  # движение мышки по полю
    doska.bind("<Button-1>", cell_select)  # нажатие левой кнопки
    isRunning = True
def new_game():  # начинаем новую игру
    global pole
    global player_points
    global bot_points
    pole = [[0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0]]
    possible_turns(pole)
    player_points = 0
    bot_points = 0
def rendering():  # рисуем игровое поле
    global peshki
    global pole
    global kr_ramka, zel_ramka
    poz_x_1 = 1
    poz_y_1 = 1
    poz_x_2 = 1
    poz_y_2 = 1
    k = 100
    x = 0
    doska.delete('all')
    kr_ramka = doska.create_rectangle(-5, -5, -5, -5, outline="red", width=5)
    zel_ramka = doska.create_rectangle(-5, -5, -5, -5, outline="green", width=5)

    while x < 8 * k:  # рисуем доску
        y = 1 * k
        while y < 8 * k:
            doska.create_rectangle(x, y, x + k, y + k, fill="black")
            y += 2 * k
        x += 2 * k
    x = 1 * k
    while x < 8 * k:  # рисуем доску
        y = 0
        while y < 8 * k:
            doska.create_rectangle(x, y, x + k, y + k, fill="black")
            y += 2 * k
        x += 2 * k

    for y in range(8):  # рисуем стоячие пешки
        for x in range(8):
            z = pole[y][x]
            if z:
                if (poz_x_1, poz_y_1) != (x, y):
                    doska.create_image(x * k, y * k, anchor=NW, image=peshki[z])
    # рисуем активную пешку
    z = pole[poz_y_1][poz_x_1]
    if z:
        doska.create_image(poz_x_1 * k, poz_y_1 * k, anchor=NW, image=peshki[z], tag='ani')
        kx = 1 if poz_x_1 < poz_x_2 else -1
        ky = 1 if poz_y_1 < poz_y_2 else -1
        for i in range(abs(poz_x_1 - poz_x_2)):  # анимация перемещения пешки
            for ii in range(33):
                doska.move('ani', 0.03 * k * kx, 0.03 * k * ky)
                doska.update()  # обновление
                time.sleep(0.05)


def cell_hover(event):  # выбор клетки
    x, y = (event.x) // 100, (event.y) // 100  # вычисляем координаты клетки
    doska.coords(zel_ramka, x * 100, y * 100, x * 100 + 100, y * 100 + 100)  # рамка в выбранной клетке


def cell_select(event):  # выбор клетки для хода 2
    global poz1_x, poz1_y, poz2_x, poz2_y
    global move_order
    global player_points
    x, y = (event.x) // 100, (event.y) // 100  # вычисляем координаты клетки
    if pole[y][x] == 1 or pole[y][x] == 2:   # проверяем пешку игрока в выбранной клетке
        doska.coords(kr_ramka, x * 100, y * 100, x * 100 + 100, y * 100 + 100)  # рамка в выбранной клетке
        poz1_x, poz1_y = x, y
    else:
        if poz1_x != -1:  # клетка выбрана
            poz2_x, poz2_y = x, y
            if not move_order:  # ход игрока?
                checkers_before_turn = checkers_counter()
                make_turn(poz1_y, poz1_x, poz2_y, poz2_x)
                checkers_after_turn = checkers_counter()
                player_points += checkers_before_turn - checkers_after_turn
                current_move_order()
            else:
                pass
                # bot_turns()  # передаём ход компьютеру
            poz1_x = -1  # клетка не выбрана
            doska.coords(kr_ramka, -5, -5, -5, -5)  # рамка вне поля
def possible_turns(polee): # Сканер возможных ходов каждой шашкы для конкретной вариации поля
    global move_list
    move_list.clear()
    for x in range(8):
        for y in range(8):
            if polee[y][x] == 1 or polee[y][x] == 2:
                move_list += possible_turn_for_checker(x, y, False, polee) # Добавляем ходы шашки
def checkers_counter():
    global pole
    global bot_points
    global player_points
    checkers_on_pole = 0
    for x in range(8):
        for y in range(8):
            if pole[y][x] != 0:
                checkers_on_pole += 1
    if checkers_on_pole <= 2:
        end_game()
    return checkers_on_pole
def end_game():
    global is_game_stoped
    global player_points
    global bot_points
    if not is_game_stoped:
        print("Конец игры")
        #messagebox.showinfo(player_points)
        if player_points >= 11:
            messagebox.showinfo("Победа", "Вы играли и выиграли)\nПерезайдите, чтобы начать заново")
        else:
            messagebox.showinfo("Поражение", "Вы играли и проиграли(\nПерезайдите, чтобы начать заново?")
        is_game_stoped = True
    window.destroy()
def possible_turn_for_checker(x,y, only_atack, polee): # Просмотр ходов отдельной шашечкы
    move_list = []
    global move_order
    global last_checker
    coords_for_battle = [(-1, 1), (-1, -1), (1, -1), (1, 1)]
    coords_for_move = [1, -1]
    for c in coords_for_move: # Ход пешки
        y_coord = 0
        if not move_order:
            y_coord = -1
        else:
            y_coord = 1
        if 0 <= y + y_coord <= 7 and 0 <= x + c <= 7 and not only_atack: # Если ход - не только атака (турецкая рубка)
            if polee[y][x] == 1 and polee[y + y_coord][x + c] == 0 and (y,x) != last_checker:
                move_list.append(((y,x),(y + y_coord, x + c), 0)) # Первый () - коорд. шашки, второй - куда она ходит
    for c in coords_for_battle: # Еда пешки
        if 0 <= y + c[0] * 2 <= 7 and 0 <= x + c[1] * 2 <= 7:
            if polee[y][x] == 1 and (polee[y + c[0]][x + c[1]] == 1 or polee[y + c[0]][x + c[1]] == 2)\
                    and polee[y + c[0] * 2][x + c[1] * 2] == 0 and (y,x) != last_checker:
                move_list.append(((y, x), (y + c[0] * 2, x + c[1] * 2), 1))
    for c in coords_for_battle: # Ходьба для дамки
        for i in range(1, 8):
            if 0 <= y + c[0] * (i) <= 7 and 0 <= x + c[1] * (i) <= 7:
                if polee[y][x] == 2 and polee[y + c[0] * i][x + c[1] * i] == 0 and (y,x) != last_checker \
                        and not only_atack:
                    move_list.append(((y, x), (y + c[0] * i, x + c[1] * i), 2))
            if 0 <= y + c[0] * (i + 1) <= 7 and 0 <= x + c[1] * (i + 1) <= 7:
                if polee[y][x] == 2 \
                        and (polee[y + c[0] * i][x + c[1] * i] == 1 or polee[y + c[0] * i][x + c[1] * i] == 2) \
                        and polee[y + c[0] * (i + 1)][x + c[1] * (i + 1)] == 0 and (y,x) != last_checker:
                    move_list.append(((y, x), (y + c[0] * (i + 1), x + c[1] * (i + 1)), 3))
                    break
                elif polee[y][x] == 2 \
                        and (polee[y + c[0] * i][x + c[1] * i] == 1 or polee[y + c[0] * i][x + c[1] * i] == 2) \
                        and polee[y + c[0] * (i + 1)][x + c[1] * (i + 1)] != 0 and (y,x) != last_checker:
                    break
            else:
                break
    return move_list
def make_turn(checker_y, checker_x, target_y, target_x): # Сделать ход по правилам
    global move_list
    global move_order
    global pole
    global last_checker
    global is_turns_exist
    # Ищем совпадение введенного хода из списка всех ходов
    for turn in move_list:
        if pole[checker_y][checker_x] == 1 and turn == ((checker_y, checker_x), (target_y, target_x), 0):
            pole[checker_y][checker_x] = 0
            pole[target_y][target_x] = 1
            last_checker = (target_y, target_x)
            move_order = True
            if target_y == 7 or target_y == 0:
                pole[target_y][target_x] = 2
        elif pole[checker_y][checker_x] == 1 and turn == ((checker_y, checker_x), (target_y, target_x), 1):
            pole[checker_y][checker_x] = 0
            pole[target_y][target_x] = 1
            # Направление, в котором бьет пешка
            direction = int((target_y - checker_y) / 2), int((target_x - checker_x) / 2)
            pole[target_y - direction[0]][target_x - direction[1]] = 0
            checker_move_list = possible_turn_for_checker(target_x, target_y, True, pole) # Проверяем ход той же шашкой
            if len(checker_move_list) > 0:
                is_turns_exist = True
                move_list.clear()
                move_list += checker_move_list
                pass
            else:
                is_turns_exist = False
                last_checker = (target_y, target_x)
                move_order = True
            if target_y == 7 or target_y == 0:
                pole[target_y][target_x] = 2
        elif pole[checker_y][checker_x] == 2 and turn == ((checker_y, checker_x), (target_y, target_x), 2):
            pole[checker_y][checker_x] = 0
            pole[target_y][target_x] = 2
            last_checker = (target_y, target_x)
            move_order = True
        elif pole[checker_y][checker_x] == 2 and turn == ((checker_y, checker_x), (target_y, target_x), 3):
            pole[checker_y][checker_x] = 0
            pole[target_y][target_x] = 2
            direction = int((target_y - checker_y) / 2), int((target_x - checker_x) / 2)
            pole[target_y - direction[0]][target_x - direction[1]] = 0
            checker_move_list = possible_turn_for_checker(target_x, target_y, True, pole)  # Проверяем ход той же шашкой
            if len(checker_move_list) > 0:
                is_turns_exist = True
                move_list.clear()
                move_list += checker_move_list
                pass
            else:
                is_turns_exist = False
                last_checker = (target_y, target_x)
                move_order = True
    rendering()
    possible_turns(pole) # Теперь ищем все ходы на измененной доске
    if is_turns_exist and move_order:
        bot_turns()
    checkers_counter()
def current_move_order():
    global move_order
    if move_order:
        bot_turns()
# Бот
def bot_turns():
    global move_list
    global pole
    global move_order
    global last_checker
    global bot_points
    pole_in_brain = copy.deepcopy(pole)
    #Соберем все ходы для бота
    turns_for_bots = []
    for move in move_list:
        if move[2] == 0:
            turns_for_bots.append(((move[0][0], move[0][1]), (move[1][0], move[1][1]), 0)) # Если тип хода - ходьба - цена 0
        elif move[2] == 1:
            turns_for_bots.append(((move[0][0], move[0][1]), (move[1][0], move[1][1]), 1)) # Если тип хода - рубка - цена +1
        elif move[2] == 2:
            turns_for_bots.append(((move[0][0], move[0][1]), (move[1][0], move[1][1]), 1)) # Если тип хода - ходьба дамки - цена 0
        elif move[2] == 3:
            turns_for_bots.append(((move[0][0], move[0][1]), (move[1][0], move[1][1]), 2)) # Если тип хода - рубка дамки - цена +1
    # Начинаем анализ заданной глубины собранных ходов и изменяем там цены
    for turn in turns_for_bots:
        pole_in_brain_raschet = copy.deepcopy(pole_in_brain)
        for p in range(prediction):
            pole_in_brain_raschet[turn[0][0]][turn[0][1]] = 0
            pole_in_brain_raschet[turn[1][0]][turn[1][1]] = 1
            # Сначала бот предсказывает лучший ход игрока
            move_order = False
            possible_turns(pole_in_brain_raschet)
            move_order = True
            best_player_turn= move_list[random.randint(0, len(move_list) - 1)]
            if best_player_turn[2] == 0:
                pole_in_brain_raschet[best_player_turn[0][0]][best_player_turn[0][1]] = 0
                pole_in_brain_raschet[best_player_turn[1][0]][best_player_turn[1][1]] = 1
                turn = ((move[0][0], move[0][1]), (move[1][0], move[1][1]), turn[2] + 0)
            elif best_player_turn[2] == 1:
                pole_in_brain_raschet[best_player_turn[0][0]][best_player_turn[0][1]] = 0
                pole_in_brain_raschet[best_player_turn[1][0]][best_player_turn[1][1]] = 1
                turn = ((move[0][0], move[0][1]), (move[1][0], move[1][1]), turn[2] - 1)
            elif best_player_turn[2] == 2:
                pole_in_brain_raschet[best_player_turn[0][0]][best_player_turn[0][1]] = 0
                pole_in_brain_raschet[best_player_turn[1][0]][best_player_turn[1][1]] = 2
                turn = ((move[0][0], move[0][1]), (move[1][0], move[1][1]), turn[2] + 1)
            elif best_player_turn[2] == 3:
                pole_in_brain_raschet[best_player_turn[0][0]][best_player_turn[0][1]] = 0
                pole_in_brain_raschet[best_player_turn[1][0]][best_player_turn[1][1]] = 2
                turn = ((move[0][0], move[0][1]), (move[1][0], move[1][1]), turn[2] - 2)
            # Теперь делаем ход бота на основе хода игрока
            possible_turns(pole_in_brain_raschet)
            best_raschet_turn = move_list[random.randint(0, len(move_list) - 1)]
            if best_raschet_turn[2] == 0:
                pole_in_brain_raschet[best_raschet_turn[0][0]][best_raschet_turn[0][1]] = 0
                pole_in_brain_raschet[best_raschet_turn[1][0]][best_raschet_turn[1][1]] = 1
                turn = ((move[0][0], move[0][1]), (move[1][0], move[1][1]), turn[2] + 0)
            elif best_raschet_turn[2] == 1:
                pole_in_brain_raschet[best_raschet_turn[0][0]][best_raschet_turn[0][1]] = 0
                pole_in_brain_raschet[best_raschet_turn[1][0]][best_raschet_turn[1][1]] = 1
                turn = ((move[0][0], move[0][1]), (move[1][0], move[1][1]), turn[2] + 1)
            elif best_raschet_turn[2] == 2:
                pole_in_brain_raschet[best_raschet_turn[0][0]][best_raschet_turn[0][1]] = 0
                pole_in_brain_raschet[best_raschet_turn[1][0]][best_raschet_turn[1][1]] = 2
                turn = ((move[0][0], move[0][1]), (move[1][0], move[1][1]), turn[2] + 1)
            elif best_raschet_turn[2] == 3:
                pole_in_brain_raschet[best_raschet_turn[0][0]][best_raschet_turn[0][1]] = 0
                pole_in_brain_raschet[best_raschet_turn[1][0]][best_raschet_turn[1][1]] = 2
                turn = ((move[0][0], move[0][1]), (move[1][0], move[1][1]), turn[2] + 2)
    best_index = 0 # Индекс максимальной цены
    best_cost = 0 # Максимальная цена
    if len(turns_for_bots) == 0:
        print("У бота нет ходов")
        end_game()
        return
    for i in range(len(turns_for_bots)):
        if best_cost < turns_for_bots[i][2]:
            best_cost = turns_for_bots[i][2]
            best_index = i
    best_turn = turns_for_bots[best_index]
    make_turn(best_turn[0][0], best_turn[0][1], best_turn[1][0], best_turn[1][1])
    #Для отладки
    make_turn(best_turn[0][0], best_turn[0][1], best_turn[1][0], best_turn[1][1])
    # Для отладки
    print(best_turn)
    move_order = False
    #last_checker = (best_turn[1][0], best_turn[1][1])

def turn_order_check():
    global move_order
    global bot_points
    if move_order:
        checkers_before_turn = checkers_counter()
        bot_turns()
        checkers_after_turn = checkers_counter()
        bot_points += checkers_before_turn - checkers_after_turn
    window.after(1, turn_order_check)
isRunning = False
#startGame()
if isRunning:
    window.after(0, turn_order_check)





# главное окно приложения
kabinet = Tk()
# заголовок окна
kabinet.title('Главная страница')
# размер окна
kabinet.geometry('600x600')
# можно ли изменять размер окна - нет
kabinet.resizable(False, False)
kabinet["bg"]='black'
img=PhotoImage(file='images/fon2.png')
Label(kabinet,image=img,bg='white',height='600',width='590').place(x=0,y=0)
font1=font.Font(family= "Arial", size=11, weight="normal", slant="italic")

if not is_loginned:
    print("Вход не выполнен")
    kabinet.destroy()

def play_button_clicked():
    startGame()

play_Button = Button(kabinet, text="Играть",border=0,bg='black',cursor='hand2',fg='red',font=font1, command= play_button_clicked)
play_Button.place(x=255,y=400)
username_label = Label(kabinet, text=f'имя пользователя:{username}',fg='black',bg='white').place(x=10,y=25)

mainloop()