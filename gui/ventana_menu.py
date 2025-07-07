from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QLabel
)
from PyQt5.QtGui import QFont, QCursor, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

from gui.ventana_clientes import VentanaClientes
from gui.ventana_trabajos import VentanaTrabajos 

class VentanaMenu(QWidget):
    def __init__(self, ventana_inicio):
        super().__init__()
        self.setWindowTitle("Menú Principal")
        self.setFixedSize(800, 600)
        self.ventana_inicio = ventana_inicio

        # Carga el logo para fondo
        self.ruta_logo = "assets/logo.png"
        self.logo_pixmap = QPixmap(self.ruta_logo).scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )

        self.init_ui()

    def init_ui(self):
        # Layout principal para los botones y barra
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(10)

        # Barra superior con botón Cerrar sesión a la derecha
        barra_superior = QHBoxLayout()
        barra_superior.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.boton_cerrar_sesion = QPushButton("Cerrar sesión")
        self.boton_cerrar_sesion.setFont(QFont("Arial", 10))
        self.boton_cerrar_sesion.setCursor(QCursor(Qt.PointingHandCursor))
        self.boton_cerrar_sesion.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        self.boton_cerrar_sesion.clicked.connect(self.cerrar_sesion)
        barra_superior.addWidget(self.boton_cerrar_sesion)

        layout_principal.addLayout(barra_superior)

        # Layout para los botones principales (Clientes y Trabajos)
        botones_layout = QVBoxLayout()
        botones_layout.setAlignment(Qt.AlignCenter)

        self.boton_clientes = QPushButton("Clientes")
        self.boton_clientes.setFont(QFont("Arial", 12))
        self.boton_clientes.setFixedSize(200, 50)
        self.boton_clientes.setCursor(QCursor(Qt.PointingHandCursor))
        self.boton_clientes.clicked.connect(self.abrir_clientes)

        self.boton_trabajos = QPushButton("Trabajos")
        self.boton_trabajos.setFont(QFont("Arial", 12))
        self.boton_trabajos.setFixedSize(200, 50)
        self.boton_trabajos.setCursor(QCursor(Qt.PointingHandCursor))
        self.boton_trabajos.clicked.connect(self.abrir_trabajos)

        botones_layout.addWidget(self.boton_clientes)
        botones_layout.addSpacing(20)
        botones_layout.addWidget(self.boton_trabajos)

        layout_principal.addLayout(botones_layout)

        self.setLayout(layout_principal)

    def paintEvent(self, event):
        """Dibuja el logo de fondo con opacidad."""
        painter = QPainter(self)
        painter.setOpacity(0.15)  # Opacidad baja para efecto tenue
        # Ajusta el pixmap para que cubra toda la ventana
        pixmap_redimensionado = self.logo_pixmap.scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )
        # Centrar el pixmap
        x = (self.width() - pixmap_redimensionado.width()) // 2
        y = (self.height() - pixmap_redimensionado.height()) // 2
        painter.drawPixmap(x, y, pixmap_redimensionado)
        painter.setOpacity(1)  # Restablece opacidad normal
        super().paintEvent(event)

    def cerrar_sesion(self):
        respuesta = QMessageBox.question(
            self,
            "Cerrar sesión",
            "¿Está seguro que desea cerrar sesión?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            self.close()
            self.ventana_inicio.show()

    def abrir_clientes(self):
        self.clientes = VentanaClientes(self.ventana_inicio)
        self.clientes.show()
        self.close()

    def abrir_trabajos(self):
        self.trabajos = VentanaTrabajos(self.ventana_inicio)
        self.trabajos.show()
        self.close()
