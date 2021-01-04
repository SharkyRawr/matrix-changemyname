from lib.matrix import MatrixAPI
from .emojieditor import Ui_EmojiEditor
from PyQt5.QtWidgets import QDialog, QLabel, QPlainTextEdit
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from typing import List, Dict


class EmojiEditor(Ui_EmojiEditor, QDialog):
    def __init__(self, matrixapi: MatrixAPI, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowIcon(QIcon(":/icon.png"))

        self.matrix = matrixapi
        self.populateForm()

    def populateForm(self):
        g = self.gridLayout
        emotes = self.matrix.get_account_data(self.matrix.user_id or '', "im.ponies.user_emotes")
        
        emoticons: Dict = emotes['emoticons']
        row = 0
        for k, v in emoticons.items():
            g.addWidget(QPlainTextEdit(k, parent=self), row, 0)
            g.addWidget(QPlainTextEdit(v['url'], parent=self), row, 1)
            
            pm = QPixmap()
            emojiBytes = self.matrix.media_get_thumbnail(v['url'], width=128, height=128)
            pm.loadFromData(emojiBytes)
            pm.scaled(128, 128, Qt.KeepAspectRatio)
            preview = QLabel(self)
            preview.setPixmap(pm)
            g.addWidget(preview, row, 2)
            
            row +=1

    