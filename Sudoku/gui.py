from PyQt5.QtWidgets import QLabel, QPushButton, QMainWindow, QApplication, QLineEdit
from PyQt5.QtGui import QFont
from solver import solve
import sys
import threading
  
class Window(QMainWindow):

    def __init__(self, x=3, y=3):
        super().__init__()
        self.block_sz = [x,y]
        self.size = x*y
        self.setWindowTitle("Sudoku")
        self.setGeometry(100, 100, 800, 800)
        self.UiComponents()
        self.show()
        

    def sudoku_board(self):
        self.board = [[QLineEdit(self) for _ in range(self.size)] for _ in range(self.size)]
        self.fix = [[False for _ in range(self.size)] for _ in range(self.size)]
        x, y = 60, 60
        for i in range(self.size):
            for j in range(self.size):
                self.board[j][i].setGeometry(x*i + 20, y*j + 20, 50, 50)
                self.board[j][i].setFont(QFont('Times', 17))
    
    def UiComponents(self):
        self.sudoku_board()
        self.btn = QPushButton(self)
        self.btn.setText('分析')    
        self.btn.setGeometry(600, 20, 120, 80)
        self.btn.clicked.connect(self.solve_thread)
        
        self.btn2 = QPushButton(self)
        self.btn2.setText('清除')    
        self.btn2.setGeometry(600, 100, 120, 80)
        self.btn2.clicked.connect(self.clear)
    
    def solve_number(self):
        numf = lambda x: int(x) if x else 0 
        puzzle = [[numf(self.board[j][i].text()) for i in range(self.size)] for j in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if puzzle[i][j]:
                    self.fix[i][j] = True
                else:
                    self.fix[i][j] = False
                    
        can_solve = solve(puzzle, (self.size,self.block_sz[0], self.block_sz[1]))
        if not can_solve:
            print("Can't be solve")
        for i in range(self.size):
            for j in range(self.size):
                self.board[i][j].setText(str(puzzle[i][j]))
                
    def solve_thread(self):
        t = threading.Thread(target=self.solve_number)
        t.start()
        
    def clear(self):
        for i in range(self.size):
            for j in range(self.size):
                if not self.fix[i][j]:
                    self.board[i][j].setText('')


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())