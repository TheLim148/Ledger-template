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
)

def main():
    app = QApplication([])

    window = QWidget()
    window.setWindowTitle("Ledger app")
    window.resize(400, 300)
    window.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

    layout = QFormLayout(window)

    owner_input = QLineEdit()
    owner_input.setPlaceholderText("Enter your name..")
    owner_input.setMaximumWidth(300)
    
    balance_input = QLineEdit()
    balance_input.setPlaceholderText("Enter your start balance..")
    balance_input.setMaximumWidth(300)

    # Create Account button
    ca_btn = QPushButton("Create Account")
    ca_btn.setMaximumWidth(100)

    def handle_create_account():
        parse_input(owner_input, balance_input)

    ca_btn.clicked.connect(handle_create_account)
    
    layout.addRow("Owner: ", owner_input)
    layout.addRow("Balance: ", balance_input)
    layout.addRow(ca_btn)
    layout.setAlignment(Qt.AlignmentFlag.AlignLeft)


    window.show()
    window.setFocus()

    app.exec()

def parse_input(input1: QLineEdit, input2: QLineEdit):
    owner = input1.text()
    raw_balance = input2.text()

    try:
        parsed_balance = int(raw_balance)
        print(owner, parsed_balance)
    except ValueError:
        print("balance must be an integer!")
        return


if __name__ == "__main__":
    main()