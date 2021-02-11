import mimetypes
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from lib.matrix import MXC_RE, MatrixAPI
from PyQt5.QtCore import QMutex, QObject, Qt, QThread, pyqtSignal, pyqtSlot, QSize
from PyQt5.QtGui import QIcon, QMovie, QPixmap
from PyQt5.QtWidgets import QDialog, QLabel, QPlainTextEdit

from .emojieditor import Ui_EmojiEditor

EMOJI_DIR = r'emojis'

class EmojiDownloadThread(QThread):
    emojiFinished = pyqtSignal(int, bytes, str, str, name="emojiFinished")
    keepRunning = True

    def __init__(self, parent: Optional[QObject], matrix: MatrixAPI, emojilist: Dict) -> None:
        super().__init__(parent)
        self.emojilist = emojilist
        self.matrix = matrix
        self.keepRunning = True

    def abort_gracefully(self):
        self.keepRunning = False

    def run(self):
        for i, mxc in self.emojilist.items():
            if self.keepRunning == False:
                break

            emojiBytes, mimetype, filepath = self.getCachedEmoji(mxc, width=128, height=128)
            self.emojiFinished.emit(i, emojiBytes, mimetype, filepath)

    def getCachedEmoji(self, mxcurl, width: int, height: int) -> Tuple[bytes, str, str]:
        m = MXC_RE.search(mxcurl)
        if m is None:
            raise Exception("MXC url could not be parsed")
        if len(m.groups()) == 2:
            _, mediaid = m.groups()
            mediapath = Path()
            mediapath = mediapath.joinpath(EMOJI_DIR, mediaid)

            # check if the file is already cached locally
            for p in os.listdir(EMOJI_DIR):
                pm = re.match(r'(.+)\.(.+)', p)
                if pm:
                    filename, ext = pm.groups()
                    if mediaid in filename:
                        print("Cached emoji", mediaid)
                        mimetype, _ = mimetypes.guess_type(p)
                        mimetype = mimetype or 'application/octet-stream'
                        with open(os.path.join(EMOJI_DIR, p), 'rb') as f:
                            return f.read(), mimetype, os.path.join(EMOJI_DIR, p),
            
            print("Downloading emoji", mediaid)
            emojiBytes, content_type = self.matrix.media_get_thumbnail(mxcurl, width=width, height=height)
            ext = mimetypes.guess_extension(content_type) or '.bin'
            mediapath = mediapath.with_suffix(ext)

            with open(str(mediapath), 'wb') as f:
                f.write(emojiBytes)
            return emojiBytes, content_type, str(mediapath)
        raise Exception("we fell through, what are we doing here??")
            


class EmojiEditor(Ui_EmojiEditor, QDialog):
    updateRowMutex = QMutex()

    def __init__(self, matrixapi: MatrixAPI, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowIcon(QIcon(":/icon.png"))
        self.updateRowMutex = QMutex()

        if not os.path.lexists(EMOJI_DIR) and not os.path.isdir(EMOJI_DIR):
            os.mkdir(EMOJI_DIR)

        self.matrix = matrixapi
        self.populateForm()

    @pyqtSlot()
    def closeEvent(self, event):
        self.emoji_dl_thr.abort_gracefully()
        self.emoji_dl_thr.wait(1000)
        event.accept()

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


        def updateRowPixmap(row, bytes, mimetype, filepath):
            preview = QLabel(self)
            preview.setMinimumSize(128, 128)
            preview.setMaximumSize(128, 128)

            if 'image/gif' in mimetype:
                movie = QMovie(filepath)
                # @todo: movie.setScaledSize() to something aspect ratio correct
                preview.setMovie(movie)
                movie.start()
            else:
                pm = QPixmap()
                pm.loadFromData(bytes)
                pm = pm.scaled(128, 128, Qt.KeepAspectRatio)    
                preview.setPixmap(pm)

            self.updateRowMutex.lock()
            self.gridLayout.addWidget(preview, row, 2)
            self.updateRowMutex.unlock()
        

        self.emoji_dl_thr = EmojiDownloadThread(self, self.matrix, emoRow)
        self.emoji_dl_thr.emojiFinished.connect(updateRowPixmap)
        self.emoji_dl_thr.start()

