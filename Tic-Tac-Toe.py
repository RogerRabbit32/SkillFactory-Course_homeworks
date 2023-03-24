field = [['-', '-', '-'] for i in range(3)]


def show_field():
    print(' ', '0', '1', '2')
    for i in range(3):
        print(f'{i}', ' '.join(field[i]))


def request():
    while True:
        print()
        if n % 2 != 0:
            print(f'Игрок 1, пожалуйста, введите координаты вашего хода:')
        else:
            print(f'Игрок 2, пожалуйста, введите координаты вашего хода:')
        a = input().split()
        if len(a) < 2 or len(a) > 2:
            print('Нам потребуются две координаты...')
            print('---------------------------------')
            continue
        elif not a[0].isdigit() or not a[1].isdigit():
            print('Пожалуйста, вводите только числа.')
            print('---------------------------------')
            continue
        z, h = int(a[0]), int(a[1])
        if (z == 0 or z == 1 or z == 2) and \
                (h == 0 or h == 1 or h == 2) and \
                field[z][h] != '-':
            print('Эта клетка уже занята.')
            print('---------------------------------')
        elif (z == 0 or z == 1 or z == 2) and \
                (h == 0 or h == 1 or h == 2) and \
                field[z][h] == '-':
            return z, h
        else:
            print('Пожалуйста, введите две координаты. Только числа от 0 до 2! :(')
            print('---------------------------------')


def win_condition():
    if field[0][0] == field[1][1] == field[2][2] != '-':
        return True
    elif field[2][0] == field[1][1] == field[0][2] != '-':
        return True
    elif field[0][0] == field[0][1] == field[0][2] != '-':
        return True
    elif field[1][0] == field[1][1] == field[1][2] != '-':
        return True
    elif field[2][0] == field[2][1] == field[2][2] != '-':
        return True
    elif field[0][0] == field[1][0] == field[2][0] != '-':
        return True
    elif field[0][1] == field[1][1] == field[2][1] != '-':
        return True
    elif field[0][2] == field[1][2] == field[2][2] != '-':
        return True
    else:
        return False


def intro():
    print('--------------------------------------------------')
    print('    Добро пожаловать в игру "Крестики-Нолики"!')
    print('  Для того чтобы поставить свой знак ("O" или "X"),')
    print(' нужно будет ввести две координаты: по горизонтали')
    print(' и вертикали: числа 0, 1 или 2. Вот так: 0 1. Для')
    print('вашего удобства эти координаты указаны вокруг поля.')
    print()
    print(' ', '0', '1', '2')
    print('0', '-', 'X', '-')
    print('1', '-', '-', '-')
    print('2', '-', '-', '-')
    print()
    print('Удачи!')
    print('---------------------------------------------------')


intro()
show_field()
n = 0
while True:
    n += 1
    x, y = request()
    if n % 2 != 0:
        field[x][y] = 'X'
    if n % 2 == 0:
        field[x][y] = 'O'
    show_field()
    if win_condition():
        if n % 2 != 0:
            print('Победа! Поздравляем, Игрок 1! Игра окончена.')
        else:
            print('Победа! Поздравляем, Игрок 2! Игра окончена.')
        break
    if n == 9:
        print('Ничья! Ещё одну партию?')
        break
