from lib.matrix import MatrixAPI
from .emojieditor import Ui_EmojiEditor
from PyQt5.QtWidgets import QDialog, QLabel, QPlainTextEdit
from PyQt5.QtGui import QIcon


class EmojiEditor(Ui_EmojiEditor, QDialog):
    def __init__(self, matrixapi: MatrixAPI, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowIcon(QIcon(":/icon.png"))

        self.matrix = matrixapi
        self.populateForm()

    def populateForm(self):
        l = self.formLayout
        emotes = self.matrix.get_account_data(self.matrix.user_id or '', "im.ponies.user_emotes")
        
        emoticons = emotes['emoticons']
        for k, v in emoticons.items():
            l.addRow(QPlainTextEdit(k, parent=self), QPlainTextEdit(v['url'], parent=self))

    