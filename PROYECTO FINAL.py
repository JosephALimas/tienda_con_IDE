from PyQt6.QtWidgets import QApplication, QCheckBox, QFrame,QMainWindow, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel, QHBoxLayout, QComboBox, QTableWidget , QTableWidgetItem
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import pandas as pd
import csv
import sys
import os
from datetime import datetime
import requests

########################################### CLASES ##################################
title_font = QFont()
title_font.setFamily('Helvetica')
title_font.setPointSize(25)
title_font.setBold(True)

instr_font = QFont()
instr_font.setFamily('Helvetica')
instr_font.setPointSize(20)
instr_font.setBold(True)    

instr2_font = QFont()
instr2_font.setFamily('Helvetica')
instr2_font.setPointSize(15)
instr2_font.setBold(True)    

class stablishment:
    def __init__(self, stablishment_name = '', item_id = 0, batch_id = 0, sale_id = 0) -> None:
        self.sn = stablishment_name
        self.itemList = []
        self.salesList = []
        self.item_id = item_id
        self.batch_id = batch_id
        self.sale_id = sale_id

class mainItem:
    def __init__(self, batch_count = 0,id_p = 0 ,name = '', lab = '', iva = False) -> None:
        self.name = name
        self.lab = lab
        self.iva = iva
        self.id_p = id_p
        self.batch_count = batch_count
        self.batches_list = []

    def printMainItemList(self, pharmacy):
        for index in range(0, len(pharmacy.itemList), 1):
            print(f'Name {pharmacy.itemList[index].name}')
 
class batchItem:
    def __init__(self, name = '',id_b = 0, sku = '', cost = 0.0, sale = 0.0, stock = 0, presentation = '',exp_day = None, exp_month = None, exp_year = None) -> None:
        self.name = name
        self.id_b = id_b
        self.sku = sku
        self.cost = cost
        self.sale = sale
        self.stock = stock
        self.presentation = presentation
        self.exp_day = exp_day
        self.exp_month = exp_month
        self.exp_year = exp_year

class soldItem(batchItem): 
    def __init__(self, amountSold = 0, subtotal = 0.0, total = 0.0):
        self.amountSold = amountSold
        self.subtotal = subtotal
        self.total = total

class Sale:
    def __init__(self, day = '', month = '', year= '', saleid = 0, subutotal = 0.0, total = 0.0, paymentType = '', billing = False):
        self.day = day
        self.month = month
        self.year = year
        self.saleId = saleid
        self.subtotal = subutotal
        self.total = total
        self.paymenType = paymentType
        self.billing = billing 
        self.itemsSold = []
        
        
        
####################################### GUI CLASSES ###################################

class MainMenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Pharmacy system')
        self.setMinimumSize(500, 300)
        
        #LEEMOS LOS CSV
        main_item_CSV = pd.read_csv('mainItemInventory.csv')
        MainItemCSVrowsQuant = main_item_CSV.shape[0]
        
        batch_items_CSV = pd.read_csv('batchInventory.csv')
        BatchItemsCSVrowsQuant = batch_items_CSV.shape[0]
        
        sales_items_CSV = pd.read_csv('salesDF.csv')
        salesItemsCSVrowsQuant = sales_items_CSV.shape[0]
        #
        
        self.pharmacy = stablishment('New Pharmacy')
        
        #BAJAMOS LOS DATOS DE LOS CSV
        
        self.pharmacy.item_id += MainItemCSVrowsQuant
        self.pharmacy.batch_id += BatchItemsCSVrowsQuant
        self.pharmacy.sale_id += salesItemsCSVrowsQuant
        
        #METEMOS LOS DATOS A LA LISTA
        if (MainItemCSVrowsQuant > 0):
            self.pharmacy = DFMainItemsToList(self.pharmacy)
        
        if (BatchItemsCSVrowsQuant > 0):
            self.pharmacy = DFBatchItemsToList(self.pharmacy)
            
        #
        #for i in range(0, len(self.pharmacy.itemList[0].batches_list), 1):
         #   print(self.pharmacy.itemList[0].batches_list[i].presentation)
        #CREAMOS EL WIDGET Y EL LAYOUT PARA EL MENU PRINCIPAL
        self.main_menu_widget = QWidget(self)
        self.main_menu_widget.setStyleSheet("background-color: #e0c49d;")
        self.main_menu_layout = QVBoxLayout(self.main_menu_widget)
        
        
        #INICIALIZAMOS TODOS LOS WIDGETS QUE IRAN EN EL MENU
        #FRAME PARA EL TITULO 
        main_frame = QFrame()
        main_frame.setFrameShape(QFrame.Shape.Box)
        main_frame.setLineWidth(4)
        main_frame.setLayout(QVBoxLayout())
        main_frame.setStyleSheet('color: #3f2b17')
        
        title_frame = QFrame()
        title_frame.setFrameShape(QFrame.Shape.Box) 
        title_frame.setLineWidth(4)
        title_frame.setLayout(QHBoxLayout())
        #LABEL DEL TITULO
        title_label = QLabel('Welcome to UP Pharmacy system')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #804415;")
        title_font
        
        logoLabel = QLabel()
        logoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo = QIcon('logoUP.png')
        logoLabel.setPixmap(logo.pixmap(200, 200))
        
        title_label.setFont(title_font)
        #LABEL DE LA INSTRUCCIÓN INICIAL
        instr_label = QLabel('Select an option')
        instr_label.setStyleSheet('color: #044883;')
        instr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instr_label.setFont(instr_font)
        
        #BOTON 1
        products_button = QPushButton('1.- Products menu')
        products_button.setFont(instr2_font)
        
        products_button.setStyleSheet('border: 2px solid #7e562e')
        products_button.clicked.connect(self.open_opt1_window)
        #BOTON 2
        sales_button = QPushButton('2.- Create a sale')
        sales_button.setFont(instr2_font)
        sales_button.setStyleSheet('border: 2px solid #7e562e')
        sales_button.clicked.connect(self.open_opt2_window)
        #sales_button.clicked.connect(None)
        #BOTON 3
        reports_button = QPushButton('3.- Reports')
        reports_button.setFont(instr2_font)
        reports_button.setStyleSheet('border: 2px solid #7e562e')
        reports_button.clicked.connect(self.open_opt3_window)
        #BOTON 4
        exit_button = QPushButton('Exit')
        exit_button.clicked.connect(self.exit_Program)
        exit_button.setStyleSheet('border: 2px solid #7e562e')
        exit_button.setFont(instr_font)
        
        #AGREGAMOS AL LAYOUT LOS WIDGETS PREVIAMENTE CREADOS
        self.main_menu_layout.addWidget(main_frame)
        main_frame.layout().addWidget(title_frame)
        #main_menu_layout.addWidget(title_frame)
        title_frame.layout().addWidget(title_label)
        title_frame.layout().addWidget(logoLabel)
        main_frame.layout().addWidget(instr_label)
        #main_menu_layout.addWidget(instr_label)
        main_frame.layout().addWidget(products_button)
        main_frame.layout().addWidget(sales_button)
        main_frame.layout().addWidget(reports_button)
        main_frame.layout().addWidget(exit_button)
        self.setCentralWidget(self.main_menu_widget)
    
        
    
    #FUNCIONES PARA ABRIR LAS PESTAÑAS DE CADA SUB MENU
    def open_opt1_window(self):
        self.products_menu_window = ProductsMenuWindow(self)
        self.products_menu_window.show()
        self.hide()
        
    def open_opt2_window(self):
        self.sales_menu_window = SalesMenuWindow(self)
        self.sales_menu_window.show()
        self.hide()
    
    def open_opt3_window(self):
        self.reports_menu_window = ReportsMenuWindow(self)
        self.reports_menu_window.show()
        self.hide()
    
    def exit_Program(self):
        self.close()
         
class ProductsMenuWindow(QWidget):
    def __init__(self, main_menu_window: MainMenuWindow):
        super().__init__()
        self.main_menu_window = main_menu_window
        self.setStyleSheet("background-color: #e0c49d;")
        #print(self.main_menu_window.pharmacy.itemList[0].name)
        
        self.setWindowTitle('Pharmacy system')
        self.setMinimumSize(700, 400)
        menu1_layout = QVBoxLayout(self)
        
        #WIDGETS FOR MENU 1   
        main_frame = QFrame()
        main_frame.setFrameShape(QFrame.Shape.Box)
        main_frame.setLineWidth(4)
        main_frame.setLayout(QVBoxLayout())
        main_frame.setStyleSheet('color: #3f2b17;')
        
        title_frame = QFrame()
        title_frame.setFrameShape(QFrame.Shape.Box) 
        title_frame.setLineWidth(4)
        title_frame.setLayout(QVBoxLayout())
        title_frame.setStyleSheet('color: #3f2b17;')
        
        welcome1_label = QLabel('Select an option')
        welcome1_label.setStyleSheet('color: #044883;')
        welcome1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome1_label.setFont(title_font)
        
        opt1_button = QPushButton('1.- Add an item')
        opt1_button.setFont(instr2_font)
        opt1_button.setStyleSheet('border: 2px solid #7e562e')
        opt1_button.clicked.connect(self.addItem_window)
        
        opt2_button = QPushButton('2.- Edit an item')
        opt2_button.setFont(instr2_font)
        opt2_button.setStyleSheet('border: 2px solid #7e562e')
        opt2_button.clicked.connect(self.editItem_window)
        
        opt3_button = QPushButton('3.- Add a batch')
        opt3_button.setFont(instr2_font)
        opt3_button.setStyleSheet('border: 2px solid #7e562e')
        opt3_button.clicked.connect(self.addBatch_window)
        
        opt4_button = QPushButton('4.- Edit a batch')
        opt4_button.setFont(instr2_font)
        opt4_button.setStyleSheet('border: 2px solid #7e562e')
        opt4_button.clicked.connect(self.editBatch_window)
        
        opt5_button = QPushButton('Return to main menu')
        opt5_button.setStyleSheet('border: 2px solid #7e562e')
        opt5_button.clicked.connect(self.returnToMainMenu)
        opt5_button.setFont(instr_font)
        #ADDING THE WIDGETS TO THE LAYOUT
        menu1_layout.addWidget(main_frame)
        main_frame.layout().addWidget(title_frame)
        title_frame.layout().addWidget(welcome1_label)
        main_frame.layout().addWidget(opt1_button)
        main_frame.layout().addWidget(opt2_button)
        main_frame.layout().addWidget(opt3_button)
        main_frame.layout().addWidget(opt4_button)
        main_frame.layout().addWidget(opt5_button)
        
    def addItem_window(self):
        self.addItemNextWindow = AddItemWindow(self, self.main_menu_window.pharmacy)
        self.addItemNextWindow.show()
        self.hide()
    
    def editItem_window(self):
        self.editItemNextWindow = EditItemWindow(self, self.main_menu_window.pharmacy)
        self.editItemNextWindow.show()
        self.hide()
    
    def addBatch_window(self):
        self.addBatchNextWindow = AddBatchWindow(self, main_menu_window.pharmacy)
        self.addBatchNextWindow.show()
        self.hide()
    
    def editBatch_window(self):
        self.editBatchNextWindow = EditBatchWindow(self, main_menu_window.pharmacy)
        self.editBatchNextWindow.show()
        self.hide()

    def returnToMainMenu(self):
        self.main_menu_window.show()
        self.close()

class AddItemWindow(QWidget):
    def __init__(self, main_menu_window: MainMenuWindow, pharmacy: stablishment):
        super().__init__()
        self.setStyleSheet("background-color: #e0c49d;")
        self.main_menu_window = main_menu_window
        self.pharmacy = pharmacy
        self.setWindowTitle('Pharmacy system')
        self.setMinimumSize(700, 400)
        self.addItemWindow = QVBoxLayout(self)
        
        #print(self.pharmacy.itemList[0].name)
        
        #WIDGETS
        main_frame = QFrame()
        main_frame.setFrameShape(QFrame.Shape.Box)
        main_frame.setLineWidth(4)
        main_frame.setLayout(QVBoxLayout())
        main_frame.setStyleSheet('color: #3f2b17')
        
        title_frame = QFrame()
        title_frame.setFrameShape(QFrame.Shape.Box) 
        title_frame.setLineWidth(4)
        title_frame.setLayout(QVBoxLayout())
        title_frame.setStyleSheet('color: #3f2b17')
        
        instructions_label = QLabel('Add an item')
        instructions_label.setFont(title_font)
        instructions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions_label.setStyleSheet('color: #044883')
        
        instr2_label = QLabel('Introduce all the information for the item:')
        instr2_label.setFont(instr_font)
        instr2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instr2_label.setStyleSheet('color: #7e562e')
        
        name_label = QLabel('Name of the item')
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setFont(instr2_font)
        
        self.lab_lineWriter = QLineEdit()
        self.lab_lineWriter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lab_lineWriter.setReadOnly(False)
        self.lab_lineWriter.textChanged.connect(self.on_text_changed)
        
        lab_label = QLabel('Laboratory of the item')
        lab_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lab_label.setFont(instr2_font)
        self.name_lineWriter = QLineEdit()
        self.name_lineWriter.setReadOnly(False)
        self.name_lineWriter.textChanged.connect(self.on_text_changed)
        
        iva_label = QLabel('Check the box if the item has iva')
        iva_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        iva_label.setFont(instr2_font)
        self.iva_lineWriter = QCheckBox()
        

        self.send_info = QPushButton('Add the item')
        self.send_info.clicked.connect(self.addanItemProcess)
        self.send_info.setFont(instr2_font)
        
        self.exit_button = QPushButton('Return to the main menu')
        self.exit_button.clicked.connect(self.exitToMainMenu)
        self.exit_button.setFont(instr_font)
        
        #AÑADIRLOS AL LAYOUT       
        self.addItemWindow.addWidget(main_frame)
        main_frame.layout().addWidget(title_frame)
        title_frame.layout().addWidget(instructions_label)
        title_frame.layout().addWidget(instr2_label)
        main_frame.layout().addWidget(name_label)
        main_frame.layout().addWidget(self.name_lineWriter)
        main_frame.layout().addWidget(lab_label)
        main_frame.layout().addWidget(self.lab_lineWriter)
        main_frame.layout().addWidget(iva_label)
        main_frame.layout().addWidget(self.iva_lineWriter)
        main_frame.layout().addWidget(self.send_info)
        main_frame.layout().addWidget(self.exit_button)
        
        

    def on_text_changed(self):
        self.send_info.setEnabled(bool(self.name_lineWriter.text()) and bool(self.lab_lineWriter.text()))

    def addanItemProcess(self):
        tempItem = mainItem()
        tempItem.name = self.name_lineWriter.text()
        tempItem.lab = self.lab_lineWriter.text()
        tempItem.iva = bool(self.iva_lineWriter.isChecked())
        tempItem.id_p = main_menu_window.pharmacy.item_id

        
        main_menu_window.pharmacy.itemList.append(tempItem)
        main_menu_window.pharmacy.item_id += 1
        complete_label = QLabel('The item was succesfullly added')
        complete_label.setFont(instr2_font)
        complete_label.setStyleSheet("color: green;")
        self.name_lineWriter.clear()
        self.lab_lineWriter.clear()
        self.iva_lineWriter.setChecked(False)
        self.addItemWindow.addWidget(complete_label)
        
        #AÑADIMOS NUESTRO OBJETO RECIEN CREADO A LOS CSV
        addMainItemToDF(tempItem)
        addMainItemToSoldCSV(tempItem)
        
    def exitToMainMenu(self):
        self.main_menu_window.show()
        self.close()

class EditItemWindow(QWidget):
    def __init__(self, main_menu_window: MainMenuWindow, pharmacy: stablishment ):
        super().__init__()
        self.main_menu_window = main_menu_window
        self.setStyleSheet("background-color: #e0c49d;")
        self.pharmacy = pharmacy
        self.setMinimumSize(500, 300)
        self.setWindowTitle('Pharmacy system')
        self.edit_item_window = QVBoxLayout(self)
        
        #WIDGETS
        main_frame = QFrame()
        main_frame.setFrameShape(QFrame.Shape.Box)
        main_frame.setLineWidth(4)
        main_frame.setLayout(QVBoxLayout())
        
        
        title_frame = QFrame()
        title_frame.setFrameShape(QFrame.Shape.Box) 
        title_frame.setLineWidth(4)
        title_frame.setLayout(QVBoxLayout())
        
        self.title_label = QLabel('Edit an item')
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet('color: #044883;')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.instr_label = QLabel('Select the item')
        self.instr_label.setFont(instr_font)
        
        exit_button = QPushButton('Return to main menu')
        exit_button.clicked.connect(self.exitMainMenu)
        exit_button.setFont(instr_font)
        #print(self.pharmacy.itemList[0].name)
        #AGREGAR LOS WIDGETS AL LAYOUT
        self.edit_item_window.addWidget(main_frame)
        main_frame.layout().addWidget(title_frame)
        title_frame.layout().addWidget(self.title_label)
        title_frame.layout().addWidget(self.instr_label)


        #AÑADIMOS ESOS BOTONES
        for index in range(0, len(self.pharmacy.itemList), 1):
            tempButton = QPushButton(self.pharmacy.itemList[index].name)
            tempButton.setFont(instr2_font)
            tempButton.clicked.connect(self.itemSelected) 
            main_frame.layout().addWidget(tempButton)
            
        main_frame.layout().addWidget(exit_button)




    
    ##########
    def exitMainMenu(self):
        self.main_menu_window.show()
        self.hide()
    
    def itemSelected(self):
        button_pushed = self.sender()
        selected_item = button_pushed.text()
        self.next_window = EditItemProcessWindow(self, self.pharmacy, selected_item)
        self.next_window.show()
        self.hide()
        
class EditItemProcessWindow(QWidget):
    def __init__(self, main_menu_window: MainMenuWindow, pharmacy: stablishment, selected_item = '' ):
        super().__init__()
        self.main_menu_window = main_menu_window
        self.setStyleSheet("background-color: #e0c49d;")
        self.pharmacy = pharmacy
        self.selected_item = selected_item
        self.setMinimumSize(500, 300)
        self.setWindowTitle('Pharmacy system')
        self.edit_item_window = QVBoxLayout(self)
        
        #WIDGETS
        main_frame = QFrame()
        main_frame.setFrameShape(QFrame.Shape.Box)
        main_frame.setLineWidth(4)
        main_frame.setLayout(QVBoxLayout())
          
        title_frame = QFrame()
        title_frame.setFrameShape(QFrame.Shape.Box) 
        title_frame.setLineWidth(4)
        title_frame.setLayout(QVBoxLayout())
        
        self.title_label = QLabel(f'Edit {selected_item}')
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet('color: #044883;')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.instr_label = QLabel('Select the property you want to edit')
        self.instr_label.setFont(instr_font)
        
        self.button1 = QPushButton('Laboratory of the item')
        self.button1.setFont(instr2_font)
        self.button1.clicked.connect(self.modifyLab)
        
        self.button2 = QPushButton('IVA of the item')
        self.button2.setFont(instr2_font)
        self.button2.clicked.connect(self.modifyIva)
        
        self.exit_button = QPushButton('Return to main menu')
        self.exit_button.clicked.connect(self.exitMainMenu)
        self.exit_button.setFont(instr_font)
        #AÑADISMO WIDGETS
        self.edit_item_window.addWidget(main_frame)
        main_frame.layout().addWidget(title_frame)
        title_frame.layout().addWidget(self.title_label)
        title_frame.layout().addWidget(self.instr_label)
        main_frame.layout().addWidget(self.button1)
        main_frame.layout().addWidget(self.button2)
        main_frame.layout().addWidget(self.exit_button)
        
        #print(self.main_menu_window.pharmacy.itemList[0].lab)
        
    def modifyLab(self):
        self.editLabWindow = ModifyLabMainItemWindow(self, self.main_menu_window.pharmacy, self.selected_item)
        self.editLabWindow.show()
        self.hide()
        
    def modifyIva(self):
        self.editIvaWindow = ModifyIvaMainItemWindow(self, self.main_menu_window.pharmacy, self.selected_item)
        self.editIvaWindow.show()
        self.hide()
    
    def exitMainMenu(self):
        self.main_menu_window.show()
        self.hide()

class ModifyLabMainItemWindow(QWidget):
    def __init__(self, main_menu_window: MainMenuWindow, pharmacy: stablishment, selected_item = '' ):
        super().__init__()
        self.main_menu_window = main_menu_window
        self.setStyleSheet("background-color: #e0c49d;")
        self.pharmacy = pharmacy
        self.selected_item = selected_item
        self.setMinimumSize(500, 300)
        self.setWindowTitle('Pharmacy system')
        self.modify_lab_window = QVBoxLayout(self)
        #print(self.selected_item)
        self.ListPositionOfItem = 0
        #CONSEGUIMOS EL VALOR DE LA LISTA DONDE SE ENCUENTRO EL OBJETO A MODIFICAR
        for index in range (0, len(self.main_menu_window.pharmacy.itemList), 1):
            if self.main_menu_window.pharmacy.itemList[index].name == selected_item:
                break
            else:
                self.ListPositionOfItem += 1
        
        #WIDGETS
        self.main_frame = QFrame()
        self.main_frame.setFrameShape(QFrame.Shape.Box)
        self.main_frame.setLineWidth(4)
        self.main_frame.setLayout(QVBoxLayout())
          
        title_frame = QFrame()
        title_frame.setFrameShape(QFrame.Shape.Box) 
        title_frame.setLineWidth(4)
        title_frame.setLayout(QVBoxLayout())
        
        self.title_label = QLabel('Edit laboratory')
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet('color: #044883;')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.instr_label = QLabel('Introduce the new laboratory')
        self.instr_label.setFont(instr_font)

        self.old_name_line = QLabel(f'Old laboratory: {self.main_menu_window.pharmacy.itemList[self.ListPositionOfItem].lab}')
        self.old_name_line.setFont(instr2_font)
        
        self.new_name = QLabel('New laboratory')
        self.new_name.setFont(instr_font)
        
        self.new_name_line = QLineEdit()
        self.new_name_line.setReadOnly(False)
        
        self.send_info = QPushButton('Apply changes')
        self.send_info.clicked.connect(self.changeNameProcess)
        self.send_info.setFont(instr2_font)
        
        self.exit_button = QPushButton('Return to main menu')
        self.exit_button.clicked.connect(self.exitMainMenu)
        self.exit_button.setFont(instr_font)
        #ADD WIDGETS TO THE LAYOUT
        self.modify_lab_window.addWidget(self.main_frame)
        self.main_frame.layout().addWidget(title_frame)
        title_frame.layout().addWidget(self.title_label)
        title_frame.layout().addWidget(self.instr_label)
        self.main_frame.layout().addWidget(self.old_name_line)
        self.main_frame.layout().addWidget(self.new_name)
        self.main_frame.layout().addWidget(self.new_name_line)
        self.main_frame.layout().addWidget(self.send_info)
        self.main_frame.layout().addWidget(self.exit_button)

    def changeNameProcess(self):
        self.main_menu_window.pharmacy.itemList[self.ListPositionOfItem].lab = self.new_name_line.text()
        self.succesMessage = QLabel('The laboratory was updated correctly')
        self.succesMessage.setFont(instr2_font)
        self.succesMessage.setStyleSheet('color: green;')
        self.main_frame.layout().addWidget(self.succesMessage)
        
        self.main_menu_window.pharmacy = changeLabOnDF(self.main_menu_window.pharmacy,self.ListPositionOfItem)

    def exitMainMenu(self):
        self.main_menu_window.show()
        self.hide()
    
class ModifyIvaMainItemWindow(QWidget):
    def __init__(self, main_menu_window: MainMenuWindow, pharmacy: stablishment, selected_item = '' ):
        super().__init__()
        self.setStyleSheet("background-color: #e0c49d;")
        self.main_menu_window = main_menu_window
        self.pharmacy = pharmacy
        self.selected_item = selected_item
        self.setMinimumSize(500, 300)
        self.setWindowTitle('Pharmacy system')
        self.modify_iva_window = QVBoxLayout(self)
        #print(self.selected_item)
        self.ListPositionOfItem = 0
        #CONSEGUIMOS EL VALOR DE LA LISTA DONDE SE ENCUENTRO EL OBJETO A MODIFICAR
        for index in range (0, len(self.main_menu_window.pharmacy.itemList), 1):
            if self.main_menu_window.pharmacy.itemList[index].name == selected_item:
                break
            else:
                self.ListPositionOfItem += 1
        
        #WIDGETS
        self.main_frame = QFrame()
        self.main_frame.setFrameShape(QFrame.Shape.Box)
        self.main_frame.setLineWidth(4)
        self.main_frame.setLayout(QVBoxLayout())
          
        title_frame = QFrame()
        title_frame.setFrameShape(QFrame.Shape.Box) 
        title_frame.setLineWidth(4)
        title_frame.setLayout(QVBoxLayout())
    
        self.title_label = QLabel('Edit the IVA of the item')
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet('color: #044883;')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.instr_label = QLabel('Mark the box if your item has IVA')
        self.instr_label.setFont(instr_font)
        self.instr_label2 = QLabel('or unmark the box if doesnt')
        self.instr_label2.setFont(instr_font)
        
        self.second_layout = QHBoxLayout()
        self.ivaWidget = QWidget(self)
        self.ivaWidget.setLayout(self.second_layout)
        
        self.ivaMessage = QLabel('IVA of the item:')
        self.ivaMessage.setFont(instr2_font)
        
        self.IVAcheckBox = QCheckBox()
        if self.main_menu_window.pharmacy.itemList[self.ListPositionOfItem].iva == True:
            self.IVAcheckBox.setChecked(True)
        
        self.sendNewInfo = QPushButton('Update the IVA')
        self.sendNewInfo.clicked.connect(self.modifyIVAProcess)
        self.sendNewInfo.setFont(instr2_font)
        
        self.exit_button = QPushButton('Return to the main menu')
        self.exit_button.clicked.connect(self.exitToMainMenu)
        self.exit_button.setFont(instr_font)
        
        # AÑADIMOS LOS WIDGETS AL LAYOUT
        self.modify_iva_window.addWidget(self.main_frame)
        self.main_frame.layout().addWidget(title_frame)
        title_frame.layout().addWidget(self.title_label)
        title_frame.layout().addWidget(self.instr_label)
        title_frame.layout().addWidget(self.instr_label2)
        #main_frame.layout().addWidget(self.IVAcheckBox)
        self.main_frame.layout().addWidget(self.ivaWidget)
        self.second_layout.addWidget(self.ivaMessage)
        self.second_layout.addWidget(self.IVAcheckBox)
        self.main_frame.layout().addWidget(self.sendNewInfo)
        self.main_frame.layout().addWidget(self.exit_button)
    
    def modifyIVAProcess(self):
        self.main_menu_window.pharmacy.itemList[self.ListPositionOfItem].iva = bool(self.IVAcheckBox.isChecked())
        self.main_menu_window.pharmacy = changeIvaOnDf(self.main_menu_window.pharmacy, self.ListPositionOfItem)
        confirmationMessage = QLabel('The IVA was updated succesfully')
        confirmationMessage.setFont(instr2_font)
        confirmationMessage.setStyleSheet('color: green;')
        self.main_frame.layout().addWidget(confirmationMessage)
        pass
        
    
    def exitToMainMenu(self):
        self.main_menu_window.show()
        self.close()
     
class AddBatchWindow(QWidget):
    def __init__(self, main_menu_window: MainMenuWindow, pharmacy: stablishment):
        super().__init__()
        self.main_menu_window = main_menu_window
        self.pharmacy = pharmacy
        self.setStyleSheet("background-color: #e0c49d;")
        self.setMinimumSize(500, 300)
        self.setWindowTitle('Pharmacy system')
        self.add_batch_window = QVBoxLayout(self)
        
        #WIDGETS
        main_frame = QFrame()
        main_frame.setFrameShape(QFrame.Shape.Box)
        main_frame.setLineWidth(4)
        main_frame.setLayout(QVBoxLayout())
          
        title_frame = QFrame()
        title_frame.setFrameShape(QFrame.Shape.Box) 
        title_frame.setLineWidth(4)
        title_frame.setLayout(QVBoxLayout())
        
        self.title_label = QLabel('Add a Batch menu')
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet('color: #044883;')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.instr_label = QLabel('Select the item you want to add a batch for')
        self.instr_label.setFont(instr_font)
        
        self.exit_button = QPushButton('Return to the main menu')
        self.exit_button.clicked.connect(self.exitMainMenu)
        self.exit_button.setFont(instr_font)
        
        #AÑADIMOS LOS WIDGETS AL LAYOUT
        self.add_batch_window.addWidget(main_frame)
        main_frame.layout().addWidget(title_frame)
        title_frame.layout().addWidget(self.title_label)
        title_frame.layout().addWidget(self.instr_label)
        
        for index in range(0, len(self.pharmacy.itemList), 1):
            tempButton = QPushButton(self.pharmacy.itemList[index].name)
            tempButton.setFont(instr2_font)
            tempButton.clicked.connect(self.itemSelected) 
            main_frame.layout().addWidget(tempButton)

        main_frame.layout().addWidget(self.exit_button)
        
    def itemSelected(self):
        button_pushed = self.sender()
        selected_item = button_pushed.text()
        self.next_window = AddBatchProcessWindow(self, self.pharmacy, selected_item)
        self.next_window.show()
        self.hide()
    
    def exitMainMenu(self):
        self.main_menu_window.show()
        self.hide()
        
class AddBatchProcessWindow(QWidget):
    def __init__(self, main_menu_window: MainMenuWindow, pharmacy: stablishment, selected_item = '' ):
        super().__init__()
        self.setStyleSheet("background-color: #e0c49d;")
        self.main_menu_window = main_menu_window
        self.pharmacy = pharmacy
        self.selected_item = selected_item
        self.setMinimumSize(500, 300)
        self.setWindowTitle('Pharmacy system')
        self.add_batch_window = QVBoxLayout(self)
        
        
        #WIDGETS
        main_frame = QFrame()
        main_frame.setFrameShape(QFrame.Shape.Box)
        main_frame.setLineWidth(4)
        main_frame.setLayout(QVBoxLayout())
          
        title_frame = QFrame()
        title_frame.setFrameShape(QFrame.Shape.Box) 
        title_frame.setLineWidth(4)
        title_frame.setLayout(QVBoxLayout())
        
        self.title_label = QLabel(f'Add a batch to {self.selected_item}')
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet('color: #044883;')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.instr_label = QLabel('Introduce the information of the new batch')
        self.instr_label.setFont(instr_font)
        
        #
        self.label1 = QLabel('Sku')
        self.label1.setFont(instr2_font)
        self.skuLineEdit = QLineEdit()
        self.skuLineEdit.setReadOnly(False)
        self.skuLineEdit.textChanged.connect(self.on_text_changed)
        
        self.label2 = QLabel('Stock')
        self.label2.setFont(instr2_font)
        self.stockLineEdit = QLineEdit()
        self.stockLineEdit.setReadOnly(False)
        self.stockLineEdit.textChanged.connect(self.on_text_changed)
        
        self.label3 = QLabel('Presentation')
        self.label3.setFont(instr2_font)
        self.presentLineEdit = QLineEdit()
        self.presentLineEdit.setReadOnly(False)
        self.presentLineEdit.textChanged.connect(self.on_text_changed)
        
        self.label4 = QLabel('Cost price')
        self.label4.setFont(instr2_font)
        self.costLineEdit = QLineEdit()
        self.costLineEdit.setReadOnly(False)
        self.costLineEdit.textChanged.connect(self.on_text_changed)
        
        self.label5 = QLabel('Sale price')
        self.label5.setFont(instr2_font)
        self.saleLineEdit = QLineEdit()
        self.saleLineEdit.setReadOnly(False)
        self.saleLineEdit.textChanged.connect(self.on_text_changed)
        
        self.date_label = QLabel('Date of expiracy DD/MM/YYYY')
        self.date_label.setFont(instr2_font)
        self.dateLabelLayout = QHBoxLayout()
        self.month = QLineEdit()
        self.month.textChanged.connect(self.on_text_changed)
        self.month.setReadOnly(False)
        self.year = QLineEdit()
        self.year.textChanged.connect(self.on_text_changed)
        self.year.setReadOnly(False)
        self.day = QLineEdit()
        self.day.setReadOnly(False)
        self.day.textChanged.connect(self.on_text_changed)
        self.dateLabelLayout.addWidget(self.day)
        self.dateLabelLayout.addWidget(self.month)
        self.dateLabelLayout.addWidget(self.year)
        self.dateWIDGET = QWidget(self)
        self.dateWIDGET.setLayout(self.dateLabelLayout)
        
        self.send_info = QPushButton(f'Add the batch to {self.selected_item}')
        self.send_info.clicked.connect(self.addBatchProcess)
        self.send_info.setFont(instr2_font)
        
        self.exit_button = QPushButton('Return to the main menu')
        self.exit_button.clicked.connect(self.exitMainMenu)
        self.exit_button.setFont(instr_font)
        
       
        
        #ADD WIDGETS TO LAYOUT
        self.add_batch_window.addWidget(main_frame)
        main_frame.layout().addWidget(title_frame)
        title_frame.layout().addWidget(self.title_label)
        title_frame.layout().addWidget(self.instr_label)
        main_frame.layout().addWidget(self.label1)
        main_frame.layout().addWidget(self.skuLineEdit)
        main_frame.layout().addWidget(self.label2)
        main_frame.layout().addWidget(self.stockLineEdit)
        main_frame.layout().addWidget(self.label3)
        main_frame.layout().addWidget(self.presentLineEdit)
        main_frame.layout().addWidget(self.label4)
        main_frame.layout().addWidget(self.costLineEdit)
        main_frame.layout().addWidget(self.label5)
        main_frame.layout().addWidget(self.saleLineEdit)
        main_frame.layout().addWidget(self.date_label)
        main_frame.layout().addWidget(self.dateWIDGET)
        main_frame.layout().addWidget(self.send_info)
        main_frame.layout().addWidget(self.exit_button)
        
        
     # ERRORRRRRRRRRRRR   
    def on_text_changed(self):
        self.send_info.setEnabled(bool(self.skuLineEdit.text()) and bool(self.stockLineEdit.text()) and bool(self.presentLineEdit.text()) and bool(self.costLineEdit.text()) and bool(self.saleLineEdit.text())  and bool(self.month.text()) and bool(self.year.text()) and bool(self.day.text()))

    def addBatchProcess(self):
        tempBatch = batchItem()
        tempBatch.id_b = self.main_menu_window.pharmacy.batch_id
        

        tempBatch.sku = self.skuLineEdit.text()
        tempBatch.stock = int(self.stockLineEdit.text())
        tempBatch.presentation = self.presentLineEdit.text()
        tempBatch.cost = float(self.costLineEdit.text())
        tempBatch.sale = float(self.saleLineEdit.text())
        tempBatch.exp_day = self.day.text()
        tempBatch.exp_month = self.month.text()
        tempBatch.exp_year = self.year.text()
        tempBatch.id_b = self.main_menu_window.pharmacy.batch_id
        
        itemLoc = 0
        for index in range (0, len(main_menu_window.pharmacy.itemList), 1):
            if self.selected_item == main_menu_window.pharmacy.itemList[index].name:
                break
            else:
                itemLoc += 1
                
        tempBatch.name = main_menu_window.pharmacy.itemList[itemLoc].name
        main_menu_window.pharmacy.itemList[itemLoc].batches_list.append(tempBatch)
        #print(main_menu_window.pharmacy.itemList[itemLoc].batches_list[0].sku)

        self.main_menu_window.pharmacy = addBatchToDF(tempBatch, self.main_menu_window.pharmacy, itemLoc)
        self.main_menu_window.pharmacy.batch_id += 1
        
        self.skuLineEdit.clear()
        self.stockLineEdit.clear()
        self.presentLineEdit.clear()
        self.costLineEdit.clear()
        self.saleLineEdit.clear()
        self.day.clear()
        self.month.clear()
        self.year.clear()
        
        confirmation_message = QLabel('The batch was succesfully added')
        confirmation_message.setFont(instr2_font)
        confirmation_message.setStyleSheet("color: green;")
        self.add_batch_window.addWidget(confirmation_message)
    def exitMainMenu(self):
        self.main_menu_window.show()
        self.hide()
        
class EditBatchWindow(QWidget):
    def __init__(self, main_menu_window: MainMenuWindow, pharmacy: stablishment):
        super().__init__()
        self.main_menu_window = main_menu_window
        self.setStyleSheet("background-color: #e0c49d;")
        self.pharmacy = pharmacy
        self.setMinimumSize(500, 300)
        self.setWindowTitle('Pharmacy system')
        self.edit_batch_window = QVBoxLayout(self)
        
        #WIDGETS
        main_frame = QFrame()
        main_frame.setFrameShape(QFrame.Shape.Box)
        main_frame.setLineWidth(4)
        main_frame.setLayout(QVBoxLayout())
          
        title_frame = QFrame()
        title_frame.setFrameShape(QFrame.Shape.Box) 
        title_frame.setLineWidth(4)
        title_frame.setLayout(QVBoxLayout())
        
        self.title_label = QLabel('Edit a Batch')
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet('color: #044883;')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.instr_label = QLabel('Select the item')
        self.instr_label.setFont(instr_font)
        
        
        
        self.exit_button = QPushButton('Exit to main menu')
        self.exit_button.clicked.connect(self.exitMainMenu)
        self.exit_button.setFont(instr_font)
        
        #ADD WIDGETS TO THE LAYOUT
        self.edit_batch_window.addWidget(main_frame)
        main_frame.layout().addWidget(title_frame)
        title_frame.layout().addWidget(self.title_label)
        title_frame.layout().addWidget(self.instr_label)

        for index in range(0, len(self.pharmacy.itemList), 1):
            tempButton = QPushButton(self.pharmacy.itemList[index].name)
            tempButton.setFont(instr2_font)
            tempButton.clicked.connect(self.itemSelected) 
            main_frame.layout().addWidget(tempButton)

        main_frame.layout().addWidget(self.exit_button)

    def itemSelected(self):
        button_pushed = self.sender()
        selected_item = button_pushed.text()
        self.next_window = SelectToModWindow(self, self.pharmacy, selected_item)
        self.next_window.show()
        self.hide()
    
    
    def exitMainMenu(self):
        self.main_menu_window.show()
        self.hide()

class SelectToModWindow(QWidget):
    def __init__(self, main_menu_window: MainMenuWindow, pharmacy: stablishment, selected_item):
        super().__init__()
        self.main_menu_window = main_menu_window
        self.pharmacy = pharmacy
        self.selected_item = selected_item
        self.setStyleSheet("background-color: #e0c49d;")
        self.setMinimumSize(500, 300)
        self.setWindowTitle('Pharmacy system')
        self.select_batch_window = QVBoxLayout(self)
        
        rowNemValue = 0
        for index in range (0, len(pharmacy.itemList), 1):
            if selected_item == pharmacy.itemList[index].name:
                break
            else:
                rowNemValue += 1
        
        #WIDGETS
        main_frame = QFrame()
        main_frame.setFrameShape(QFrame.Shape.Box)
        main_frame.setLineWidth(4)
        main_frame.setLayout(QVBoxLayout())
          
        title_frame = QFrame()
        title_frame.setFrameShape(QFrame.Shape.Box) 
        title_frame.setLineWidth(4)
        title_frame.setLayout(QVBoxLayout())
        
        self.title_label = QLabel('Edit a Batch menu')
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet('color: #044883;')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.instr_label = QLabel(f'Select the batch of {self.pharmacy.itemList[rowNemValue].name}')
        self.instr_label.setFont(instr_font)
        
        self.exit_button = QPushButton('Return to the main menu')
        self.exit_button.clicked.connect(self.exitMainMenu)
        self.exit_button.setFont(instr_font)
        
        #AÑADIMOS LOS WIDGETS
        self.select_batch_window.addWidget(main_frame)
        main_frame.layout().addWidget(title_frame)
        title_frame.layout().addWidget(self.title_label)
        title_frame.layout().addWidget(self.instr_label)
        for index in range(0, len(self.pharmacy.itemList[rowNemValue].batches_list), 1):
            tempButton = QPushButton(f'{self.pharmacy.itemList[rowNemValue].batches_list[index].presentation} gm')
            tempButton.setFont(instr2_font)
            tempButton.clicked.connect(self.batchSelected)
            main_frame.layout().addWidget(tempButton)
            #print(len(self.pharmacy.itemList[rowNemValue].batches_list))
        main_frame.layout().addWidget(self.exit_button)

        #for i in range(0, len(self.pharmacy.itemList[rowNemValue].batches_list), 1):
        #    print(self.pharmacy.itemList[rowNemValue].batches_list[i].sale)
        
    def batchSelected(self):
        buttonPushed = self.sender()
        presentationOfButton = buttonPushed.text()
        presentationButtonList = presentationOfButton.split(' ')
        
        self.presentation = presentationButtonList[0]
        self.mainItem = self.selected_item
        
        self.newWindow = ModifyBatchData(self, self.pharmacy, self.presentation, self.mainItem)
        self.newWindow.show()
        self.hide()

    def exitMainMenu(self):
        self.main_menu_window.show()
        self.hide()

class ModifyBatchData(QWidget):
    def __init__(self,main_menu_window: MainMenuWindow, pharmacy: stablishment, presentation = '', mainItem = ''):
        super().__init__()
        self.main_menu_window = main_menu_window
        self.presentation = int(presentation)
        self.mainItem = mainItem
        self.setStyleSheet("background-color: #e0c49d;")
        self.pharmacy = pharmacy
        self.setMinimumSize(500, 300)
        self.setWindowTitle('Pharmacy system')
        self.edit_batch_window = QVBoxLayout(self)
        batchesCSV = pd.read_csv('batchInventory.csv')
        lenBatchesCSV = batchesCSV.shape[0]
        
        self.itemPos = getPositioOfMainItem(self.mainItem,lenBatchesCSV ,self.pharmacy)
        self.batchPos = getPositionOfBatch(self.mainItem,self.presentation,lenBatchesCSV ,self.pharmacy, self.itemPos)
        
        #WIDGETS
        self.main_frame = QFrame()
        self.main_frame.setFrameShape(QFrame.Shape.Box)
        self.main_frame.setLineWidth(4)
        self.main_frame.setLayout(QVBoxLayout())
          
        title_frame = QFrame()
        title_frame.setFrameShape(QFrame.Shape.Box) 
        title_frame.setLineWidth(4)
        title_frame.setLayout(QVBoxLayout())
        
        self.title_label = QLabel(f'Edit {mainItem} batch')
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet('color: #044883;')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.instr_label = QLabel('Select the new information')
        self.instr_label.setFont(instr_font)
    
        self.id_label = QLabel('ID')
        self.id_label.setFont(instr2_font)
        
        self.id_line = QLineEdit()
        self.id_line.setReadOnly(False)
        self.id_line.setText(f'{self.main_menu_window.pharmacy.itemList[self.itemPos].batches_list[self.batchPos].id_b}')
        
        #
        self.sku_label = QLabel('SKU')
        self.sku_label.setFont(instr2_font)
        
        self.sku_line = QLineEdit()
        self.sku_line.setReadOnly(False)
        self.sku_line.setText(f'{self.main_menu_window.pharmacy.itemList[self.itemPos].batches_list[self.batchPos].sku}')
        
        self.cost_label = QLabel('Cost value')
        self.cost_label.setFont(instr2_font)
        
        self.cost_line = QLineEdit()
        self.cost_line.setReadOnly(False)
        self.cost_line.setText(f'{self.main_menu_window.pharmacy.itemList[self.itemPos].batches_list[self.batchPos].cost}')
        
        self.sale_label = QLabel('Sale value')
        self.sale_label.setFont(instr2_font)
        
        self.sale_line = QLineEdit()
        self.sale_line.setReadOnly(False)
        self.sale_line.setText(f'{self.main_menu_window.pharmacy.itemList[self.itemPos].batches_list[self.batchPos].sale}')
        
        self.stock_label = QLabel('Stock')
        self.stock_label.setFont(instr2_font)
        
        self.stock_line = QLineEdit()
        self.stock_line.setReadOnly(False)
        self.stock_line.setText(f'{self.main_menu_window.pharmacy.itemList[self.itemPos].batches_list[self.batchPos].stock}')
        
        self.pre_label = QLabel('Presentation')
        self.pre_label.setFont(instr2_font)
        
        self.pre_line = QLineEdit()
        self.pre_line.setReadOnly(False)
        self.pre_line.setText(f'{self.main_menu_window.pharmacy.itemList[self.itemPos].batches_list[self.batchPos].presentation}')
        
        self.expDay_label = QLabel('Expiration day')
        self.expDay_label.setFont(instr2_font)
        
        self.expDay_line = QLineEdit()
        self.expDay_line.setReadOnly(False)
        self.expDay_line.setText(f'{self.main_menu_window.pharmacy.itemList[self.itemPos].batches_list[self.batchPos].exp_day}')
        
        self.expMonth_label = QLabel('Expiration month')
        self.expMonth_label.setFont(instr2_font)
        
        self.expMonth_line = QLineEdit()
        self.expMonth_line.setReadOnly(False)
        self.expMonth_line.setText(f'{self.main_menu_window.pharmacy.itemList[self.itemPos].batches_list[self.batchPos].exp_month}')
        
        self.expYear_label = QLabel('Expiration year')
        self.expYear_label.setFont(instr2_font)
        
        self.expYear_line = QLineEdit()
        self.expYear_line.setReadOnly(False)
        self.expYear_line.setText(f'{self.main_menu_window.pharmacy.itemList[self.itemPos].batches_list[self.batchPos].exp_year}')
        
        self.submitChangesButton = QPushButton('Submit Changes')
        self.submitChangesButton.clicked.connect(self.editBatchProcess)
        self.submitChangesButton.setFont(instr2_font)
        
        self.exit_button = QPushButton('Exit to menu')
        self.exit_button.setFont(instr_font)
        self.exit_button.clicked.connect(self.exitMainMenu)
    
        # AGREGGAMOSS LOS WIDGETS
        self.edit_batch_window.addWidget(self.main_frame)
        self.main_frame.layout().addWidget(title_frame)
        title_frame.layout().addWidget(self.title_label)
        title_frame.layout().addWidget(self.instr_label)
        self.main_frame.layout().addWidget(self.id_label)
        self.main_frame.layout().addWidget(self.id_line)
        self.main_frame.layout().addWidget(self.sku_label)
        self.main_frame.layout().addWidget(self.sku_line)
        self.main_frame.layout().addWidget(self.cost_label)
        self.main_frame.layout().addWidget(self.cost_line)
        self.main_frame.layout().addWidget(self.sale_label)
        self.main_frame.layout().addWidget(self.sale_line)
        self.main_frame.layout().addWidget(self.stock_label)
        self.main_frame.layout().addWidget(self.stock_line)
        self.main_frame.layout().addWidget(self.pre_label)
        self.main_frame.layout().addWidget(self.pre_line)
        self.main_frame.layout().addWidget(self.expDay_label)
        self.main_frame.layout().addWidget(self.expDay_line)
        self.main_frame.layout().addWidget(self.expMonth_label)
        self.main_frame.layout().addWidget(self.expMonth_line)
        self.main_frame.layout().addWidget(self.expYear_label)
        self.main_frame.layout().addWidget(self.expYear_line)
        self.main_frame.layout().addWidget(self.submitChangesButton)
        self.main_frame.layout().addWidget(self.exit_button)
        
    def editBatchProcess(self):
        self.main_menu_window.pharmacy.itemList[self.itemPos].batches_list[self.batchPos].id_b = int(self.id_line.text())
        self.main_menu_window.pharmacy.itemList[self.itemPos].batches_list[self.batchPos].sku = str(self.sku_line.text())
        self.main_menu_window.pharmacy.itemList[self.itemPos].batches_list[self.batchPos].cost = float(self.cost_line.text())
        self.main_menu_window.pharmacy.itemList[self.itemPos].batches_list[self.batchPos].sale = float(self.sale_line.text())
        self.main_menu_window.pharmacy.itemList[self.itemPos].batches_list[self.batchPos].stock = int(self.stock_line.text())
        self.main_menu_window.pharmacy.itemList[self.itemPos].batches_list[self.batchPos].presentation = int(self.pre_line.text())
        self.main_menu_window.pharmacy.itemList[self.itemPos].batches_list[self.batchPos].exp_day = str(self.expDay_line.text())
        self.main_menu_window.pharmacy.itemList[self.itemPos].batches_list[self.batchPos].exp_month = str(self.expMonth_line.text())
        self.main_menu_window.pharmacy.itemList[self.itemPos].batches_list[self.batchPos].exp_year = int(self.expYear_line.text())
        # AGREGAMOS LOS CAMBIOS AL CSV
        
        confirmationMessage = QLabel('The batch was updated succesfully')
        confirmationMessage.setFont(instr2_font)
        confirmationMessage.setStyleSheet('color: green;')
        self.main_frame.layout().addWidget(confirmationMessage)
        
        self.main_menu_window.pharmacy = self.editBatchOnCSV(self.main_menu_window.pharmacy, self.batchPos, self.itemPos)
        
    def editBatchOnCSV(self, pharmacy: stablishment, batchPos, itemPos):
        batchCSV = pd.read_csv('batchInventory.csv')
        lenBatchCSV = batchCSV.shape[0]
        
        itemRowCont = 0    
        for i in range(0, lenBatchCSV, 1):
            if batchCSV['NAME OF MAIN ITEM'][i] == pharmacy.itemList[itemPos].batches_list[batchPos].name:
                break
            else:
                itemRowCont += 1
        # id
        
        myList = []
        with open('batchInventory.csv', 'r') as file:
            myFile = csv.reader(file)
            for row in myFile:
                if row:
                    myList.append(row)

        newDetail = pharmacy.itemList[itemPos].batches_list[batchPos].id_b 
        myList[itemRowCont+1][1] = newDetail

        with open('batchInventory.csv', 'w+', newline = '') as file:
            myFile = csv.writer(file)
            for row in myList:
                if row: 
                    myFile.writerow(row)
        #SKU
        
        myList = []
        with open('batchInventory.csv', 'r') as file:
            myFile = csv.reader(file)
            for row in myFile:
                if row:
                    myList.append(row)

        newDetail = pharmacy.itemList[itemPos].batches_list[batchPos].sku
        myList[itemRowCont+1][2] = newDetail

        with open('batchInventory.csv', 'w+', newline = '') as file:
            myFile = csv.writer(file)
            for row in myList:
                if row: 
                    myFile.writerow(row)
        
        
        # STOCK
        myList = []
        with open('batchInventory.csv', 'r') as file:
            myFile = csv.reader(file)
            for row in myFile:
                if row:
                    myList.append(row)

        newDetail = pharmacy.itemList[itemPos].batches_list[batchPos].stock
        myList[itemRowCont+1][3] = newDetail

        with open('batchInventory.csv', 'w+', newline = '') as file:
            myFile = csv.writer(file)
            for row in myList:
                if row: 
                    myFile.writerow(row)
        
        myList = []
        with open('batchInventory.csv', 'r') as file:
            myFile = csv.reader(file)
            for row in myFile:
                if row:
                    myList.append(row)

        newDetail = pharmacy.itemList[itemPos].batches_list[batchPos].presentation
        myList[itemRowCont+1][4] = newDetail

        with open('batchInventory.csv', 'w+', newline = '') as file:
            myFile = csv.writer(file)
            for row in myList:
                if row: 
                    myFile.writerow(row)
        
        myList = []
        with open('batchInventory.csv', 'r') as file:
            myFile = csv.reader(file)
            for row in myFile:
                if row:
                    myList.append(row)

        newDetail = pharmacy.itemList[itemPos].batches_list[batchPos].cost
        myList[itemRowCont+1][5] = newDetail

        with open('batchInventory.csv', 'w+', newline = '') as file:
            myFile = csv.writer(file)
            for row in myList:
                if row: 
                    myFile.writerow(row)
        
        myList = []
        with open('batchInventory.csv', 'r') as file:
            myFile = csv.reader(file)
            for row in myFile:
                if row:
                    myList.append(row)

        newDetail = pharmacy.itemList[itemPos].batches_list[batchPos].sale
        myList[itemRowCont+1][6] = newDetail

        with open('batchInventory.csv', 'w+', newline = '') as file:
            myFile = csv.writer(file)
            for row in myList:
                if row: 
                    myFile.writerow(row)
        
        myList = []
        with open('batchInventory.csv', 'r') as file:
            myFile = csv.reader(file)
            for row in myFile:
                if row:
                    myList.append(row)

        newDetail = pharmacy.itemList[itemPos].batches_list[batchPos].exp_day
        myList[itemRowCont+1][7] = newDetail

        with open('batchInventory.csv', 'w+', newline = '') as file:
            myFile = csv.writer(file)
            for row in myList:
                if row: 
                    myFile.writerow(row)
        
        myList = []
        with open('batchInventory.csv', 'r') as file:
            myFile = csv.reader(file)
            for row in myFile:
                if row:
                    myList.append(row)

        newDetail = pharmacy.itemList[itemPos].batches_list[batchPos].exp_month
        myList[itemRowCont+1][8] = newDetail

        with open('batchInventory.csv', 'w+', newline = '') as file:
            myFile = csv.writer(file)
            for row in myList:
                if row: 
                    myFile.writerow(row)
        
        myList = []
        with open('batchInventory.csv', 'r') as file:
            myFile = csv.reader(file)
            for row in myFile:
                if row:
                    myList.append(row)

        newDetail = pharmacy.itemList[itemPos].batches_list[batchPos].exp_year
        myList[itemRowCont+1][9] = newDetail

        with open('batchInventory.csv', 'w+', newline = '') as file:
            myFile = csv.writer(file)
            for row in myList:
                if row: 
                    myFile.writerow(row)
        
        return pharmacy
    def exitMainMenu(self):
        self.main_menu_window.show()
        self.hide()

class SalesMenuWindow(QWidget):
    def __init__(self, main_menu_window: MainMenuWindow):
        super().__init__()
        self.main_menu_window = main_menu_window
        self.setStyleSheet("background-color: #e0c49d;")
        self.setWindowTitle('Pharmacy system')
        self.setMinimumSize(500, 300)
        self.sales_menu_layout = QVBoxLayout(self)
        batchInventoryCSV = pd.read_csv('batchInventory.csv')
        
        
        # CREAMOS UNN OBJETO SALE TEMPORAL QUE LEUGO METEREMOS EN LA LISTA DE LA FARMACIA
        self.tempSale = Sale()
        self.tempSale.day = TodayDay
        self.tempSale.month = TodayMonth
        self.tempSale.year = TodayYear
        self.tempSale.saleId = self.main_menu_window.pharmacy.sale_id
        
        #WIDGETS FOR MENU 2
        self.main_frame = QFrame()
        self.main_frame.setFrameShape(QFrame.Shape.Box)
        self.main_frame.setLineWidth(4)
        self.main_frame.setLayout(QVBoxLayout())
          
        title_frame = QFrame()
        title_frame.setFrameShape(QFrame.Shape.Box) 
        title_frame.setLineWidth(4)
        title_frame.setLayout(QVBoxLayout())
        
        self.title_label = QLabel('Creating a sale')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet('color: #044883;')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.instruct_label = QLabel('Type the SKU of the item')
        self.instruct_label.setFont(instr_font)
        self.instruct_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        exit2_button = QPushButton('Return to main menu')
        exit2_button.clicked.connect(self.exitToMainMenu)
        exit2_button.setFont(instr_font)
        
        selectorWidget = QWidget()
        selectorWidgetLayout = QHBoxLayout()
        selectorWidget.setLayout(selectorWidgetLayout)
        
        self.itemSelector = QLineEdit()
        self.itemSelector.setReadOnly(False)
        
        addQuant = QPushButton('+')
        addQuant.setFont(instr_font)
        addQuant.setStyleSheet('color: navy')
        addQuant.clicked.connect(self.addOne)
        
        substractQuant = QPushButton('-')
        substractQuant.setFont(instr_font)
        substractQuant.setStyleSheet('color: navy;')
        substractQuant.clicked.connect(self.subsOne)
        
        self.quantLineEdit = QLineEdit('0')
        self.quantLineEdit.setReadOnly(True)
        
        additemConfirmation = QPushButton('Add item to cart')
        additemConfirmation.clicked.connect(self.addItemToCart)
        
        finishSaleConfirmation = QPushButton('Billing')
        finishSaleConfirmation.clicked.connect(self.billingProcess)
        skulist = QLabel('SKU list')
        
        #AÑADIMOS WIDGETS
        
        self.sales_menu_layout.addWidget(self.main_frame)
        self.main_frame.layout().addWidget(title_frame)
        title_frame.layout().addWidget(self.title_label)
        title_frame.layout().addWidget(self.instruct_label)
        selectorWidgetLayout.addWidget(self.itemSelector)
        selectorWidgetLayout.addWidget(addQuant)
        selectorWidgetLayout.addWidget(substractQuant)
        selectorWidgetLayout.addWidget(self.quantLineEdit)
        self.main_frame.layout().addWidget(selectorWidget)
        self.main_frame.layout().addWidget(additemConfirmation)
        self.main_frame.layout().addWidget(finishSaleConfirmation)
        self.main_frame.layout().addWidget(skulist)
        
        
        for index in range (0, batchInventoryCSV.shape[0], 1):
            name = batchInventoryCSV['NAME OF MAIN ITEM'][index] 
            batch_presentation = batchInventoryCSV['PRESENTATION'][index] 
            skuBatch = batchInventoryCSV['SKU'][index] 
            itemLabel = QLabel(f'SKU: {skuBatch} {name}: {batch_presentation} gm')
            #itemLabel.setTextInteractionFlags(itemLabel.textInteractionFlags() | Qt.TextSelectable)
            self.main_frame.layout().addWidget(itemLabel)
            
        
        self.main_frame.layout().addWidget(exit2_button)

    def addOne(self):
        quant = int(self.quantLineEdit.text())
        quant += 1
        self.quantLineEdit.setText(str(quant)) 

    
    def subsOne(self):
        quant = int(self.quantLineEdit.text())
        quant -= 1
        self.quantLineEdit.setText(str(quant)) 

    def addItemToCart(self):
        itemSKU = self.itemSelector.text()
        quantItem = int(self.quantLineEdit.text())
        
        if itemSKU == '':
            errorLabel = QLabel('You havent selected any items yet')
            self.main_frame.layout().addWidget(errorLabel)
        else:
            self.tempSoldItem = soldItem()
            #LEEMOS LA BASE DE DATOS
            batchinvetoryCSV = pd.read_csv('batchInventory.csv')
            batchQuant = batchinvetoryCSV.shape[0]
            
            mainIteminventoryCSV = pd.read_csv('mainItemInventory.csv')
            mainItemQuant = mainIteminventoryCSV.shape[0]
            
            #ENCONTRAMOS EN QUE LINEA SE ENCUENTRA NUESTRO BATCH PARA COMOPRARLO
            batchRowDetector = 0
            for i in range(0, batchQuant, 1):
                if itemSKU == batchinvetoryCSV['SKU'][i]:
                    break
                else:
                    batchRowDetector += 1
            #print(batchRowDetector)
            #ENNCONTRAMOS LA LIEA EN DONDE SE ENCUENTRA EL MAINN ITEM PARA ACCEDER A SUS DATOS
            itemRowDetector = 0
            for i in range(0, mainItemQuant, 1):
                if batchinvetoryCSV['NAME OF MAIN ITEM'][batchRowDetector] == mainIteminventoryCSV['NAME'][i]:
                    break
                else:
                    itemRowDetector += 1
            #print(itemRowDetector)
            # AGREGAMOS LOS VALORES DE COSTO Y DE VENTA
            tempSubtotal = (quantItem * int(batchinvetoryCSV['SALE'][batchRowDetector]))
            self.tempSale.subtotal += tempSubtotal
            
            if  mainIteminventoryCSV['IVA'][itemRowDetector] == True:
                tempTotal = (tempSubtotal * 1.16)
                self.tempSale.total += tempTotal
            else:
                tempTotal = tempSubtotal
                self.tempSale.total += tempTotal
            
            self.itemSelector.clear()
            self.quantLineEdit.setText('0')
            #print(self.tempSale.subtotal)
            #print(self.tempSale.total)        
            
            # LE DAMOS AL SOLD ITEM TODAS LAS PROPIEDADES ANTERIORES A EL
            self.tempSoldItem.name = batchinvetoryCSV['NAME OF MAIN ITEM'][batchRowDetector]
            self.tempSoldItem.amountSold = quantItem
            self.tempSoldItem.subtotal = tempSubtotal
            self.tempSoldItem.total = tempTotal
            self.tempSoldItem.id_b = batchinvetoryCSV['ID'][batchRowDetector]
            self.tempSoldItem.sku = batchinvetoryCSV['SKU'][batchRowDetector]
            self.tempSoldItem.cost = batchinvetoryCSV['COST'][batchRowDetector]
            self.tempSoldItem.sale = batchinvetoryCSV['SALE'][batchRowDetector]
            self.tempSoldItem.stock = batchinvetoryCSV['STOCK'][batchRowDetector]
            self.tempSoldItem.presentation = batchinvetoryCSV['PRESENTATION'][batchRowDetector]
            self.tempSoldItem.exp_day = batchinvetoryCSV['EXP DAY'][batchRowDetector]
            self.tempSoldItem.exp_month = batchinvetoryCSV['EXP MONTH'][batchRowDetector]
            self.tempSoldItem.exp_year = batchinvetoryCSV['EXP YEAR'][batchRowDetector]
            
            self.tempSale.itemsSold.append(self.tempSoldItem)
            
            
            
            #AGREGAMOS UNO EN EL CONTADOR DE NUESTRAS VENTAS TOTALES AL STABLISHMENT
            self.main_menu_window.pharmacy.sale_id += 1
    
    def billingProcess(self):
        if len(self.tempSale.itemsSold) == 0:
            errorLabel = QLabel('You havent selected any items yet')
            self.main_frame.layout().addWidget(errorLabel)
        else:
            self.newWindow = BillingWindow(self, self.main_menu_window.pharmacy, self.tempSale)
            self.newWindow.show()
            self.hide()
    
    def exitToMainMenu(self):
        self.main_menu_window.show()
        self.hide()
       
class BillingWindow(QWidget):
    def __init__(self, main_menu_window: MainMenuWindow, pharmacy: stablishment, tempSale: Sale):
        super().__init__()
        self.main_menu_window = main_menu_window
        self.main_menu_window.pharmacy = pharmacy
        self.setStyleSheet("background-color: #e0c49d;")
        self.tempSale = tempSale
        self.setWindowTitle('Pharmacy system')
        self.setMinimumSize(500, 300)
        self.billing_window_layout = QVBoxLayout(self)
        
        # WIDGETS
        
        main_frame = QFrame()
        main_frame.setFrameShape(QFrame.Shape.Box)
        main_frame.setLineWidth(4)
        main_frame.setLayout(QVBoxLayout())
          
        title_frame = QFrame()
        title_frame.setFrameShape(QFrame.Shape.Box) 
        title_frame.setLineWidth(4)
        title_frame.setLayout(QVBoxLayout())
        
        self.title_label = QLabel('You are about to create a sale')
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet('color: #044883;')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.paymentTypeInstr = QLabel('Select your payment type')
        self.paymentTypeInstr.setFont(instr_font)
        self.paymentTypeInstr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.comboBox = QComboBox(self)
        self.comboBox.addItem('Cash')
        self.comboBox.addItem('Card')
        
        self.billingOption = QLabel('Select your billing option')
        self.billingOption.setFont(instr_font)
        self.billingOption.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.billingComboBox = QComboBox(self)
        self.billingComboBox.addItem('Yes')
        self.billingComboBox.addItem('No')
        
        self.finishButton = QPushButton('Print reciept')
        self.finishButton.clicked.connect(self.printRecieptProcess)
        self.finishButton.setFont(instr2_font)
        
        exit_button = QPushButton('Add more items to the cart')
        exit_button.clicked.connect(self.returnToMainMenu)
        exit_button.setFont(instr_font)
        
        
        #AGREGAMOS LOS WIDGETS
        self.billing_window_layout.addWidget(main_frame)
        main_frame.layout().addWidget(title_frame)
        title_frame.layout().addWidget(self.title_label)
        main_frame.layout().addWidget(self.paymentTypeInstr)
        main_frame.layout().addWidget(self.comboBox)
        main_frame.layout().addWidget(self.billingOption)
        main_frame.layout().addWidget(self.billingComboBox)
        main_frame.layout().addWidget(self.finishButton)
        main_frame.layout().addWidget(exit_button)
       
    def printRecieptProcess(self):
        self.tempSale.paymenType = self.comboBox.currentText()
        self.tempSale.billing = self.billingComboBox.currentText()
        self.main_menu_window.pharmacy.salesList.append(self.tempSale)
        self.newWindow = RecieptWindow(self, self.main_menu_window.pharmacy, self.tempSale)
        self.newWindow.show()
        self.hide()
             
    def returnToMainMenu(self):
        self.main_menu_window.show()
        self.close()
        
class RecieptWindow(QWidget):
    def __init__(self, main_menu_window: MainMenuWindow, pharmacy: stablishment, tempSale: Sale):
        super().__init__()
        self.main_menu_window = main_menu_window
        self.main_menu_window.pharmacy = pharmacy
        self.setStyleSheet("background-color: #e0c49d;")
        self.tempSale = tempSale
        self.setWindowTitle('Pharmacy system')
        self.setMinimumSize(680, 740)
        self.recietp_window = QVBoxLayout(self)
        
        
        # WIDGETS
        
        main_frame = QFrame()
        main_frame.setFrameShape(QFrame.Shape.Box)
        main_frame.setLineWidth(4)
        main_frame.setLayout(QVBoxLayout())
          
        title_frame = QFrame()
        title_frame.setFrameShape(QFrame.Shape.Box) 
        title_frame.setLineWidth(4)
        title_frame.setLayout(QHBoxLayout())
        
        self.titleWidget = QWidget()
        self.titleWidgetLayout = QHBoxLayout()
        self.titleWidget.setLayout(self.titleWidgetLayout)
        
        self.pharmacyName = QLabel('UP Pharmacy')
        self.pharmacyName.setFont(title_font)
        self.pharmacyName.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.titleWidgetLayout.addWidget(self.pharmacyName)
        
        self.dateAndSaleId = QLabel(str(f'ID: {self.tempSale.saleId} Date: {self.tempSale.day}/{self.tempSale.month}/{self.tempSale.year}'))
        self.dateAndSaleId.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.dateAndSaleId.setFont(instr2_font)
        self.titleWidgetLayout.addWidget(self.dateAndSaleId)
        
        self.itemsSoldInfo = QTableWidget()
        self.itemsSoldInfo.setColumnCount(6)
        self.itemsSoldInfo.setHorizontalHeaderLabels(['ID','ITEM','PRICE','QTY.','SUBTOTAL','TOTAL'])
        
        items = []
        for index in range(0, len(self.tempSale.itemsSold), 1):
            # CONSEGUIMOS LOS DEMAS VALORES DEL ITEM PARA METER EN EL DICCIONARIO
            id = self.tempSale.itemsSold[index].id_b
            item = (f'{self.tempSale.itemsSold[index].name} {self.tempSale.itemsSold[index].presentation} gm')
            price = self.tempSale.itemsSold[index].sale
            qty = self.tempSale.itemsSold[index].amountSold
            subtotal = self.tempSale.itemsSold[index].subtotal
            total = self.tempSale.itemsSold[index].total
            # ESSTABLECEMOS LOS VALORES EN UNN DICCIONNARIO
            tempItemDict = {'ID': id, 'Item': item, 'Price': price, 'Qty': qty, 'Subtotal': subtotal, 'Total': total}                        
            items.append(tempItemDict)
        
        
        self.itemsSoldInfo.setRowCount(len(items))

        for row, item in enumerate(items):
            id_item = QTableWidgetItem(str(item['ID']))
            nombre_item = QTableWidgetItem(str(item['Item']))
            precio_item = QTableWidgetItem(str(item['Price']))
            cantidad_item = QTableWidgetItem(str(item['Qty']))
            subtotal_item = QTableWidgetItem(str(item['Subtotal']))
            total_item = QTableWidgetItem(str(item['Total']))

            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            nombre_item.setFlags(nombre_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            precio_item.setFlags(precio_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            cantidad_item.setFlags(cantidad_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            subtotal_item.setFlags(subtotal_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            total_item.setFlags(total_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            
            self.itemsSoldInfo.setItem(row, 0, id_item)
            self.itemsSoldInfo.setItem(row, 1, nombre_item)
            self.itemsSoldInfo.setItem(row, 2, precio_item)
            self.itemsSoldInfo.setItem(row, 3, cantidad_item)
            self.itemsSoldInfo.setItem(row, 4, subtotal_item)
            self.itemsSoldInfo.setItem(row, 5, total_item)
        
        
        self.totalAndSubtotalTable = QTableWidget()
        self.totalAndSubtotalTable.setColumnCount(2)
        self.totalAndSubtotalTable.setRowCount(1)
        self.totalAndSubtotalTable.setHorizontalHeaderLabels(['Subtotal','Total'])
        
        
        subtotalFinal = QTableWidgetItem(str(self.tempSale.subtotal))
        totalFinal = QTableWidgetItem(str(self.tempSale.total))
            
        subtotalFinal.setFlags(subtotalFinal.flags() & ~Qt.ItemFlag.ItemIsEditable)
        totalFinal.setFlags(totalFinal.flags() & ~Qt.ItemFlag.ItemIsEditable)
            
        self.totalAndSubtotalTable.setItem(0, 0, subtotalFinal)
        self.totalAndSubtotalTable.setItem(0, 1, totalFinal)
        
        self.paymentType = QLabel(f'Payment method: {self.tempSale.paymenType} ')
        self.paymentType.setFont(instr2_font)
        self.paymentType.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.billing = QLabel(f'Billing: {self.tempSale.billing}')
        self.billing.setFont(instr2_font)
        self.billing.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.hotizontalWidgetForData = QWidget()
        self.layout3 = QHBoxLayout()
        self.hotizontalWidgetForData.setLayout(self.layout3)
        
        self.verticalWidgetForData = QWidget()
        self.layout4 = QVBoxLayout()
        self.verticalWidgetForData.setLayout(self.layout4)
        
        self.layout3.addWidget(self.verticalWidgetForData)
        
        self.verticalWidgetForData.layout().addWidget(self.paymentType)
        self.verticalWidgetForData.layout().addWidget(self.billing)
        
        self.layout3.addWidget(self.totalAndSubtotalTable)
        
        self.goodbyeMessage = QLabel('Thanks for buying on Up Pharmacy')
        self.goodbyeMessage.setFont(instr2_font)
        self.goodbyeMessage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.goodbyeMessage2 = QLabel('Please, come back soon')
        self.goodbyeMessage2.setFont(instr_font)
        self.goodbyeMessage2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.exit = QPushButton('Return to the main menu')
        self.exit.clicked.connect(self.returnToMainMenu)
        
        # AGREGAMOS AL LAYOUT
        self.recietp_window.addWidget(main_frame)
        main_frame.layout().addWidget(title_frame)
        title_frame.layout().addWidget(self.titleWidget)
        main_frame.layout().addWidget(self.itemsSoldInfo)
        main_frame.layout().addWidget(self.hotizontalWidgetForData)
        main_frame.layout().addWidget(self.goodbyeMessage)
        main_frame.layout().addWidget(self.goodbyeMessage2)
        main_frame.layout().addWidget(self.exit)
        
        # AGREGAMOS LOS DATOS A LA LISTA EN NUESTRO STABLISHMENT
        self.main_menu_window.pharmacy.salesList.append(tempSale)
    
        
        # MODIFICAMOS EL CSV DE BATCHES CON EL NUEVO STOCK
        
        #LEEMOS EL CSV DE BATCHES
        batchCSV = pd.read_csv('batchInventory.csv')
        lenBatchCSV = batchCSV.shape[0]
        
        #para cada item vendido de nuestra lista de itemssold, conseguimos la posicion, luego, modificamos el csv con ese dato nuevo
        for index in range (0, len(self.tempSale.itemsSold), 1):
            for l in range(0, lenBatchCSV, 1):
                if batchCSV['SKU'][l] == self.tempSale.itemsSold[index].sku:
                    changeStockOnDF(self.tempSale, index, l)
                    changeValuesOfSoldItems(self.tempSale, index)
                    
        # MODIFICAMOS EL CSV DE SALES
        self.main_menu_window.pharmacy = addSaleToDf(self.main_menu_window.pharmacy, self.tempSale)
        
   
        
        
        
    def returnToMainMenu(self):
        self.main_menu_window.show()
        self.hide()

class ReportsMenuWindow(QWidget):
    def __init__(self, main_menu_window):
        super().__init__()
        self.setStyleSheet("background-color: #e0c49d;")
        self.main_menu_window = main_menu_window
        self.setWindowTitle('Pharmacy system')
        self.setMinimumSize(500, 300)
        self.menu_layout3 = QVBoxLayout(self)
        
        #WIDGETS FOR MENU 3
        self.main_frame = QFrame()
        self.main_frame.setFrameShape(QFrame.Shape.Box)
        self.main_frame.setLineWidth(4)
        self.main_frame.setStyleSheet('color: #3f2b17;')
        self.main_frame.setLayout(QVBoxLayout())
          
        self.title_frame = QFrame()
        self.title_frame.setFrameShape(QFrame.Shape.Box) 
        self.title_frame.setLineWidth(4)
        self.title_frame.setStyleSheet('color: #3f2b17;')
        self.title_frame.setLayout(QVBoxLayout())
        
        self.title_label = QLabel('Reports menu')
        self.title_label.setStyleSheet('color: #044883;')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(title_font)
        
        
        
        self.instr_label3 = QLabel('Select an option')
        self.instr_label3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instr_label3.setStyleSheet('color: #804415;')
        self.instr_label3.setFont(instr_font)
        
        self.opt1 = QPushButton('1.- Sales management')
        self.opt1.setFont(instr2_font)
        self.opt1.setStyleSheet('border: 2px solid #7e562e')
        self.opt1.clicked.connect(self.opt1Submenu)
        
        self.opt2 = QPushButton('2.- Sold products management')
        self.opt2.setFont(instr2_font)
        self.opt2.setStyleSheet('border: 2px solid #7e562e')
        self.opt2.clicked.connect(self.opt2Submenu)
        
        self.opt3 = QPushButton('3.- Laboratories management')
        self.opt3.setFont(instr2_font)
        self.opt3.setStyleSheet('border: 2px solid #7e562e')
        self.opt3.clicked.connect(self.op3Submenu)
        
        self.opt4 = QPushButton('4.- Inventory management')
        self.opt4.setFont(instr2_font)
        self.opt4.setStyleSheet('border: 2px solid #7e562e')
        self.opt4.clicked.connect(self.op4Submenu)
        
        self.exit3_button = QPushButton('Return to main menu')
        self.exit3_button.setStyleSheet('border: 2px solid #7e562e')
        self.exit3_button.clicked.connect(self.exitToMainMenu)
        self.exit3_button.setFont(instr_font)
        
        #ADDING THE WIDGETS
        self.menu_layout3.addWidget(self.main_frame)
        self.main_frame.layout().addWidget(self.title_frame)
        self.title_frame.layout().addWidget(self.title_label)
        self.title_frame.layout().addWidget(self.instr_label3)
        self.main_frame.layout().addWidget(self.opt1)
        self.main_frame.layout().addWidget(self.opt2)
        self.main_frame.layout().addWidget(self.opt3)
        self.main_frame.layout().addWidget(self.opt4)
        self.main_frame.layout().addWidget(self.exit3_button)
        
    def opt1Submenu(self):
        self.newWindow = SalesReportsWindow(self.main_menu_window, self.main_menu_window.pharmacy)
        self.newWindow.show()
        self.hide()
    
    def opt2Submenu(self):
        self.newWindow = SoldProductsReportsWindow(self.main_menu_window, self.main_menu_window.pharmacy)
        self.newWindow.show()
        self.hide()
    
    def op3Submenu(self):
        self.newWindow = LaboReportsWindow(self.main_menu_window, self.main_menu_window.pharmacy)
        self.newWindow.show()
        self.hide()
    
    def op4Submenu(self):
        self.newWindow = InventoryReportsWindow(self.main_menu_window, self.main_menu_window.pharmacy)
        self.newWindow.show()
        self.hide()
    
    def exitToMainMenu(self):
        self.main_menu_window.show()
        self.hide()
    
class SalesReportsWindow(QWidget):
    def __init__(self, main_menu_window: MainMenuWindow, pharmacy: stablishment ):
        super().__init__()
        self.main_menu_window = main_menu_window
        self.setStyleSheet("background-color: #e0c49d;")
        self.pharmacy = pharmacy
        self.setMinimumSize(500, 300)
        self.setWindowTitle('Pharmacy system')
        self.reportsWindow = QVBoxLayout(self)
        
        #WIDGETS
        main_frame = QFrame()
        main_frame.setFrameShape(QFrame.Shape.Box)
        main_frame.setLineWidth(4)
        main_frame.setStyleSheet('color: #3f2b17')
        main_frame.setLayout(QVBoxLayout())
          
        title_frame = QFrame()
        title_frame.setFrameShape(QFrame.Shape.Box) 
        title_frame.setLineWidth(4)
        title_frame.setStyleSheet('color: #3f2b17')
        title_frame.setLayout(QVBoxLayout())
        
        self.title_label = QLabel('Sales reports')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet('color: #804415;')
        self.title_label.setFont(title_font)
        
        self.instr_label = QLabel('Select your filter')
        self.instr_label.setFont(instr_font)
        self.instr_label.setStyleSheet('color: #044883;')
        self.instr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instr_label.setFont(instr_font)

        self.filterOption = QComboBox(self)
        self.filterOption.setFont(instr2_font)
        self.filterOption.setStyleSheet('border: 2px solid #7e562e')
        self.filterOption.addItem('Daily')
        self.filterOption.addItem('Monthly')
        self.filterOption.addItem('Yearly')
        
        self.setFilterButton = QPushButton('Set the filter')
        self.setFilterButton.clicked.connect(self.applyFilter)
        self.setFilterButton.setFont(instr_font)
        self.setFilterButton.setStyleSheet('border: 2px solid #7e562e')
        
        info_frame = QFrame()
        info_frame.setFrameShape(QFrame.Shape.Box) 
        info_frame.setLineWidth(4)
        info_frame.setStyleSheet('color: #3f2b17')
        info_frame.setLayout(QGridLayout())
        
        self.n_sales = QLabel('Number of sales')
        self.n_sales.setFont(instr2_font)
        self.n_sales.setStyleSheet('color: #3f2b17')
        
        self.n_sales_line = QLineEdit()
        self.n_sales_line.setReadOnly(True)
        self.n_sales_line.setStyleSheet('border: 2px solid #7e562e')
        
        self.n_trans = QLabel('Number of transactions')
        self.n_trans.setFont(instr2_font)
        self.n_trans.setStyleSheet('color: #3f2b17')
        
        self.n_trans_line = QLineEdit()
        self.n_trans_line.setReadOnly(True)
        self.n_trans_line.setStyleSheet('border: 2px solid #7e562e')
        
        self.n_value = QLabel('Average value')
        self.n_value.setFont(instr2_font)
        self.n_value.setStyleSheet('color: #3f2b17')
        
        self.n_value_line = QLineEdit()
        self.n_value_line.setReadOnly(True)
        self.n_value_line.setStyleSheet('border: 2px solid #7e562e')

        self.exit_button = QPushButton('Return to main menu')
        self.exit_button.clicked.connect(self.exitMainMenu)
        self.exit_button.setFont(instr_font)
        
        # AÑADIMOS LOS WIDGETS AL LAYOUT
        self.reportsWindow.addWidget(main_frame)
        main_frame.layout().addWidget(title_frame)
        title_frame.layout().addWidget(self.title_label)
        title_frame.layout().addWidget(self.instr_label)
        main_frame.layout().addWidget(self.filterOption)
        main_frame.layout().addWidget(self.setFilterButton)
        main_frame.layout().addWidget(info_frame)
        info_frame.layout().addWidget(self.n_sales,0,0)
        info_frame.layout().addWidget(self.n_sales_line,0,1)
        info_frame.layout().addWidget(self.n_trans,1,0)
        info_frame.layout().addWidget(self.n_trans_line,1,1)
        info_frame.layout().addWidget(self.n_value,2,0)
        info_frame.layout().addWidget(self.n_value_line,2,1)
        main_frame.layout().addWidget(self.exit_button)
        
    def applyFilter(self):
        itemCSV = pd.read_csv('mainItemInventory.csv')
        lenItemCSV = itemCSV.shape[0]
        
        soldCSV = pd.read_csv('soldItems.csv')
        lenSoldCSV = soldCSV.shape[0]
        
        salesCSV = pd.read_csv('salesDF.csv')
        lensalesCSV = salesCSV.shape[0]
        
        filter = str(self.filterOption.currentText())
        nSales = 0
        nTransactions = 0
        averagValue = 0.0
        
        if filter == 'Daily':
            for index in range(0, lensalesCSV, 1):
                if int(TodayDay) == int(salesCSV['DAY'][index]):
                    nSales += 1
                    nTransactions += 1
                    averagValue += salesCSV['TOTAL'][index]
            
        elif filter == 'Monthly':
            for index in range(0, lensalesCSV, 1):
                if int(TodayMonth) == int(salesCSV['MONTH'][index]):
                    nSales += 1
                    nTransactions += 1
                    averagValue += salesCSV['TOTAL'][index]
        elif filter == 'Yearly':
            for index in range(0, lensalesCSV, 1):
                if int(TodayYear) == int(salesCSV['YEAR'][index]):
                    nSales += 1
                    nTransactions += 1
                    averagValue += salesCSV['TOTAL'][index]
        
        self.n_sales_line.setText(str(nSales))
        self.n_trans_line.setText(str(nTransactions))
        self.n_value_line.setText(str(averagValue))
        
    def exitMainMenu(self):
        self.main_menu_window.show()
        self.hide()
                
class SoldProductsReportsWindow(QWidget):
    def __init__(self, main_menu_window: MainMenuWindow, pharmacy: stablishment ):
        super().__init__()
        self.main_menu_window = main_menu_window
        self.pharmacy = pharmacy
        self.setMinimumSize(500, 740)
        self.setStyleSheet("background-color: #e0c49d;")
        self.setWindowTitle('Pharmacy system')
        self.reportsWindow = QVBoxLayout(self)
        #READ CSV
        soldItemsCSV = pd.read_csv('soldItems.csv')
        lenSoldItemsCSV = soldItemsCSV.shape[0]
        
        inventoryCSV = pd.read_csv('mainItemInventory.csv')
        lenInventoryCSV = inventoryCSV.shape[0] 
        
        #WIDGETS
        main_frame = QFrame()
        main_frame.setFrameShape(QFrame.Shape.Box)
        main_frame.setLineWidth(4)
        main_frame.setStyleSheet('color: #3f2b17')
        main_frame.setLayout(QVBoxLayout())
          
        title_frame = QFrame()
        title_frame.setFrameShape(QFrame.Shape.Box) 
        title_frame.setLineWidth(4)
        title_frame.setStyleSheet('color: #3f2b17')
        title_frame.setLayout(QVBoxLayout())
        
        self.title_label = QLabel('Sold items management')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet('color: #804415;')
        self.title_label.setFont(title_font)
        
        self.instr_label = QLabel('Information of each sold item')
        self.instr_label.setFont(instr_font)
        self.instr_label.setStyleSheet('color: #044883;')
        self.instr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instr_label.setFont(instr_font)

        self.infoTable = QTableWidget()
        self.infoTable.setColumnCount(4)
        self.infoTable.setHorizontalHeaderLabels(['ID', 'ITEM', 'SALES VOLUME', 'REVENUE'])
        
        items = []
        for index in range (0, lenSoldItemsCSV, 1):
            id = inventoryCSV['ID_P'][index]
            name = inventoryCSV['NAME'][index]
            sales_vol = soldItemsCSV['AMOUNT SOLD'][index]
            revenue = soldItemsCSV['REVENUE'][index]
            tempDict = {'id': id, 'name': name, 'sales_vol': sales_vol, 'revenue': revenue}
            
            items.append(tempDict)
            
        self.infoTable.setRowCount(len(items))
        
        for row, item in enumerate(items):
            id = QTableWidgetItem(str(item['id']))
            name = QTableWidgetItem(str(item['name']))
            sales_vol = QTableWidgetItem(str(item['sales_vol']))
            revenue = QTableWidgetItem(str(item['revenue']))

            id.setFlags(id.flags() & ~Qt.ItemFlag.ItemIsEditable)
            name.setFlags(name.flags() & ~Qt.ItemFlag.ItemIsEditable)
            sales_vol.setFlags(sales_vol.flags() & ~Qt.ItemFlag.ItemIsEditable)
            revenue.setFlags(revenue.flags() & ~Qt.ItemFlag.ItemIsEditable)

            
            self.infoTable.setItem(row, 0, id)
            self.infoTable.setItem(row, 1, name)
            self.infoTable.setItem(row, 2, sales_vol)
            self.infoTable.setItem(row, 3, revenue)
            
        self.exit_button = QPushButton('Return to main menu')
        self.exit_button.clicked.connect(self.exitMainMenu)
        self.exit_button.setFont(instr_font)
        
        
        #ADD WIDGETS
        self.reportsWindow.addWidget(main_frame)
        main_frame.layout().addWidget(title_frame)
        title_frame.layout().addWidget(self.title_label)
        title_frame.layout().addWidget(self.instr_label)
        main_frame.layout().addWidget(self.infoTable)
        main_frame.layout().addWidget(self.exit_button)
        
    def exitMainMenu(self):
        self.main_menu_window.show()
        self.hide()
        
class LaboReportsWindow(QWidget):
    def __init__(self, main_menu_window: MainMenuWindow, pharmacy: stablishment ):
        super().__init__()
        self.main_menu_window = main_menu_window
        self.pharmacy = pharmacy
        self.setMinimumSize(565, 740)
        self.setStyleSheet("background-color: #e0c49d;")
        self.setWindowTitle('Pharmacy system')
        self.labReportsWindow = QVBoxLayout(self)
        #LEE LOS CSV
        itemCSV = pd.read_csv('mainItemInventory.csv')
        lenItemCSV = itemCSV.shape[0]
        
        soldCSV = pd.read_csv('soldItems.csv')
        lenSoldCSV = soldCSV.shape[0]
        
        #WIDGETS
        main_frame = QFrame()
        main_frame.setFrameShape(QFrame.Shape.Box)
        main_frame.setLineWidth(4)
        main_frame.setStyleSheet('color: #3f2b17')
        main_frame.setLayout(QVBoxLayout())
          
        title_frame = QFrame()
        title_frame.setFrameShape(QFrame.Shape.Box) 
        title_frame.setLineWidth(4)
        title_frame.setStyleSheet('color: #3f2b17')
        title_frame.setLayout(QVBoxLayout())
        
        self.title_label = QLabel('Laboratory reports')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet('color: #804415;')
        self.title_label.setFont(title_font)
        
        self.instr_label = QLabel('Select your filter')
        self.instr_label.setFont(instr_font)
        self.instr_label.setStyleSheet('color: #044883;')
        self.instr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instr_label.setFont(instr_font)
        
        self.infoTable = QTableWidget()
        self.infoTable.setColumnCount(5)
        self.infoTable.setHorizontalHeaderLabels(['LAB', 'ID','ITEM', 'SALES VOLUME', 'REVENUE'])
        
        
        
        items = []
        for index in range (0, lenSoldCSV, 1):
            lab = itemCSV['LAB'][index]
            id = itemCSV['ID_P'][index]
            name = itemCSV['NAME'][index]
            sales_vol = soldCSV['AMOUNT SOLD'][index]
            revenue = soldCSV['REVENUE'][index]
            tempDict = {'lab': lab ,'id': id, 'name': name, 'sales_vol': sales_vol, 'revenue': revenue}
            
            items.append(tempDict)
            
        self.infoTable.setRowCount(len(items))
        
        for row, item in enumerate(items):
            lab = QTableWidgetItem(str(item['lab']))
            id = QTableWidgetItem(str(item['id']))
            name = QTableWidgetItem(str(item['name']))
            sales_vol = QTableWidgetItem(str(item['sales_vol']))
            revenue = QTableWidgetItem(str(item['revenue']))

            lab.setFlags(id.flags() & ~Qt.ItemFlag.ItemIsEditable)
            id.setFlags(id.flags() & ~Qt.ItemFlag.ItemIsEditable)
            name.setFlags(name.flags() & ~Qt.ItemFlag.ItemIsEditable)
            sales_vol.setFlags(sales_vol.flags() & ~Qt.ItemFlag.ItemIsEditable)
            revenue.setFlags(revenue.flags() & ~Qt.ItemFlag.ItemIsEditable)

            self.infoTable.setItem(row, 0, lab)
            self.infoTable.setItem(row, 1, id)
            self.infoTable.setItem(row, 2, name)
            self.infoTable.setItem(row, 3, sales_vol)
            self.infoTable.setItem(row, 4, revenue)

        self.exit_button = QPushButton('Return to main menu')
        self.exit_button.setFont(instr_font)
        self.exit_button.setStyleSheet('border: 2px solid #7e562e')
        self.exit_button.clicked.connect(self.exitMainMenu)
        
        #ADD WIDGETS
        self.labReportsWindow.addWidget(main_frame)
        main_frame.layout().addWidget(title_frame)
        title_frame.layout().addWidget(self.title_label)
        title_frame.layout().addWidget(self.instr_label)
        main_frame.layout().addWidget(self.infoTable)
        
        
        main_frame.layout().addWidget(self.exit_button)
        
    def exitMainMenu(self):
        self.main_menu_window.show()
        self.hide()
        
class InventoryReportsWindow(QWidget):
    def __init__(self, main_menu_window: MainMenuWindow, pharmacy: stablishment ):
        super().__init__()
        self.main_menu_window = main_menu_window
        self.setStyleSheet("background-color: #e0c49d;")
        self.pharmacy = pharmacy
        self.setMinimumSize(500, 300)
        self.setWindowTitle('Pharmacy system')
        self.inventoryreportsWindow = QVBoxLayout(self)
        #LEE LOS CSV
        itemCSV = pd.read_csv('mainItemInventory.csv')
        lenItemCSV = itemCSV.shape[0]
        
        soldCSV = pd.read_csv('soldItems.csv')
        lenSoldCSV = soldCSV.shape[0]
        
        #WIDGETS
        main_frame = QFrame()
        main_frame.setFrameShape(QFrame.Shape.Box)
        main_frame.setLineWidth(4)
        main_frame.setStyleSheet('color: #3f2b17')
        main_frame.setLayout(QVBoxLayout())
          
        title_frame = QFrame()
        title_frame.setFrameShape(QFrame.Shape.Box) 
        title_frame.setLineWidth(4)
        title_frame.setStyleSheet('color: #3f2b17')
        title_frame.setLayout(QVBoxLayout())
        
        self.title_label = QLabel('Inventory management')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet('color: #804415;')
        self.title_label.setFont(title_font)
        
        self.instr_label = QLabel('Select your filter')
        self.instr_label.setFont(instr_font)
        self.instr_label.setStyleSheet('color: #044883;')
        self.instr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instr_label.setFont(instr_font)
    
        self.nameButton = QPushButton('By name')
        self.nameButton.setFont(instr2_font)
        self.nameButton.setStyleSheet('border: 2px solid #7e562e')
        self.nameButton.clicked.connect(self.nameFilter)
        
        self.skuButton = QPushButton('By SKu')
        self.skuButton.setFont(instr2_font)
        self.skuButton.setStyleSheet('border: 2px solid #7e562e')
        self.skuButton.clicked.connect(self.skuFilter)

        self.exit_button = QPushButton('Return to main menu')
        self.exit_button.setFont(instr_font)
        self.exit_button.setStyleSheet('border: 2px solid #7e562e')
        self.exit_button.clicked.connect(self.exitMainMenu)
        
        # ADD WIDGETS
        self.inventoryreportsWindow.addWidget(main_frame)
        main_frame.layout().addWidget(title_frame)
        title_frame.layout().addWidget(self.title_label)
        title_frame.layout().addWidget(self.instr_label)
        main_frame.layout().addWidget(self.nameButton)
        main_frame.layout().addWidget(self.skuButton)
        main_frame.layout().addWidget(self.exit_button)
    
    def nameFilter(self):
        self.newWindow = nameFilterWindow(self, self.main_menu_window.pharmacy)
        self.newWindow.show()
        self.hide()
    def skuFilter(self):
        self.newWindow = skuFilterWindow(self, self.main_menu_window.pharmacy)
        self.newWindow.show()
        self.hide()

    def exitMainMenu(self):
        self.main_menu_window.show()
        self.hide()
        
class nameFilterWindow(QWidget):
    def __init__(self, main_menu_window: MainMenuWindow, pharmacy: stablishment ):
        super().__init__()
        self.main_menu_window = main_menu_window
        self.pharmacy = pharmacy
        self.setStyleSheet("background-color: #e0c49d;")
        self.setMinimumSize(500, 740)
        self.setWindowTitle('Pharmacy system')
        self.nameReportWindow = QVBoxLayout(self)
        
        #LEE LOS CSV
        self.itemCSV = pd.read_csv('mainItemInventory.csv')
        self.lenItemCSV = self.itemCSV.shape[0]
        
        self.batchCSV = pd.read_csv('batchInventory.csv')
        self.lenbatchCSV = self.batchCSV.shape[0]
        
        #WIDGETS
        self.main_frame = QFrame()
        self.main_frame.setFrameShape(QFrame.Shape.Box)
        self.main_frame.setLineWidth(4)
        self.main_frame.setStyleSheet('color: #3f2b17')
        self.main_frame.setLayout(QVBoxLayout())
          
        self.title_frame = QFrame()
        self.title_frame.setFrameShape(QFrame.Shape.Box) 
        self.title_frame.setLineWidth(4)
        self.title_frame.setStyleSheet('color: #3f2b17')
        self.title_frame.setLayout(QVBoxLayout())
        
        self.title_label = QLabel('Inventory management by name')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet('color: #804415;')
        self.title_label.setFont(title_font)
        
        self.instr_label = QLabel('Introduce the name of the item')
        self.instr_label.setFont(instr_font)
        self.instr_label.setStyleSheet('color: #044883;')
        self.instr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.name_lineEdit = QLineEdit()
        self.name_lineEdit.setFont(instr2_font)
        self.name_lineEdit.setReadOnly(False)
        self.name_lineEdit.setStyleSheet('color: #3f2b17;')
        
        self.submitButton = QPushButton('Search for the item')
        self.submitButton.setFont(instr_font)
        self.submitButton.setStyleSheet('border: 2px solid #7e562e')
        self.submitButton.clicked.connect(self.infoSearching)
        
        self.exit_button = QPushButton('Return to main menu')
        self.exit_button.setFont(instr_font)
        self.exit_button.setStyleSheet('border: 2px solid #7e562e')
        self.exit_button.clicked.connect(self.exitMainMenu)
        
        self.info_frame = QFrame()
        self.info_frame.setFrameShape(QFrame.Shape.Box) 
        self.info_frame.setLineWidth(4)
        self.info_frame.setStyleSheet('color: #3f2b17')
        self.info_frame.setLayout(QGridLayout())
        
        self.errorLabel = QLabel('Error finding the item, please try again')
        self.errorLabel.setFont(instr2_font)
        self.errorLabel.setStyleSheet('color: red;')
        self.errorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # ADD WIDGETS
        self.nameReportWindow.addWidget(self.main_frame)
        self.main_frame.layout().addWidget(self.title_frame)
        self.title_frame.layout().addWidget(self.title_label)
        self.title_frame.layout().addWidget(self.instr_label)
        self.main_frame.layout().addWidget(self.name_lineEdit)
        self.main_frame.layout().addWidget(self.submitButton)
        self.main_frame.layout().addWidget(self.info_frame)
        
        
        
        self.main_frame.layout().addWidget(self.exit_button)
        

        
    def infoSearching(self):
        name_of_mainItem = self.name_lineEdit.text()
        foundControl = False
        
        
        iterationForCoordsInGrid = 0
        for index in range(0, self.lenbatchCSV, 1):
            if name_of_mainItem == self.batchCSV['NAME OF MAIN ITEM'][index]:
                presentation = self.batchCSV['PRESENTATION'][index]
                day =self.batchCSV['EXP DAY'][index]
                month = self.batchCSV['EXP MONTH'][index]
                year = self.batchCSV['EXP YEAR'][index]
                
                self.BatchPre = QLabel('Presentation: ')
                self.BatchPre.setFont(instr2_font)
                self.BatchPre.setStyleSheet('color: #3f2b17;')
                
                self.BatchPre_line = QLineEdit(f'{presentation} gm')
                self.BatchPre_line.setFont(instr2_font)
                self.BatchPre_line.setReadOnly(True)
                self.BatchPre_line.setStyleSheet('color: #3f2b17;')
                
                self.stock = QLabel('Stock: ')
                self.stock.setFont(instr2_font)
                self.stock.setStyleSheet('color: #3f2b17;')
                
                self.stock_line = QLineEdit(str(self.batchCSV['STOCK'][index]))
                self.stock_line.setFont(instr2_font)
                self.stock_line.setReadOnly(True)
                self.stock_line.setStyleSheet('color: #3f2b17;')
                
                self.ExpDate = QLabel('Expiration date: ')
                self.ExpDate.setFont(instr2_font)
                self.ExpDate.setStyleSheet('color: #3f2b17;')
                
                self.ExpDate_line = QLineEdit(f'{day}/{month}/{year}')
                self.ExpDate_line.setFont(instr2_font)
                self.ExpDate_line.setReadOnly(True)
                self.ExpDate_line.setStyleSheet('color: #3f2b17;')
                
                self.info_frame.layout().addWidget(self.BatchPre, iterationForCoordsInGrid,0)
                self.info_frame.layout().addWidget(self.BatchPre_line, iterationForCoordsInGrid,1)
                iterationForCoordsInGrid += 1
                self.info_frame.layout().addWidget(self.stock, iterationForCoordsInGrid,0)
                self.info_frame.layout().addWidget(self.stock_line, iterationForCoordsInGrid,1)
                iterationForCoordsInGrid += 1
                self.info_frame.layout().addWidget(self.ExpDate, iterationForCoordsInGrid,0)
                self.info_frame.layout().addWidget(self.ExpDate_line, iterationForCoordsInGrid,1)
                iterationForCoordsInGrid += 1 
                foundControl = True
        
        if foundControl == False:
            self.main_frame.layout().addWidget(self.errorLabel)   
                
    def exitMainMenu(self):
        self.main_menu_window.show()
        self.hide()

class skuFilterWindow(QWidget):
    def __init__(self, main_menu_window: MainMenuWindow, pharmacy: stablishment ):
        super().__init__()
        self.setStyleSheet("background-color: #e0c49d;")
        self.main_menu_window = main_menu_window
        self.pharmacy = pharmacy
        self.setMinimumSize(500, 500)
        self.setWindowTitle('Pharmacy system')
        self.nameReportWindow = QVBoxLayout(self)
        
        #LEE LOS CSV
        self.itemCSV = pd.read_csv('mainItemInventory.csv')
        self.lenItemCSV = self.itemCSV.shape[0]
        
        self.batchCSV = pd.read_csv('batchInventory.csv')
        self.lenbatchCSV = self.batchCSV.shape[0]
        
        #WIDGETS
        self.main_frame = QFrame()
        self.main_frame.setFrameShape(QFrame.Shape.Box)
        self.main_frame.setLineWidth(4)
        self.main_frame.setStyleSheet('color: #3f2b17')
        self.main_frame.setLayout(QVBoxLayout())
          
        self.title_frame = QFrame()
        self.title_frame.setFrameShape(QFrame.Shape.Box) 
        self.title_frame.setLineWidth(4)
        self.title_frame.setStyleSheet('color: #3f2b17')
        self.title_frame.setLayout(QVBoxLayout())
        
        self.title_label = QLabel('Inventory management by SKU')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet('color: #804415;')
        self.title_label.setFont(title_font)
        
        self.instr_label = QLabel('Introduce the SKU of the item')
        self.instr_label.setFont(instr_font)
        self.instr_label.setStyleSheet('color: #044883;')
        self.instr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.name_lineEdit = QLineEdit()
        self.name_lineEdit.setFont(instr2_font)
        self.name_lineEdit.setReadOnly(False)
        self.name_lineEdit.setStyleSheet('color: #3f2b17;')
        
        self.submitButton = QPushButton('Search for the item')
        self.submitButton.setFont(instr_font)
        self.submitButton.setStyleSheet('border: 2px solid #7e562e')
        self.submitButton.clicked.connect(self.infoSearching)
        
        self.exit_button = QPushButton('Return to main menu')
        self.exit_button.setFont(instr_font)
        self.exit_button.setStyleSheet('border: 2px solid #7e562e')
        self.exit_button.clicked.connect(self.exitMainMenu)
        
        self.info_frame = QFrame()
        self.info_frame.setFrameShape(QFrame.Shape.Box) 
        self.info_frame.setLineWidth(4)
        self.info_frame.setStyleSheet('color: #3f2b17')
        self.info_frame.setLayout(QGridLayout())
        
        self.errorLabel = QLabel('Error finding the item, please try again')
        self.errorLabel.setFont(instr2_font)
        self.errorLabel.setStyleSheet('color: red;')
        self.errorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # ADD WIDGETS
        self.nameReportWindow.addWidget(self.main_frame)
        self.main_frame.layout().addWidget(self.title_frame)
        self.title_frame.layout().addWidget(self.title_label)
        self.title_frame.layout().addWidget(self.instr_label)
        self.main_frame.layout().addWidget(self.name_lineEdit)
        self.main_frame.layout().addWidget(self.submitButton)
        self.main_frame.layout().addWidget(self.info_frame)
        
        
        
        self.main_frame.layout().addWidget(self.exit_button)
        

        
    def infoSearching(self):
        sku_of_item = self.name_lineEdit.text()
        foundControl = False
        
        
        iterationForCoordsInGrid = 0
        for index in range(0, self.lenbatchCSV, 1):
            if sku_of_item == self.batchCSV['SKU'][index]:
                name = self.batchCSV['NAME OF MAIN ITEM'][index]
                presentation = self.batchCSV['PRESENTATION'][index]
                day =self.batchCSV['EXP DAY'][index]
                month = self.batchCSV['EXP MONTH'][index]
                year = self.batchCSV['EXP YEAR'][index]
                
                self.name = QLabel('Name: ')
                self.name.setFont(instr2_font)
                self.name.setStyleSheet('color: #3f2b17;')
                
                self.name_line = QLineEdit(str(name))
                self.name_line.setFont(instr2_font)
                self.name_line.setReadOnly(True)
                self.name_line.setStyleSheet('color: #3f2b17;')
                
                self.BatchPre = QLabel('Presentation: ')
                self.BatchPre.setFont(instr2_font)
                self.BatchPre.setStyleSheet('color: #3f2b17;')
                
                self.BatchPre_line = QLineEdit(f'{presentation} gm')
                self.BatchPre_line.setFont(instr2_font)
                self.BatchPre_line.setReadOnly(True)
                self.BatchPre_line.setStyleSheet('color: #3f2b17;')
                
                self.stock = QLabel('Stock: ')
                self.stock.setFont(instr2_font)
                self.stock.setStyleSheet('color: #3f2b17;')
                
                self.stock_line = QLineEdit(str(self.batchCSV['STOCK'][index]))
                self.stock_line.setFont(instr2_font)
                self.stock_line.setReadOnly(True)
                self.stock_line.setStyleSheet('color: #3f2b17;')
                
                self.ExpDate = QLabel('Expiration date: ')
                self.ExpDate.setFont(instr2_font)
                self.ExpDate.setStyleSheet('color: #3f2b17;')
                
                self.ExpDate_line = QLineEdit(f'{day}/{month}/{year}')
                self.ExpDate_line.setFont(instr2_font)
                self.ExpDate_line.setReadOnly(True)
                self.ExpDate_line.setStyleSheet('color: #3f2b17;')
                
                self.info_frame.layout().addWidget(self.name, iterationForCoordsInGrid,0)
                self.info_frame.layout().addWidget(self.name_line, iterationForCoordsInGrid,1)
                iterationForCoordsInGrid += 1
                self.info_frame.layout().addWidget(self.BatchPre, iterationForCoordsInGrid,0)
                self.info_frame.layout().addWidget(self.BatchPre_line, iterationForCoordsInGrid,1)
                iterationForCoordsInGrid += 1
                self.info_frame.layout().addWidget(self.stock, iterationForCoordsInGrid,0)
                self.info_frame.layout().addWidget(self.stock_line, iterationForCoordsInGrid,1)
                iterationForCoordsInGrid += 1
                self.info_frame.layout().addWidget(self.ExpDate, iterationForCoordsInGrid,0)
                self.info_frame.layout().addWidget(self.ExpDate_line, iterationForCoordsInGrid,1)
                iterationForCoordsInGrid += 1  
                foundControl = True         
            
        if foundControl == False:
            self.main_frame.layout().addWidget(self.errorLabel)   
    def exitMainMenu(self):
        self.main_menu_window.show()
        self.hide()

##################################################### FUNCTIONS ############################################################
def salesFileCheckUp():
    path ='salesDf.csv'
    check_file = os.path.isfile(path)
    if check_file:
        pass
    else:
        with open('salesDf.csv', 'w', newline = '') as salesDf:
            writer = csv.writer(salesDf)
            writer.writerow(['DAY','MONTH','YEAR', 'SALEID', 'ITEMS SOLD', 'PAYMENT TYPE', 'BILLING', 'SUBTOTAL', 'TOTAL'])
            pass
        
    # DE PASO, DESCARGAMOS EL LOGO UP

    url = 'https://www.enroll-u.com/_i/2/7/6/8c464a12-a139-11ea-b8a3-0295ecf211ad.png'
    response = requests.get(url, verify=False)

    with open('logoUP.png', 'wb') as file:
        file.write(response.content)

def MainIteminventarioFileCheckUp():
    path = 'mainItemInventory.csv'
    check_file = os.path.isfile(path)
#print(check_file)

    if check_file:
        #print("FLAG")
        pass
    else:
        with open('mainItemInventory.csv', 'w', newline = '')as inventario:
            writer = csv.writer(inventario)
            writer.writerow(['NAME', 'ID_P','LAB', 'IVA'])
            pass
        
def batchInventoryFileCheckUp():
    path = 'batchInventory.csv'
    check_file = os.path.isfile(path)
#print(check_file)

    if check_file:
        #print("FLAG")
        pass
    else:
        with open('batchInventory.csv', 'w', newline = '')as inventario:
            writer = csv.writer(inventario)
            writer.writerow(['NAME OF MAIN ITEM', 'ID', 'SKU', 'STOCK', 'PRESENTATION', 'COST', 'SALE', 'EXP DAY', 'EXP MONTH','EXP YEAR'])
            pass

def soldItemsFileCheckUP():
    path = 'soldItems.csv'
    check_file = os.path.isfile(path)
    if check_file:
        pass
    else:
        with open('soldItems.csv', 'w', newline = '') as soldItems:
            writer = csv.writer(soldItems)
            writer.writerow(['ITEM', 'AMOUNT SOLD', 'SUBTOTAL', 'TOTAL', 'REVENUE'])

def DFMainItemsToList(pharmacy):
    main_item_CSV = pd.read_csv('mainItemInventory.csv')
    rowsQuant = main_item_CSV.shape[0]
    for index in range (0, rowsQuant, 1):
        tempItem = mainItem()
        tempItem.name = main_item_CSV['NAME'][index]
        tempItem.id_p = main_item_CSV['ID_P'][index]
        tempItem.lab = main_item_CSV['LAB'][index]
        tempItem.iva = main_item_CSV['IVA'][index]

        pharmacy.itemList.append(tempItem)
        pharmacy.item_id += 1
    
    #print(pharmacy.itemList[0].name)
    return pharmacy
    
def DFBatchItemsToList(pharmacy: stablishment):
    batch_items_CSV = pd.read_csv('batchInventory.csv')
    main_item_CSV = pd.read_csv('mainItemInventory.csv')
    BatchRowsQuant = batch_items_CSV.shape[0]
    MainItemRowsQuant = main_item_CSV.shape[0]
    
    for index in range(0, BatchRowsQuant, 1):
        tempBatch = batchItem()
        tempBatch.name = batch_items_CSV['NAME OF MAIN ITEM'][index]
        tempBatch.id_b = batch_items_CSV['ID'][index]
        tempBatch.sku = batch_items_CSV['SKU'][index]
        tempBatch.stock = batch_items_CSV['STOCK'][index]
        tempBatch.presentation = batch_items_CSV['PRESENTATION'][index]
        tempBatch.cost = batch_items_CSV['COST'][index]
        tempBatch.sale = batch_items_CSV['SALE'][index]
        tempBatch.exp_day = batch_items_CSV['EXP DAY'][index]
        tempBatch.exp_month = batch_items_CSV['EXP MONTH'][index]
        tempBatch.exp_year = batch_items_CSV['EXP YEAR'][index]
        
        for i in range(0, MainItemRowsQuant,1):
            if batch_items_CSV['NAME OF MAIN ITEM'][index] == main_item_CSV['NAME'][i]:
                pharmacy.itemList[i].batches_list.append(tempBatch)
        
    return pharmacy

def addMainItemToDF(item):
    with open('mainItemInventory.csv', 'a', newline = '') as inventario_csv:
            writer = csv.writer(inventario_csv)
            nueva_fila = [item.name, item.id_p, item.lab, item.iva ]
            writer.writerow(nueva_fila)

def addMainItemToSoldCSV(item):
    with open('soldItems.csv', 'a', newline = '') as inventario_csv:
            writer = csv.writer(inventario_csv)
            nueva_fila = [item.name,0,0.0,0.0,0 ]
            writer.writerow(nueva_fila)

def addBatchToDF(batch: batchItem, pharmacy: stablishment, itemLoc: int):
    with open('batchInventory.csv', 'a', newline = '') as inventario_csv:
            writer = csv.writer(inventario_csv)
            nueva_fila = [pharmacy.itemList[itemLoc].name, batch.id_b, batch.sku, batch.stock, batch.presentation, batch.cost, batch.sale, batch.exp_day, batch.exp_month, batch.exp_year]
            writer.writerow(nueva_fila)

    return pharmacy

def changeLabOnDF(pharmacy: stablishment, itemRowCont):
    myList = []
    with open('mainItemInventory.csv', 'r') as file:
        myFile = csv.reader(file)
        for row in myFile:
            if row:
                myList.append(row)

    newDetail = pharmacy.itemList[itemRowCont].lab
    myList[itemRowCont+1][2] = newDetail

    with open('mainItemInventory.csv', 'w+', newline = '') as file:
        myFile = csv.writer(file)
        for row in myList:
            if row: 
                myFile.writerow(row)

    return pharmacy

def changeIvaOnDf(pharmacy: stablishment, ListPositionOfItem: int):
    myList = []
    with open('mainItemInventory.csv', 'r') as file:
        myFile = csv.reader(file)
        for row in myFile:
            if row:
                myList.append(row)

    newDetail = pharmacy.itemList[ListPositionOfItem].iva
    myList[ListPositionOfItem+1][3] = newDetail

    with open('mainItemInventory.csv', 'w+', newline = '') as file:
        myFile = csv.writer(file)
        for row in myList:
            if row: 
                myFile.writerow(row)
    
    
    return pharmacy

def changeStockOnDF(sale: Sale, index, l):
    batchCSV = pd.read_csv('batchInventory.csv')
    lenBatchCSV = batchCSV.shape[0]
    
    myList = []
    with open('batchInventory.csv', 'r') as file:
        myFile = csv.reader(file)
        for row in myFile:
            if row:
                myList.append(row)

    newDetail = sale.itemsSold[index].stock - sale.itemsSold[index].amountSold
    myList[l+1][3] = newDetail

    with open('batchInventory.csv', 'w+', newline = '') as file:
        myFile = csv.writer(file)
        for row in myList:
            if row: 
                myFile.writerow(row)

def addSaleToDf(pharmacy: stablishment, sale: Sale):
    itemSoldNames = []
    for index in range(0, len(sale.itemsSold), 1):
        itemSoldNames.append(f'{sale.itemsSold[index].name}:{sale.itemsSold[index].presentation}')
    
    with open('salesDF.csv', 'a', newline = '') as inventario_csv:
        writer = csv.writer(inventario_csv)
        nueva_fila = [sale.day, sale.month, sale.year, sale.saleId, itemSoldNames, sale.paymenType, sale.billing, sale.subtotal, sale.total]
        writer.writerow(nueva_fila)
    return pharmacy

def changeValuesOfSoldItems(sale: Sale, index):
    # LEEMOS EL CSV
    soldItemsCSV = pd.read_csv('soldItems.csv')
    lenSolditemsCSV = soldItemsCSV.shape[0]
    
    batchCSV = pd.read_csv('batchInventory.csv')
    lenbatchCSV = batchCSV.shape[0]
    
    #encontramos la posicion en donde esta el dato que queremos modificar
    itemRowFinder = 0
    for i in range(0, lenSolditemsCSV, 1):
        if sale.itemsSold[index].name == soldItemsCSV['ITEM'][i]:
            break
        else:
            itemRowFinder += 1
            
    #modificamos el AMOUNT SOLD en esa posicion obtenida
    myList = []
    with open('soldItems.csv', 'r') as file:
        myFile = csv.reader(file)
        for row in myFile:
            if row:
                myList.append(row)
    oldDetail = soldItemsCSV['AMOUNT SOLD'][itemRowFinder]
    newDetail = oldDetail + sale.itemsSold[index].amountSold
    myList[itemRowFinder+1][1] = newDetail

    with open('soldItems.csv', 'w+', newline = '') as file:
        myFile = csv.writer(file)
        for row in myList:
            if row: 
                myFile.writerow(row)
     #MODIFICAMOS EL SUBTOTAL
     
    myList = []
    with open('soldItems.csv', 'r') as file:
        myFile = csv.reader(file)
        for row in myFile:
            if row:
                myList.append(row)
    oldDetail = float(soldItemsCSV['SUBTOTAL'][itemRowFinder])
    newDetail = oldDetail + sale.itemsSold[index].subtotal
    myList[itemRowFinder+1][2] = newDetail

    with open('soldItems.csv', 'w+', newline = '') as file:
        myFile = csv.writer(file)
        for row in myList:
            if row: 
                myFile.writerow(row)
     
    # MODIFICAMOS EL TOTAL
    myList = []
    with open('soldItems.csv', 'r') as file:
        myFile = csv.reader(file)
        for row in myFile:
            if row:
                myList.append(row)
    oldDetail = float(soldItemsCSV['TOTAL'][itemRowFinder])
    newDetail = oldDetail + sale.itemsSold[index].total
    myList[itemRowFinder+1][3] = newDetail

    with open('soldItems.csv', 'w+', newline = '') as file:
        myFile = csv.writer(file)
        for row in myList:
            if row: 
                myFile.writerow(row)
                
    # MODIFICAMOS EL REVENUE
                 # obtenemos el dato para agregarlo al csv
    myList = []
    with open('soldItems.csv', 'r') as file:
        myFile = csv.reader(file)
        for row in myFile:
            if row:
                myList.append(row)
    oldDetail = float(soldItemsCSV['REVENUE'][itemRowFinder])
    newDetail = oldDetail + (sale.itemsSold[index].sale - sale.itemsSold[index].cost)
    myList[itemRowFinder+1][4] = newDetail

    with open('soldItems.csv', 'w+', newline = '') as file:
        myFile = csv.writer(file)
        for row in myList:
            if row: 
                myFile.writerow(row)
                            
def getPositioOfMainItem(name ,lenBatchesCSV, pharmacy: stablishment):
    mainItemPos = 0
    for i in range(0, lenBatchesCSV, 1):
        if pharmacy.itemList[i].name == name:
            break
        else:
            mainItemPos += 1
    
    return mainItemPos

def getPositionOfBatch(name, presentation ,lenBatchesCSV, pharmacy: stablishment, mainItemPos):

    batchPos = 0
    for i in range(0, len(pharmacy.itemList[mainItemPos].batches_list),1):
        if presentation == pharmacy.itemList[mainItemPos].batches_list[i].presentation:
            break
        else:
            batchPos += 1
     

    
    return batchPos
  
################################################## VARIABLES ###############################################################

deskTopApp = QApplication([])
program_running = True
todaysDate = datetime.now()
TodayDay = todaysDate.day
TodayMonth = todaysDate.month
TodayYear = todaysDate.year


#################################################### MAIN ##################################################################

MainIteminventarioFileCheckUp()
batchInventoryFileCheckUp()
salesFileCheckUp()
soldItemsFileCheckUP()

main_menu_window = MainMenuWindow()
main_menu_window.setStyleSheet("background-color: #e0c49d;")
#main_menu_window.setStyleSheet("background-color: black;")
main_menu_window.show()
deskTopApp.exec()


# COLORES LISTA

# FONDO
#e0c49d

# TITULO
#804415

#SUBTITULO
#044883

# FRAMES 
#3f2b17

#BORDE DE BOTONES
# 'border: 2px solid #7e562e'

