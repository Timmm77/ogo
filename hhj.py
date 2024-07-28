import pygame as pg
import enum
# Настройки
BOARD_SIZE = 8
CELL_SIZE = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
 
class Color(enum.Enum):
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

class Piece:
    row: int
    col: int
    color: Color
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def draw(self, screen):
        pg.draw.circle(screen, self.color.value, 
                       (self.col * CELL_SIZE + CELL_SIZE // 2, self.row * CELL_SIZE + CELL_SIZE // 2), 
                       CELL_SIZE // 3)

class Board:
    cells: list[list[Piece]]
    def __init__(self, screen):
        self.screen = screen
        self.cells = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.create_pieces()

    def create_pieces(self):
        for row in range(3):
            for col in range(row % 2, BOARD_SIZE, 2):
                self.cells[row][col] = Piece(row, col, Color.RED)
        for row in range(5, BOARD_SIZE):
            for col in range(row % 2, BOARD_SIZE, 2):
                self.cells[row][col] = Piece(row, col, Color.BLUE)

    def draw(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pg.draw.rect(self.screen, color, pg.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                if self.cells[row][col]:
                    self.cells[row][col].draw(self.screen)

class Game:
    board: Board
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((CELL_SIZE * BOARD_SIZE, CELL_SIZE * BOARD_SIZE))
        pg.display.set_caption("Checkers")
        self.board = Board(self.screen)
        self.selected_piece = None
        self.clock = pg.time.Clock()

    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    row, col = y // CELL_SIZE, x // CELL_SIZE
                    if self.selected_piece:
                        if self.valid_move(row, col, self.selected_piece):
                            self.move_piece(row, col)
                        self.selected_piece = None
                    else:
                        self.selected_piece = self.board.cells[row][col]
                elif event.type == pg.KEYDOWN and event.key == pg.K_r:
                    self.reset_game()

            self.screen.fill(BLACK)
            self.board.draw()
            pg.display.flip()
            self.clock.tick(60)

        pg.quit()
    
    def check_enemies(self, piece: Piece):
        if self.board.cells[piece.row - 1][piece.col - 1]:
            return True
        if self.board.cells[piece.row - 1][piece.col + 1]:
            return True
        if self.board.cells[piece.row + 1][piece.col - 1]:
            return True
        if self.board.cells[piece.row + 1][piece.col + 1]:
            return True

    def valid_move(self, row: int, col: int, piece: Piece):
        if col % 2 == piece.col % 2 and not self.check_enemies(piece):
            return False
        if self.board.cells[row][col]:
            return False
        return True

    def move_piece(self, row, col):
        if self.selected_piece:
            self.board.cells[self.selected_piece.row][self.selected_piece.col] = None
            self.board.cells[row][col] = self.selected_piece
            self.selected_piece.row, self.selected_piece.col = row, col

    def reset_game(self):
        self.board = Board(self.screen)
        self.selected_piece = None

if __name__ == "__main__":
    game = Game()
    game.run()


#def check_taking_steps_for_player(self, x, y):
        #if (x >= 0 and x < 8) and (y >= 0 and y < 8):   
            #if y < 6 and x < 6: