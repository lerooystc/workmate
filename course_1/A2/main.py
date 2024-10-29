from random import randrange


class Cell:
    def __init__(self, x: int, y: int) -> None:
        # Добавил в клетки их координаты
        self.x = x
        self.y = y
        self.mines_around: int = 0
        self.is_mine: bool = False
        self.is_open: bool = False

    def has_neighbours(self, m_coords: set[tuple[int, int]], size: int) -> None:
        """
        Проверяет соседей каждой клетки на наличие мин.
        """
        for x in range(self.x - 1, self.x + 2):
            for y in range(self.y - 1, self.y + 2):
                coords = (x, y)
                if self.is_in_bounds(coords, size):
                    if coords in m_coords:
                        self.mines_around += 1

    def is_mine(self, m_coords: set[tuple[int, int]]) -> None:
        """
        Проверяет, если сама клетка мина.
        """
        self.is_mine = (self.x, self.y) in m_coords

    @staticmethod
    def is_in_bounds(coords: tuple[int, int], size: int) -> bool:
        """
        Вспомогательный метод к проверке соседей, проверяет вход координат в рамки.
        """
        x, y = coords
        return 0 <= x < size and 0 <= y < size

    def __repr__(self) -> str:
        if self.is_mine:
            return "*"
        return str(self.mines_around)


class GameField:
    def __init__(self, size: int, mines: int):
        self.size = size
        self.mines = mines
        self.field = None
        self.init()

    def init(self) -> None:
        mine_coords = set()
        while len(mine_coords) != self.mines:
            a, b = randrange(self.size), randrange(self.size)
            mine_coords.add((a, b))
        field = []
        for x in range(self.size):
            inner_list = []
            for y in range(self.size):
                cell = Cell(x, y)
                cell.is_mine(mine_coords)
                cell.has_neighbours(mine_coords, self.size)
                inner_list.append(cell)
            field.append(inner_list)
        self.field = field

    def show(self) -> None:
        # Для наглядности решения решил не закрывать все клетки, а выводить как есть
        for one in self.field:
            print(*one)


gf = GameField(10, 10)
gf.show()
