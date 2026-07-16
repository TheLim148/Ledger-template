from ledger import Ledger

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, 
    QLabel, 
    QFrame,
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QComboBox,
)

class LedgerWindow(QWidget):
    def __init__(self):
        super().__init__()

        self._ledger = Ledger()
        
        self.setWindowTitle("Ledger")
        self.resize(400, 300)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        self.owner_input = QLineEdit()
        self.owner_input.setPlaceholderText("Enter your name..")
        self.owner_input.setMaximumWidth(300)
        
        self.balance_input = QLineEdit()
        self.balance_input.setPlaceholderText("Enter your start balance..")
        self.balance_input.setMaximumWidth(300)
        
        self.status_label = QLabel()
        self.status_label.setMaximumWidth(300)

        self.create_account_btn = QPushButton("Create Account")
        self.create_account_btn.setMaximumWidth(100)
        self.create_account_btn.clicked.connect(self.handle_create_account)

        self.accounts_combobox = QComboBox()
        self.accounts_combobox.setMaximumWidth(300)

        self.setup_layout()
    
    def setup_layout(self):
        main_layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        form_layout.addRow("Owner: ", self.owner_input)
        form_layout.addRow("Balance: ", self.balance_input)
        form_layout.addRow("Status: ", self.status_label)

        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.create_account_btn)
        main_layout.addWidget(self.accounts_combobox)
        main_layout.addStretch()

    def handle_create_account(self):
        owner = self.owner_input.text()
        raw_balance = self.balance_input.text()

        if owner.strip() == "" or raw_balance == "":
            self.status_label.setText("Fields must not be empty")
            return

        try:
            parsed_balance = int(raw_balance)
        except ValueError:
            self.status_label.setText("Balance must be an integer!")
            return

        try:
            account = self._ledger.create_account(owner, parsed_balance)
            self.accounts_combobox.addItem(f"{account.id} | {account.owner} | {account.balance}", account.id)
            self.clear_inputs()
        except ValueError as err:
            self.status_label.setText(f"{err}")
            return

        self.status_label.setText(f"Account created: {account.owner}, {account.balance}")

    def clear_inputs(self):
        self.owner_input.setText("")
        self.balance_input.setText("")


def main():
    app = QApplication([])

    window = LedgerWindow()

    window.show()
    window.setFocus()

    app.exec()

if __name__ == "__main__":
    main()