
from PyQt6.QtGui import QSyntaxHighlighter
import re
class PythonHighlighter(QSyntaxHighlighter):
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
   