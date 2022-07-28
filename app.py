import sys, os, time
from PySide6 import QtCore, QtWidgets, QtGui
from sugurusolver.suguru import Suguru
from sugurusolver.solver import Solver

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.sug_text = QtWidgets.QLabel('', alignment=QtCore.Qt.AlignCenter)
        font = QtGui.QFont('SourceCodePro', 24)
        font.setBold(True)
        self.sug_text.setFont(font)
        
        self.name_box = QtWidgets.QComboBox()
        sug_files = os.listdir(os.getcwd()+'/data/sugurus')
        sug_files.sort(key = lambda file:
            int(''.join([str(i).zfill(3) for i in file.split('.')[0].split('_')[1:]]))
        )
        self.name_box.insertItems(0, [sug.split('.')[0] for sug in sug_files])
        self.name_box.currentTextChanged.connect(self.load_sug)

        self.reset_button = QtWidgets.QPushButton("Reset")
        self.reset_button.clicked.connect(self.load_sug)
        self.next_button = QtWidgets.QPushButton("Next")
        self.next_button.clicked.connect(self.next_sug)
        self.solve_button = QtWidgets.QPushButton("Solve")
        self.solve_button.clicked.connect(self.solve_sug)
        self.nextsolve_button = QtWidgets.QPushButton("Solve next")
        self.nextsolve_button.clicked.connect(self.nextsolve_sug)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.name_box)
        self.layout.addWidget(self.next_button)
        self.layout.addWidget(self.sug_text)
        self.layout.addWidget(self.reset_button)
        self.layout.addWidget(self.solve_button)
        self.layout.addWidget(self.nextsolve_button)
        
        self.load_sug()

    @QtCore.Slot()
    def load_sug(self):
        f = open('data/sugurus/{}.sug'.format(self.name_box.currentText()), 'r')
        self.sug = Suguru(f.read())
        f.close()
        self.update_sug()
        self.solv = Solver(self.sug, step=self.update_sug)
        self.solved = False

    def update_sug(self):
        #time.sleep(0.2) # Doesn't work?
        self.sug_text.setText(str(self.sug))

    @QtCore.Slot()
    def next_sug(self):
        self.name_box.setCurrentIndex(self.name_box.currentIndex()+1)
        self.load_sug()

    @QtCore.Slot()
    def solve_sug(self):
        if not self.solved:
            print('SOLVING:', self.name_box.currentText())
            if self.solv.solve():
                print('SOLVED')
                self.update_sug()
                self.solved = True
            else:
                print('FAILED')

    @QtCore.Slot()
    def nextsolve_sug(self):
        self.next_sug()
        self.solve_sug()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(600, 600)
    widget.show()

    sys.exit(app.exec())
