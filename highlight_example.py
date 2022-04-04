import sys
import re
from PyQt6.QtWidgets import QApplication, QWidget, QPlainTextEdit, \
                            QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontDatabase, QColor, QSyntaxHighlighter, QTextCharFormat, QIcon


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


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 1200, 800
        self.setMinimumSize(self.window_width, self.window_height)
        self.setStyleSheet('''
            QWidget {
                font-size: 30px;
            }
        ''')

        self.setWindowIcon(QIcon('index.png'))

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet("background-color:#121212; color:#ffffff")

        self.highlighter = Highlighter()

        self.setUpEditor()
        self.layout.addWidget(self.editor)


    def setUpEditor(self):
        # define pattern rule #1: highlight class header
        class_format = QTextCharFormat()
        class_format.setForeground(QColor(0,0,255))
        class_format.setFontWeight(350)
        pattern = r'^\s*class\s+\w+\(.*$'
        self.highlighter.add_mapping(pattern, class_format)

        # pattern #2: function format
        function_format = QTextCharFormat()
        function_format.setForeground(QColor(255,0,0))
        function_format.setFontItalic(True)
        pattern = r'^\s*def\s+\w+\s*\(.*\)\s*:\s*$'
        self.highlighter.add_mapping(pattern, function_format)        

        # pattern 3: comment format
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#77ff77"))
        # pattern = r'^\s*#.*$' # hightlight from the beginning of the line
        pattern = r'#.*$' # just the text
        self.highlighter.add_mapping(pattern, comment_format)

        self.editor = QPlainTextEdit()

        self.highlighter.setDocument(self.editor.document())

if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    app = QApplication(sys.argv)
    
    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')

