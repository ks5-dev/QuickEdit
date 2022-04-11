from fileinput import filename
from typing import Text
from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QVBoxLayout, 
QMenu,QCompleter,QHBoxLayout, QFileDialog, QInputDialog ,QPlainTextEdit)
import sys, os
from pathlib import Path
from PySide6.QtGui import QFont, QFontDatabase, QColor, QSyntaxHighlighter, QTextCharFormat, QIcon
import re
import os
import json

#file path

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path_python = "keywords/python.json"
python_file_path = os.path.join(script_dir, rel_path_python)

with open(python_file_path,"r") as f1:
    py_keys = json.load(f1)
    python_keywords = py_keys["basic_keywords"]

rel_path_commands = "commands/run_commands.json"
commands_file_path = os.path.join(script_dir, rel_path_commands)

with open(commands_file_path, "r") as f2:
    commands = json.load(f2)
    run_py = commands["run-python"]
    activate_venv = commands["activate-venv"]

file_options = [
    {"New" : ["New File", "New Folder"]},
    {"Open": ["Open File", "Open Folder"]},
    {"Save": ["Save now", "Save as"]}
]

edit_options = [
    "Copy",
    "Cut",
    "Search and replace",
    "Change to comment",
]

run_options = [
    "Run",
    "Editing commands"
]
completer = [
    "nuncadamavenve"
]

class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._mapping = {}

    def add_mapping(self, pattern, pattern_format):
        self._mapping[pattern] = pattern_format

    def highlightBlock(self, text_block):
        for pattern, fmt in self._mapping.items():
            for match in re.finditer(pattern, text_block):
                start, end = match.span()
                self.setFormat(start, end-start, fmt)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(700,700,600,400)
        self.setWindowTitle("QuickEdit")
        self.setStyleSheet(open("main_stylesheet.css").read())
        self.WidgetDisplay()
        self.curPath = ""

    def WidgetDisplay(self):

        self.mainLayout = QGridLayout()
        self.ribbonLayout = QHBoxLayout()

        self.file_button = QPushButton("File")
        self.file_menu = QMenu()
        self.file_menu.triggered.connect(lambda x : self.fileHandle(x.text()))
        self.file_button.setMenu(self.file_menu)
        
        self.edit_button = QPushButton("Edit")
        self.edit_menu = QMenu()
        self.edit_menu.triggered.connect(lambda x : print(x.text()))
        self.edit_button.setMenu(self.edit_menu)

        self.run_button = QPushButton("Run")
        self.run_menu = QMenu()
        self.run_menu.triggered.connect(lambda x: self.runFile(x.text()))
        self.run_button.setMenu(self.run_menu)

        self.curFileDisplay = QLabel("None")

        self.add_menu(file_options,self.file_menu)
        self.add_menu(edit_options,self.edit_menu)
        self.add_menu(run_options,self.run_menu) 

        self.ribbonLayout.addWidget(self.file_button)
        self.ribbonLayout.addWidget(self.edit_button)
        self.ribbonLayout.addWidget(self.run_button)

        self.mainLayout.addItem(self.ribbonLayout,0,0,1,6)

        self.highlighter = Highlighter()
        self.setUpEditor()
        
        self.mainLayout.addWidget(self.curFileDisplay,0,7)
        self.mainLayout.addWidget(self.TextBox,1,0,10,10)
        
        self.setLayout(self.mainLayout)

    def setUpEditor(self):
        # define pattern rule #1: highlight class header
        '''
        class_format = QTextCharFormat()
        class_format.setForeground(QColor("#00ad9c"))
        class_format.setFontWeight(350)
        pattern = r'^\s*class\s+\w+\(.*$'
        self.highlighter.add_mapping(pattern, class_format)

        # pattern #2: function format
        function_format = QTextCharFormat()
        function_format.setForeground(QColor("#f22c40"))
        function_format.setFontItalic(True)
        pattern = r'^\s*def\s+\w+\s*\(.*\)\s*:\s*$'
        self.highlighter.add_mapping(pattern, function_format)        
        '''
        
        name_format = QTextCharFormat()
        name_format.setForeground(QColor("#a85a32"))
        pattern = r".*[)]\B"
        self.highlighter.add_mapping(pattern, name_format)

        parenthesis_format = QTextCharFormat()
        parenthesis_format.setForeground(QColor("#ffffff"))
        pattern = r'\([^()]*\)'
        self.highlighter.add_mapping(pattern, parenthesis_format)


        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#32a895"))
        keyword_format.setFontWeight(350)
        #pattern = r"(?=(\b" + '\\b|\\b'.join(python_keywords) + r"\b))"
        for i in python_keywords:
            pattern = fr"\b{i}\b"
            self.highlighter.add_mapping(pattern, keyword_format)
        
        # pattern 3: comment format
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#32a834"))
        # pattern = r'^\s*#.*$' # hightlight from the beginning of the line
        pattern = r'#.*$' # just the text
        self.highlighter.add_mapping(pattern, comment_format)
        self.TextBox = QPlainTextEdit()

        self.highlighter.setDocument(self.TextBox.document())

    def add_menu(self,data, menu_obj):
        if isinstance(data,dict):
            for k,v in data.items():
                sub_menu = QMenu(k,menu_obj)
                menu_obj.addMenu(sub_menu)
                self.add_menu(v, sub_menu)
        elif isinstance(data,list):
            for element in data:
                self.add_menu(element, menu_obj)
        else :
            action = menu_obj.addAction(data)
            action.setIconVisibleInMenu(False)

    def fileHandle(self, command):
        if command == "Open File":
            home_dir = str(Path.home())
            fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir)

            if fname[0]:
                self.fileName = os.path.basename(fname[0])
                self.curFileDisplay.setText(self.fileName)
                self.curPath = fname[0]
                f = open(fname[0], 'r')

                with f:
                    
                    data = f.read()
                    self.TextBox.setPlainText(data)
        
        if command == "Save now":
            print(False)
            with open(self.curPath,"w") as f:
                f.write(self.TextBox.toPlainText())
        
        if command == "New File":
            self.curFileDisplay.setText("None")
            self.TextBox.clear()

        if command == "Save as":
            if self.curPath != "":
               fileSaveAs,_ = QFileDialog.getSaveFileName(self,"Save file as","",".txt;;" ".py")
               if fileSaveAs:
                   open(fileSaveAs+_ , "x")
                   with open(fileSaveAs+_, "w") as writeSaveAs:
                       writeSaveAs.write(self.TextBox.toPlainText())

    def runFile(self, command):
        if command == "Run" and self.curPath != "":
            print("True")
            self.curFolder = os.path.dirname(self.curPath)
            if self.fileName.endswith(".py"):
                os.system(run_py + " " + self.fileName)

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.execo())