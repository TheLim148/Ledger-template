from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from account import Account
from ledger import Ledger


class LedgerWindow(QWidget):
    def __init__(self, seed_demo, ledger: Ledger):
        super().__init__()

        self._ledger = ledger

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

        self._account_comboboxes = [
            self.single_operation_combobox,
            self.from_accounts_combobox,
            self.to_accounts_combobox,
        ]

        self.single_amount_input = QLineEdit()
        self.single_amount_input.setPlaceholderText("Enter amount..")
        self.single_amount_input.setMaximumWidth(300)

        self.transaction_amount_input = QLineEdit()
        self.transaction_amount_input.setPlaceholderText("Enter amount..")
        self.transaction_amount_input.setMaximumWidth(300)

        self.deposit_btn = QPushButton("Deposit")
        self.deposit_btn.setMaximumWidth(100)
        self.deposit_btn.clicked.connect(self.handle_deposit)

        self.withdraw_btn = QPushButton("Withdraw")
        self.withdraw_btn.setMaximumWidth(100)
        self.withdraw_btn.clicked.connect(self.handle_withdraw)

        self.transfer_btn = QPushButton("Transfer")
        self.transfer_btn.setMaximumWidth(100)
        self.transfer_btn.clicked.connect(self.handle_transfer)

        self.accounts_table = QTableWidget(columnCount=3)
        self.accounts_table.setHorizontalHeaderLabels(["id", "owner", "balance"])
        self.accounts_table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.transactions_table = QTableWidget(columnCount=6)
        self.transactions_table.setHorizontalHeaderLabels(
            ["id", "type", "amount", "from", "to", "created_at"]
        )
        self.transactions_table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        if seed_demo:
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
        single_operation_layout.addWidget(self.single_amount_input)
        single_operation_layout.addWidget(self.deposit_btn)
        single_operation_layout.addWidget(self.withdraw_btn)

        transfer_layout = QVBoxLayout()
        transfer_layout.addWidget(QLabel("Transfer"))
        transfer_layout.addWidget(self.from_accounts_combobox)
        transfer_layout.addWidget(self.to_accounts_combobox)
        transfer_layout.addWidget(self.transaction_amount_input)
        transfer_layout.addWidget(self.transfer_btn)
        transfer_layout.addSpacing(16)

        main_layout.addLayout(form_layout)
        main_layout.addSpacing(16)
        main_layout.addLayout(single_operation_layout)
        main_layout.addSpacing(16)
        main_layout.addLayout(transfer_layout)
        main_layout.addSpacing(16)
        main_layout.addWidget(self.accounts_table)
        main_layout.addSpacing(16)
        main_layout.addWidget(self.transactions_table)
        main_layout.addStretch()

    def refresh_accounts_table(self):
        accounts = self._ledger.get_accounts()
        self.accounts_table.setRowCount(len(accounts))
        row = 0
        for account in accounts:
            self.accounts_table.setItem(row, 0, QTableWidgetItem(str(account.id)))
            self.accounts_table.setItem(row, 1, QTableWidgetItem(account.owner))
            self.accounts_table.setItem(row, 2, QTableWidgetItem(str(account.balance)))
            row += 1

    def refresh_transactions_table(self):
        transactions = self._ledger.get_transactions()
        self.transactions_table.setRowCount(len(transactions))
        row = 0
        for transaction in transactions:
            self.transactions_table.setItem(
                row, 0, QTableWidgetItem(str(transaction.id))
            )
            self.transactions_table.setItem(
                row, 1, QTableWidgetItem(str(transaction.transaction_type.name))
            )
            self.transactions_table.setItem(
                row, 2, QTableWidgetItem(str(transaction.amount))
            )
            self.transactions_table.setItem(
                row, 3, QTableWidgetItem(str(transaction.from_account_id))
            )
            self.transactions_table.setItem(
                row, 4, QTableWidgetItem(str(transaction.to_account_id))
            )
            self.transactions_table.setItem(
                row, 5, QTableWidgetItem(str(transaction.created_at))
            )
            row += 1

    def seed_demo_accounts(self):
        self._ledger.create_account("user1", 1000)
        self._ledger.create_account("user2", 100000)
        self._ledger.create_account("user3", 50000)
        self._ledger.create_account("user4", 666)
        self._ledger.create_account("user5", 10)

    def parse(self, raw_value: str):
        if raw_value == "":
            self.status_label.setText("Value is empty")
            return

        try:
            value = int(raw_value)
        except ValueError:
            self.status_label.setText("Value must be an integer")
            return

        return value

    def handle_deposit(self):
        account_id = self.single_operation_combobox.currentData()
        raw_amount = self.single_amount_input.text()

        amount = self.parse(raw_amount)

        if amount is None:
            self.status_label.setText("Amount is None")
            return

        try:
            self._ledger.deposit(account_id, amount)
            account = self._ledger.get_account(account_id)

            self.refresh_ui()

            self.status_label.setText(
                f"Deposit is success. Balance of {account.id} is {account.balance}"
            )

        except ValueError as err:
            self.status_label.setText(f"{err}")
            return

    def handle_withdraw(self):
        account_id = self.single_operation_combobox.currentData()
        raw_amount = self.single_amount_input.text()

        amount = self.parse(raw_amount)

        if amount is None:
            self.status_label.setText("Amount is None")
            return

        try:
            self._ledger.withdraw(account_id, amount)
            account = self._ledger.get_account(account_id)

            self.refresh_ui()

            self.status_label.setText(
                f"Withdraw is success. Balance of {account.id} is {account.balance}"
            )

        except ValueError as err:
            self.status_label.setText(f"{err}")
            return

    def handle_transfer(self):
        from_account_id = self.from_accounts_combobox.currentData()
        to_account_id = self.to_accounts_combobox.currentData()

        raw_amount = self.transaction_amount_input.text()

        amount = self.parse(raw_amount)

        if amount is None:
            self.status_label.setText("Amount is None")
            return

        try:
            self._ledger.transfer(from_account_id, to_account_id, amount)
            from_account = self._ledger.get_account(from_account_id)
            to_account = self._ledger.get_account(to_account_id)

            self.refresh_ui()

            self.status_label.setText(
                f"Transfer is success. Balance of {1} is {2} and {3} is {4}",
                from_account.id,
                from_account.balance,
                to_account.id,
                to_account.balance,
            )
        except ValueError as err:
            self.status_label.setText(f"{err}")
            return

    def handle_create_account(self):
        owner = self.owner_input.text()
        raw_balance = self.balance_input.text()

        if owner.strip() == "" or raw_balance == "":
            self.status_label.setText("Fields must not be empty")
            return

        parsed_balance = self.parse(raw_balance)

        if parsed_balance is None:
            self.status_label.setText("Balance is None")
            return

        try:
            account = self._ledger.create_account(owner, parsed_balance)

            self.refresh_ui()

        except ValueError as err:
            self.status_label.setText(f"{err}")
            return

        self.status_label.setText(
            f"Account created: {account.owner}, {account.balance}"
        )

    def refresh_comboboxes(self, accounts: list[Account]):
        account_comboboxes = self._account_comboboxes

        for account_combobox in account_comboboxes:
            combo_id = account_combobox.currentData()
            account_combobox.clear()

            for account in accounts:
                text = f"{account.id} | {account.owner} | {account.balance}"
                account_combobox.addItem(text, account.id)

            combo_idx = account_combobox.findData(combo_id)

            if combo_idx != -1:
                account_combobox.setCurrentIndex(combo_idx)

    def update_buttons_state(self, accounts: list[Account]):
        if accounts == []:
            self.deposit_btn.setEnabled(False)
            self.withdraw_btn.setEnabled(False)
        else:
            self.deposit_btn.setEnabled(True)
            self.withdraw_btn.setEnabled(True)

        if len(accounts) < 2:
            self.transfer_btn.setEnabled(False)
        else:
            self.transfer_btn.setEnabled(True)

    def refresh_ui(self):
        self.clear_inputs()
        accounts = self._ledger.get_accounts()

        self.update_buttons_state(accounts)

        self.refresh_comboboxes(accounts)

        self.refresh_accounts_table()
        self.refresh_transactions_table()

    def clear_inputs(self):
        self.owner_input.setText("")
        self.balance_input.setText("")

        self.single_amount_input.clear()
        self.transaction_amount_input.clear()
