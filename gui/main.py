from ledger import Ledger
from account import Account

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
    QTableWidget,
    QTableWidgetItem,
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

        self.single_operation_combobox = QComboBox()
        self.single_operation_combobox.setMaximumWidth(300)

        self.from_accounts_combobox = QComboBox()
        self.from_accounts_combobox.setMaximumWidth(300)
        
        self.to_accounts_combobox = QComboBox()
        self.to_accounts_combobox.setMaximumWidth(300)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter amount..")
        self.amount_input.setMaximumWidth(300)

        self.deposit_btn = QPushButton("Deposit")
        self.deposit_btn.setMaximumWidth(100)
        self.deposit_btn.clicked.connect(self.handle_deposit)

        self.withdraw_btn = QPushButton("Withdraw")
        self.withdraw_btn.setMaximumWidth(100)
        self.withdraw_btn.clicked.connect(self.handle_withdraw)

        self.transfer_btn = QPushButton("Transfer")
        self.transfer_btn.setMaximumWidth(100)
        self.transfer_btn.clicked.connect(self.handle_transfer)

        self.table = QTableWidget()
        self.table.setHorizontalHeaderLabels(["Id", "owner", "balance"])
        
        self.seed_demo_accounts()
        self.refresh_ui()
        self.setup_layout()
 
    def setup_layout(self):
        main_layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        form_layout.addRow("Status: ", self.status_label)
        form_layout.addRow("Owner: ", self.owner_input)
        form_layout.addRow("Balance: ", self.balance_input)
        form_layout.addWidget(self.create_account_btn)


        single_operation_layout = QVBoxLayout()
        single_operation_layout.addWidget(QLabel("Single Account operations"))
        single_operation_layout.addWidget(self.single_operation_combobox)
        single_operation_layout.addWidget(self.amount_input)
        single_operation_layout.addWidget(self.deposit_btn)
        single_operation_layout.addWidget(self.withdraw_btn)


        transfer_layout = QVBoxLayout()
        transfer_layout.addWidget(QLabel("Transfer"))
        transfer_layout.addWidget(self.from_accounts_combobox)
        transfer_layout.addWidget(self.to_accounts_combobox)
        transfer_layout.addWidget(self.transfer_btn)
        transfer_layout.addSpacing(16)


        main_layout.addLayout(form_layout)
        main_layout.addSpacing(16)
        main_layout.addLayout(single_operation_layout)
        main_layout.addSpacing(16)
        main_layout.addLayout(transfer_layout)
        main_layout.addSpacing(16)
        main_layout.addWidget(self.table)
        main_layout.addStretch()

    def refresh_accounts_table(self):
        accounts = self._ledger.accounts
        self.table.setRowCount(len(accounts))
        self.table.setColumnCount(3)
        row = 0
        for idx, account in accounts.items():
            self.table.setItem(row, 0, QTableWidgetItem(str(account.id)))
            self.table.setItem(row, 1, QTableWidgetItem(account.owner))
            self.table.setItem(row, 2, QTableWidgetItem(str(account.balance)))
            row += 1

    def seed_demo_accounts(self):
        self._ledger.create_account("user1", 1000)
        self._ledger.create_account("user2", 100000)
        self._ledger.create_account("user3", 50000)
        self._ledger.create_account("user4", 666)
        self._ledger.create_account("user5", 10)

        accounts = self._ledger.accounts.items()
        for idx, account in accounts:
            text = f"{account.id} | {account.owner} | {account.balance}" 
            self.from_accounts_combobox.addItem(text, account.id)
            self.to_accounts_combobox.addItem(text, account.id)

    def handle_deposit(self):
        account_id = self.single_operation_combobox.currentData()
        raw_amount = self.amount_input.text()

        try:
            amount = int(raw_amount)

        except ValueError:
            self.status_label.setText("Amount must be an integer")
            return

        try:
            self._ledger.deposit(account_id, amount)
            account = self._ledger.get_account(account_id)

            self.refresh_ui()

            self.status_label.setText(f"Deposit is success. Balance of {account.id} is {account.balance}")

        except ValueError as err:
            self.status_label.setText(f"{err}")
            return


    def handle_withdraw(self):
        account_id = self.single_operation_combobox.currentData()
        raw_amount = self.amount_input.text()

        try:
            amount = int(raw_amount)

        except ValueError:
            self.status_label.setText("Amount must be an integer")
            return

        try:
            self._ledger.withdraw(account_id, amount)
            account = self._ledger.get_account(account_id)

            self.refresh_ui()

            self.status_label.setText(f"Withdraw is success. Balance of {account.id} is {account.balance}")

        except ValueError as err:
            self.status_label.setText(f"{err}")
            return

    def handle_transfer(self):
        from_account_id = self.from_accounts_combobox.currentData()
        to_account_id = self.to_accounts_combobox.currentData()

        raw_amount = self.amount_input.text()

        try:
            amount = int(raw_amount)
        except ValueError:
            self.status_label.setText("Amount must be an integer")
            return

        try:            
            self._ledger.transfer(from_account_id, to_account_id, amount)
            from_account = self._ledger.get_account(from_account_id)
            to_account = self._ledger.get_account(to_account_id)

            self.refresh_ui()

            self.status_label.setText(f"Transfer is success. Balance of {from_account.id} is {from_account.balance} and {to_account.id} is {to_account.balance}")
        except ValueError as err:
            self.status_label.setText(f"{err}")
            return

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

            self.refresh_ui()

        except ValueError as err:
            self.status_label.setText(f"{err}")
            return

        self.status_label.setText(f"Account created: {account.owner}, {account.balance}")

    def refresh_ui(self):
        accounts = self._ledger.accounts

        single_id = self.single_operation_combobox.currentData()
        from_id = self.from_accounts_combobox.currentData()
        to_id = self.to_accounts_combobox.currentData()

        self.clear_inputs()

        for idx, account in accounts.items():
            text = f"{account.id} | {account.owner} | {account.balance}"

            self.single_operation_combobox.addItem(text, account.id)
            self.from_accounts_combobox.addItem(text, account.id)
            self.to_accounts_combobox.addItem(text, account.id)

        single_idx = self.single_operation_combobox.findData(single_id)
        from_idx = self.from_accounts_combobox.findData(from_id)
        to_idx = self.to_accounts_combobox.findData(to_id)

        if single_idx != -1:
            self.single_operation_combobox.setCurrentIndex(single_idx)

        if from_idx != -1:
            self.from_accounts_combobox.setCurrentIndex(from_idx)

        if to_idx != -1:
            self.to_accounts_combobox.setCurrentIndex(to_idx)


        self.refresh_accounts_table()
    
    def clear_inputs(self):
        self.owner_input.setText("")
        self.balance_input.setText("")

        self.single_operation_combobox.clear()
        self.from_accounts_combobox.clear()
        self.to_accounts_combobox.clear()


def main():
    app = QApplication([])

    window = LedgerWindow()

    window.show()
    window.setFocus()

    app.exec()

if __name__ == "__main__":
    main()