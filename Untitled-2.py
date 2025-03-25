import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QMessageBox # type: ignore
from PyQt5.QtCore import Qt # type: ignore
import random

class MineSweeper(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('扫雷游戏')
        self.setGeometry(300, 300, 400, 400)
        
        # 创建中心部件和网格布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.grid = QGridLayout(central_widget)
        
        # 初始化游戏数据
        self.size = 4
        self.mines = 3
        self.buttons = []
        self.mine_positions = []
        self.opened_cells = 0
        
        # 创建按钮网格
        for i in range(self.size):
            row = []
            for j in range(self.size):
                button = QPushButton()
                button.setFixedSize(80, 80)
                button.clicked.connect(lambda checked, x=i, y=j: self.click_button(x, y))
                self.grid.addWidget(button, i, j)
                row.append(button)
            self.buttons.append(row)
            
        # 随机放置地雷
        self.place_mines()
        
    def place_mines(self):
        positions = [(i, j) for i in range(self.size) for j in range(self.size)]
        self.mine_positions = random.sample(positions, self.mines)
        
    def count_adjacent_mines(self, row, col):
        count = 0
        for i in range(max(0, row-1), min(self.size, row+2)):
            for j in range(max(0, col-1), min(self.size, col+2)):
                if (i, j) in self.mine_positions:
                    count += 1
        return count
        
    def click_button(self, row, col):
        if (row, col) in self.mine_positions:
            # 踩到地雷，游戏结束
            self.buttons[row][col].setText('💣')
            self.show_all_mines()
            QMessageBox.information(self, '游戏结束', '很遗憾，你踩到地雷了！')
            self.reset_game()
        else:
            # 显示周围地雷数量
            mines_count = self.count_adjacent_mines(row, col)
            self.buttons[row][col].setText(str(mines_count))
            self.buttons[row][col].setEnabled(False)
            self.opened_cells += 1
            
            # 检查是否胜利
            if self.opened_cells == (self.size * self.size - self.mines):
                QMessageBox.information(self, '恭喜', '你赢了！')
                self.reset_game()
                
    def show_all_mines(self):
        for row, col in self.mine_positions:
            self.buttons[row][col].setText('💣')
            
    def reset_game(self):
        # 重置游戏状态
        self.opened_cells = 0
        self.mine_positions = []
        for i in range(self.size):
            for j in range(self.size):
                self.buttons[i][j].setText('')
                self.buttons[i][j].setEnabled(True)
        self.place_mines()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = MineSweeper()
    game.show()
    sys.exit(app.exec_())
