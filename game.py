import sys
import chess, chess.engine
import sqlite3
from PyQt5 import uic
from PyQt5.Qt import QMainWindow
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QFontDatabase, QFont
from PyQt5.QtCore import QSize

board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci("stockfish/stockfish32bit.exe")

icon = QIcon()
file_names = {'r': 'bR.png', 'q': 'bQ.png',
              'k': 'bK.png', 'p': 'bp.png',
              'b': 'bB.png', 'n': 'bN.png',
              'R': 'wR.png', 'Q': 'wQ.png',
              'K': 'wK.png', 'P': 'wp.png',
              'B': 'wB.png', 'N': 'wN.png'}

positions = {'1': 'a', '2': 'b', '3': 'c', '4': 'd', '5': 'e', '6': 'f', '7': 'g', '8': 'h'}
NOTATION = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w — 0 1"


class Chess(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/mainWindowDesign.ui', self)  # Загружаем дизайн
        QFontDatabase.addApplicationFont("font/molot.otf")
        self.font = QFont("molot", 40)
        self.font.setFamily(u"molot")
        self.font.setPixelSize(135)
        self.chess_let.setFont(self.font)
        self.playButton.clicked.connect(self.menuToPlay)
        self.tasksButton.clicked.connect(self.menuToTasks)
        self.ruleButton.clicked.connect(self.menuToRules)
        self.initUI()

    def initUI(self):
        self.group = []
        self.click_counter = 0
        self.move_text = ''
        self.string = ""

    def menuToPlay(self):
        global board
        uic.loadUi('UI/play.ui', self)
        self.backToTasksButton.clicked.connect(self.backToMenu)
        board = chess.Board()
        self.group = []
        self.board()
        board = chess.Board()

    def backToMenu(self):
        uic.loadUi('UI/mainWindowDesign.ui', self)
        self.chess_let.setFont(self.font)
        self.playButton.clicked.connect(self.menuToPlay)
        self.tasksButton.clicked.connect(self.menuToTasks)
        self.ruleButton.clicked.connect(self.menuToRules)

    def menuToRules(self):
        uic.loadUi('UI/rulesWindowDesign.ui', self)
        self.chess_let.setFont(self.font)
        self.backToMenuButton.clicked.connect(self.backToMenu)

    def menuToTasks(self):
        uic.loadUi('UI/tasksWindowDesign.ui', self)
        self.chess_let.setFont(self.font)
        self.backToMenuButton.clicked.connect(self.backToMenu)
        self.taskButton_1.clicked.connect(self.startTask)
        self.taskButton_2.clicked.connect(self.startTask)
        self.taskButton_3.clicked.connect(self.startTask)
        self.taskButton_4.clicked.connect(self.startTask)
        self.taskButton_5.clicked.connect(self.startTask)
        self.taskButton_6.clicked.connect(self.startTask)
        self.taskButton_7.clicked.connect(self.startTask)
        self.taskButton_8.clicked.connect(self.startTask)
        self.taskButton_9.clicked.connect(self.startTask)
        self.taskButton_10.clicked.connect(self.startTask)

    def startTask(self):
        global board
        id = self.sender().objectName().split('_')[1]
        connect = sqlite3.connect("DB/chess_db.sqlite")
        cursor = connect.cursor()
        notation = cursor.execute(f"""SELECT task FROM tasks WHERE id={id}""").fetchall()[0][0]
        connect.close()
        uic.loadUi('UI/play.ui', self)
        self.group = []
        self.board(board=notation)
        board = chess.Board(notation)
        self.backToTasksButton.clicked.connect(self.menuToTasks)

    def exit(self):
        sys.exit(0)

    def board(self, board=NOTATION):
        board_fen = board
        board_fen_list = board_fen.split('/')
        self.data = list()
        counter = 0
        for i in board_fen_list:
            fen = ''
            fen += i
            counter += 1
            for j in i:
                if j.isdigit():
                    fen = fen.replace(j, '*' * int(j), 1)
            if counter != 8:
                fen_row_list = list(fen)
            else:
                fen_row_list = list(fen[:8])
            self.data.append(fen_row_list)
        self.move2 = 60
        counter_for_cell_colour_1 = 0
        for x in self.data:
            counter_for_cell_colour_1 += 1
            counter_for_cell_colour_2 = 0
            self.move2 += 60
            self.move1 = 10
            intermediate_list = []
            for y in x:
                counter_for_cell_colour_2 += 1
                self.move1 += 60
                self.btn = QPushButton(
                    f"{positions[str(counter_for_cell_colour_2)]}{str(9 - counter_for_cell_colour_1)}", self)
                intermediate_list.append(self.btn)
                self.btn.move(342 + self.move1, self.move2)
                self.btn.resize(60, 60)
                self.btn.clicked.connect(self.clicked)
                self.btn.show()
                self.btn.setStyleSheet('QPushButton {font-size: 1px;}')
                if counter_for_cell_colour_2 % 2 != 0 and counter_for_cell_colour_1 % 2 != 0:
                    self.btn.setStyleSheet('QPushButton {background-color: #322e2b; '
                                           'font-size: 1px;}')
                if counter_for_cell_colour_2 % 2 != 0 and counter_for_cell_colour_1 % 2 == 0:
                    self.btn.setStyleSheet('QPushButton {background-color: #a29686; '
                                           'font-size: 1px;}')
                if counter_for_cell_colour_2 % 2 == 0 and counter_for_cell_colour_1 % 2 == 0:
                    self.btn.setStyleSheet('QPushButton {background-color: #322e2b; '
                                           'font-size: 1px;}')
                if counter_for_cell_colour_2 % 2 == 0 and counter_for_cell_colour_1 % 2 != 0:
                    self.btn.setStyleSheet('QPushButton {background-color: #a29686; '
                                           'font-size: 1px;}')
                if y != '*':
                    icon.addPixmap(QPixmap(f"figures/{file_names[y]}"))
                    self.btn.setIcon(icon)
                    self.btn.setIconSize(QSize(80, 80))
            self.group.append(intermediate_list)

    def clicked(self):
        self.click_counter += 1
        if self.click_counter % 2 != 0:
            self.icon = self.sender().icon()
            self.move_text += self.sender().text()
            for j in self.group:
                for i in j:
                    if i.text() == self.sender().text():
                        q = QIcon()
                        q.addPixmap(QPixmap('qwerty'))
                        i.setIcon(q)
                        i.setIconSize(QSize(80, 80))
        elif self.click_counter % 2 == 0:
            self.move_text += self.sender().text()
            try:
                if chess.Move.from_uci(self.move_text) in board.legal_moves:
                    self.sender().setIcon(self.icon)
                    self.sender().setIconSize(QSize(80, 80))
                    board.push(chess.Move.from_uci(self.move_text))
                    result = engine.play(board, chess.engine.Limit(time=0.1))
                    board.push(result.move)
                    opponent_move = list()
                    opponent_move.append(str(result.move)[:2])
                    opponent_move.append(str(result.move)[2:4])
                    for j in self.group:
                        for i in j:
                            if i.text() == opponent_move[0]:
                                self.opponent_icon = i.icon()
                                opp_icon = QIcon()
                                opp_icon.addPixmap(QPixmap('qwerty'))
                                i.setIcon(opp_icon)
                                i.setIconSize(QSize(80, 80))
                    for j in self.group:
                        for i in j:
                            if i.text() == opponent_move[1]:
                                i.setIcon(self.opponent_icon)
                                i.setIconSize(QSize(80, 80))
                else:
                    for j in self.group:
                        for i in j:
                            if i.text() == self.move_text[:2]:
                                i.setIcon(self.icon)
                                i.setIconSize(QSize(80, 80))
            except:
                self.buttons_disable()
            if board.is_stalemate():
                self.status.setText('ПАТ')
                self.buttons_disable()
            elif board.is_insufficient_material() or board.can_claim_threefold_repetition():
                self.status.setText('НИЧЬЯ')
                self.buttons_disable()
            elif board.is_checkmate():
                self.status.setText('МАТ')
                self.buttons_disable()
            self.move_text = ''

    def buttons_disable(self):
        for row in self.group:
            for button in row:
                button.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Chess()
    ex.show()
    sys.exit(app.exec())
