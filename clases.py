from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('San Pablo Pharmacy')
        self.setMinimumSize(300, 200)
        
        mainWidget = QWidget(self)
        layout = QVBoxLayout(mainWidget)
    
        welcomeLabel = QLabel('Welcome to San Pablo Pharmacy' ,self)
        layout.addWidget(welcomeLabel)
        
        label1 = QLabel('Select an option', self)
        layout.addWidget(label1)
        
        button1 = QPushButton('Add an item')
        button1.clicked.connect(self.openNextWindow)
        layout.addWidget(button1)
        
        
        self.setCentralWidget(mainWidget)
        
    def openNextWindow(self):
        self.addItemMenuWindow = addItemMenu(self)
        self.addItemMenuWindow.show()
        self.hide()

class addItemMenu(QWidget):
    def __init__(self,mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.setMinimumSize(300,200)
        layout = QVBoxLayout(self)
        
        label = QLabel('ADD ITEM MENU', self)
        nameLabel = QLabel('Introduce the name')
        self.selectName = QLineEdit()
        self.selectName.returnPressed.connect(self.addItem)
        self.selectName.setReadOnly(False)
        
        
        
        layout.addWidget(label)
        layout.addWidget(nameLabel)
        layout.addWidget(self.selectName)
    
    def addItem(self):
        name = self.selectName.text()
        print(name)
        
app = QApplication([])
mainWindow = MainMenu()
mainWindow.show()
app.exec()