from random import randint


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return 'Вы пытаетесь выстрелить за доску!'


class BoardUsedException(BoardException):
    def __str__(self):
        return 'Вы уже стреляли в эту клетку'


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y}'


class Ship:
    def __init__(self, nose, le, d):
        self.nose = nose
        self.le = le
        self.d = d
        self.lives = le

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.le):
            cur_x = self.nose.x
            cur_y = self.nose.y
            if self.d == 0:
                cur_x += i
            elif self.d == 1:
                cur_y += i
            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    def ship_shot(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, size, hid=False):
        self.size = size
        self.hid = hid
        self.count = 0
        self.field = [['0'] * size for _ in range(size)]
        self.busy = []
        self.ships = []

    def __str__(self):
        res = ''
        res += '  '
        for i in range(1, self.size + 1):
            res += '|' + ' ' + f'{i}' + ' '
        res += '|'
        for i, row in enumerate(self.field):
            res += f'\n{i + 1} | ' + ' | '.join(row) + ' |'

        if self.hid:
            res = res.replace('■', '0')
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):
        near = [(0, 0), (0, -1), (-1, -1), (-1, 0), (-1, 1),
                (0, 1), (1, 1), (1, 0), (1, -1)]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = '.'
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = '■'
            self.busy.append(d)
        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()
        if d in self.busy:
            raise BoardUsedException()
        self.busy.append(d)
        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = 'X'
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print('Корабль уничтожен!')
                    return False
                else:
                    print('Корабль ранен.')
                    return True
            else:
                self.field[d.x][d.y] = '.'
                print('Мимо!')
                return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f'Ход компьютер: {d.x + 1}, {d.y + 1}')
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Введите координаты вашего хода: ").split()
            if len(cords) != 2:
                print('Введите две координаты!')
                continue
            x, y = cords
            if not (x.isdigit()) or not (y.isdigit()):
                print('Введите числа!')
                continue
            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True
        self.opp = AI(co, pl)
        self.us = User(pl, co)

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for i in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), i, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):
        num = 0
        while True:
            print('-' * 20)
            print('Доска пользователя:')
            print(self.us.board)
            print('-' * 20)
            print('Доска компьютера:')
            print(self.opp.board)
            print('-' * 20)
            if num % 2 == 0:
                print('Ходит пользователь!')
                repeat = self.us.move()
            else:
                print('Ходит компьютер!')
                repeat = self.opp.move()
            if repeat:
                num -= 1
            if self.opp.board.count == len(self.opp.board.ships):
                print('-' * 20)
                print('Пользователь выиграл!')
                break
            if self.us.board.count == len(self.us.board.ships):
                print('-' * 20)
                print('Компьютер выиграл!')
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
