from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QMessageBox, QStackedLayout
)
from PyQt5.QtGui import QPixmap, QFont, QPainter, QColor
from PyQt5.QtCore import Qt
from gui.ventana_menu import VentanaMenu

class VentanaInicio(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión - Inicio")
        self.setFixedSize(800, 600)

        ruta_logo = "assets/logo.png"

        pixmap_fondo = QPixmap(ruta_logo).scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )

        pixmap_opaco = QPixmap(pixmap_fondo.size())
        pixmap_opaco.fill(Qt.transparent)

        painter = QPainter(pixmap_opaco)
        painter.setOpacity(0.3)  
        painter.drawPixmap(0, 0, pixmap_fondo)
        painter.end()

        self.fondo = QLabel(self)
        self.fondo.setPixmap(pixmap_opaco)
        self.fondo.setGeometry(0, 0, self.width(), self.height())

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.logo = QLabel()
        pixmap_logo = QPixmap(ruta_logo).scaled(
            200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.logo.setPixmap(pixmap_logo)
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setStyleSheet("background: transparent;")

        self.input_codigo = QLineEdit()
        self.input_codigo.setPlaceholderText("Ingrese el código de acceso")
        self.input_codigo.setMaxLength(6)
        self.input_codigo.setFont(QFont("Arial", 12))
        self.input_codigo.setFixedWidth(300)
        self.input_codigo.setAlignment(Qt.AlignCenter)
        self.input_codigo.setEchoMode(QLineEdit.Password)
        self.input_codigo.setStyleSheet("background: rgba(255, 255, 255, 180); border-radius: 5px;")

        self.boton_ingresar = QPushButton("Ingresar")
        self.boton_ingresar.setFixedHeight(40)
        self.boton_ingresar.setFont(QFont("Arial", 12))
        self.boton_ingresar.clicked.connect(self.validar_codigo)
        self.boton_ingresar.setStyleSheet(
            """
            QPushButton {
                background-color: #007ACC;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005F9E;
            }
            """
        )

        layout.addWidget(self.logo)
        layout.addSpacing(10)
        layout.addWidget(self.input_codigo)
        layout.addSpacing(10)
        layout.addWidget(self.boton_ingresar)

        contenedor = QWidget(self)
        contenedor.setLayout(layout)
        contenedor.setGeometry(0, 0, self.width(), self.height())
        contenedor.setStyleSheet("background: transparent;")

    def validar_codigo(self):
        if self.input_codigo.text() == "134679":
            self.hide()
            self.menu = VentanaMenu(self)
            self.menu.show()
        else:
            QMessageBox.warning(self, "Acceso denegado", "Código incorrecto. Intente nuevamente.")
