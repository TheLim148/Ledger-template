from PySide6.QtWidgets import QApplication, QLabel, QFrame
from PySide6.QtCore import Qt

def main():
    app = QApplication([])

    label = QLabel("Hello my app", alignment=Qt.AlignmentFlag.AlignCenter)
    label.resize(200, 30)
    label.setFrameShape(QFrame.Shape.Panel)
    label.show()

    app.exec()



if __name__ == "__main__":
    main()