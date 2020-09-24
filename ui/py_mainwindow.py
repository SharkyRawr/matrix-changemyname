from PyQt5.QtCore import QAbstractListModel, QModelIndex, QObject, QThread, QTimer, QVariant, Qt
from requests.models import HTTPError
from .mainwindow import Ui_MainWindow
from .py_login_dialog import LoginForm
from PyQt5.QtWidgets import QMainWindow, QMessageBox
import json
import typing
from typing import List, Dict, Union


from lib import MatrixAPI, MatrixRoom
matrix = MatrixAPI()


class RoomListModel(QAbstractListModel):
    def __init__(self, parent: typing.Optional['QObject'], rooms: List[str]) -> None:
        super().__init__(parent)
        self.rooms: Dict[str, MatrixRoom] = {r: MatrixRoom(r) for r in rooms}

    def index_to_key(self, index: int) -> str:
        a = list(self.rooms)[index]
        return a

    def rowCount(self, parent: QModelIndex) -> int:
        return len(self.rooms)

    def data(self, index: QModelIndex, role: int) -> typing.Any:
        if role != Qt.DisplayRole:
            return QVariant()
        if index.row() > len(self.rooms):
            return QVariant()

        return str(self.rooms[self.index_to_key(index.row())])

    def update_room_name(self, roomid: str) -> bool:
        room = self.rooms[roomid]
        try:
            if (name := matrix.get_room_name(roomid)) is not None:
                print(roomid)
                self.set_room_name(room, name)
                return True
        except HTTPError:
            pass

        return False

    def set_room_name(self, room: Union[MatrixRoom, str], name: str) -> None:
        roomid = room.room_id if type(room) is MatrixRoom else room
        room = self.rooms[roomid]
        room.set_name(name)
        self.rooms[roomid] = room

        row = list(self.rooms.keys()).index(roomid)

        self.dataChanged.emit(
            self.createIndex(row, 0),
            self.createIndex(row, 0)
        )


class RoomListNameWorker(QThread):
    def __init__(self, parent: typing.Optional['QObject'], roomlistmodel: RoomListModel) -> None:
        super().__init__(parent)
        self.model = roomlistmodel

    def run(self):
        for r in self.model.rooms:
            if not self.model.update_room_name(r):
                print(r)
                try:
                    members = matrix.get_room_members(r)
                    self.model.set_room_name(
                        r, "{} with {}".format(r, ', '.join(members)))
                except HTTPError as herr:
                    print(herr)
                    pass

            self.msleep(100)
        print("RoomListNameWorker is done!")


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.txtUserID.setText("<Please Login>")
        self.cmdLogin.clicked.connect(self.show_login_window)

        self.load_if_available()

    def load_if_available(self) -> None:
        try:
            if matrix.load():
                if matrix.user_id and matrix.access_token:
                    self.txtUserID.setText(matrix.user_id)
                    self.matrix_test()

        except Exception as ex:
            QMessageBox.critical(
                self, "Error", "Could not restore settings from settings.json!\n" + str(type(ex)) + ": " + str(ex))

    def matrix_test(self) -> None:
        if (p := matrix.get_presence()) is not None:
            self.statusbar.showMessage("Status: {}, last active: {} seconds ago".format(
                p['presence'], p['last_active_ago']
            ))

            # Populate room list
            if (r := matrix.get_rooms()) is not None:
                model = RoomListModel(self, r)
                self.listRooms.setModel(model)
                # Start fetching room names
                self._t = RoomListNameWorker(self, model)
                self._t.start()

        else:
            QMessageBox.critical(self, "Login failed",
                                 "Matrix login has failed, please login again...")

    def show_login_window(self) -> None:
        global matrix
        dlg = LoginForm(self)
        dlg.updateDefaultsFromMatrix(matrix)

        if dlg.exec_():
            matrix = MatrixAPI(dlg.access_token, dlg.homeserver, dlg.user_id)
            if dlg.chkSave.isChecked():
                matrix.save()
            self.matrix_test()
