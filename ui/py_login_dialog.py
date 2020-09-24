from PyQt5.QtWidgets import QDialog, QMessageBox
from .login_dialog import Ui_LoginForm
from lib import MatrixAPI

class LoginForm(Ui_LoginForm, QDialog):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.is_accepted)


    def is_accepted(self) -> None:
        self.access_token = self.txtAccessToken.toPlainText()
        self.homeserver = self.txtHomeserver.toPlainText()
        self.user_id = self.txtUserID.toPlainText()

    def updateDefaultsFromMatrix(self, matrix: MatrixAPI) -> None:
        self.txtAccessToken.setPlainText(matrix.access_token)
        self.txtUserID.setPlainText(matrix.user_id)
        self.txtHomeserver.setPlainText(matrix.homeserver)

