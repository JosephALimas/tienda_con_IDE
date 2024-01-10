###################################################### LIBRARIES ##################################################

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel
import pandas as pd
import csv
import sys
import os
import datetime
import STORE_CLASES as stCl

##################################################### FUNCTIONS ############################################################

################################################## VARIABLES ###############################################################
deskTopApp = QApplication([])
program_running = True
stablishment = stCl.stablishment('DEFAULT')


#################################################### MAIN ##########################################################################



while program_running:
    main_menu_window = stCl.MainMenuWindow()
    main_menu_window.show()
    deskTopApp.exec()
    
    