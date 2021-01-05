import os
from lib.matrix import MatrixAPI
from .emojieditor import Ui_EmojiEditor
from PyQt5.QtWidgets import QDialog, QLabel, QPlainTextEdit
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal
from typing import List, Dict, Optional
from lib.matrix import MXC_RE

EMOJI_DIR = r'emojis'

class EmojiDownloadThread(QThread):
    emojiFinished = pyqtSignal(int, bytes, name="emojiFinished")

    def __init__(self, parent: Optional[QObject], matrix: MatrixAPI, emojilist: Dict) -> None:
        super().__init__(parent)
        self.emojilist = emojilist
        self.matrix = matrix

    def run(self):
        for i, mxc in self.emojilist.items():
            print(mxc)
            emojiBytes = self.getCachedEmoji(mxc, width=128, height=128)
            self.emojiFinished.emit(i, emojiBytes)

    def getCachedEmoji(self, mxcurl, width: int, height: int) -> Optional[bytes]:
        p = os.path
        if not p.lexists(EMOJI_DIR) and not p.isdir(EMOJI_DIR):
            os.mkdir(EMOJI_DIR)

        m = MXC_RE.search(mxcurl)
        if m is None:
            raise Exception("MXC url could not be parsed")
        if len(m.groups()) == 2:
            servername, mediaid = m.groups()
            mediapath = p.join(EMOJI_DIR, mediaid + ".bin")
            if p.lexists(mediapath):
                with open(mediapath, 'rb') as f:
                    return f.read()

            emojiBytes = self.matrix.media_get_thumbnail(mxcurl, width=width, height=height)
            with open(mediapath, 'wb') as f:
                f.write(emojiBytes)
            return emojiBytes
            


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
        emoRow = {}
        row = 0
        for k, v in emoticons.items():
            g.addWidget(QPlainTextEdit(k, parent=self), row, 0)
            g.addWidget(QPlainTextEdit(v['url'], parent=self), row, 1)

            emoRow[row] = v["url"]
            row +=1


        def updateRowPixmap(row, bytes):
            pm = QPixmap()
            pm.loadFromData(bytes)
            pm = pm.scaled(128, 128, Qt.KeepAspectRatio)
            preview = QLabel(self)
            preview.setPixmap(pm)
            self.gridLayout.addWidget(preview, row, 2)

        thr = EmojiDownloadThread(self, self.matrix, emoRow)
        thr.emojiFinished.connect(updateRowPixmap)
        thr.start()

        


    

        

    