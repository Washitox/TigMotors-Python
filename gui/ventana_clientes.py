from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
)
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt
from firebase_admin import firestore
from firebase_config import db

db = firestore.client()  

class VentanaClientes(QWidget):
    def __init__(self, ventana_inicio):
        super().__init__()
        self.ventana_inicio = ventana_inicio
        self.setWindowTitle("Clientes - TigMotors")
        self.setGeometry(100, 100, 900, 600)

       
        self.ruta_logo = "assets/logo.png"
        self.logo_pixmap = QPixmap(self.ruta_logo).scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )

        self.setup_ui()
        self.cargar_clientes()

    def setup_ui(self):
        
        self.boton_regresar = QPushButton("Regresar", self)
        self.boton_regresar.move(10, 10)
        self.boton_regresar.setFixedSize(80, 30)
        font = self.boton_regresar.font()
        font.setPointSize(10)
        self.boton_regresar.setFont(font)
        self.boton_regresar.setCursor(Qt.PointingHandCursor)
        self.boton_regresar.setStyleSheet("""
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
        self.boton_regresar.clicked.connect(self.regresar_menu)

        
        self.nombre_input = QLineEdit()
        self.nombre_input.setMaxLength(20)
        self.empresa_input = QLineEdit()
        self.empresa_input.setMaxLength(20)
        self.correo_input = QLineEdit()
        self.correo_input.setMaxLength(30)
        self.numero_input = QLineEdit()
        self.numero_input.setMaxLength(15)
        self.numero_input.setValidator(QtGui.QIntValidator())  # Solo números

        self.boton_agregar = QPushButton("Agregar")
        self.boton_agregar.clicked.connect(self.agregar_cliente)

        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Nombre:"))
        input_layout.addWidget(self.nombre_input)
        input_layout.addWidget(QLabel("Empresa:"))
        input_layout.addWidget(self.empresa_input)
        input_layout.addWidget(QLabel("Correo:"))
        input_layout.addWidget(self.correo_input)
        input_layout.addWidget(QLabel("Número:"))
        input_layout.addWidget(self.numero_input)
        input_layout.addWidget(self.boton_agregar)

        
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Empresa", "Correo", "Número", "Acción"])
        self.tabla.setColumnWidth(0, 50)
        self.tabla.setColumnWidth(5, 100)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.boton_regresar)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.tabla)

        self.setLayout(main_layout)

    def paintEvent(self, event):
        """Dibuja el logo de fondo con opacidad."""
        painter = QPainter(self)
        painter.setOpacity(0.15)  
        pixmap_redimensionado = self.logo_pixmap.scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )
        x = (self.width() - pixmap_redimensionado.width()) // 2
        y = (self.height() - pixmap_redimensionado.height()) // 2
        painter.drawPixmap(x, y, pixmap_redimensionado)
        painter.setOpacity(1)
        super().paintEvent(event)

    def regresar_menu(self):
        from gui.ventana_menu import VentanaMenu  
        self.close()
        self.ventana_menu = VentanaMenu(self.ventana_inicio)
        self.ventana_menu.show()

    def cargar_clientes(self):
        try:
            clientes_ref = db.collection("clientes").stream()
            self.tabla.setRowCount(0)

            for i, cliente in enumerate(clientes_ref):
                datos = cliente.to_dict()
                self.tabla.insertRow(i)
                self.tabla.setItem(i, 0, QTableWidgetItem(cliente.id))
                self.tabla.setItem(i, 1, QTableWidgetItem(datos.get("nombre", "")))
                self.tabla.setItem(i, 2, QTableWidgetItem(datos.get("empresa", "")))
                self.tabla.setItem(i, 3, QTableWidgetItem(datos.get("correo", "")))
                self.tabla.setItem(i, 4, QTableWidgetItem(datos.get("numero", "")))

                boton = QPushButton("Seleccionar")
                boton.clicked.connect(lambda _, id=cliente.id: self.seleccionar_cliente(id))
                self.tabla.setCellWidget(i, 5, boton)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la base de datos:\n{e}")

    def agregar_cliente(self):
        try:
            clientes = db.collection("clientes").stream()
            ids = []
            for c in clientes:
                try:
                    ids.append(int(c.id))
                except:
                    pass 

            nuevo_id = str(max(ids) + 1) if ids else "1"

            datos_cliente = {
                "nombre": self.nombre_input.text(),
                "empresa": self.empresa_input.text(),
                "correo": self.correo_input.text(),
                "numero": self.numero_input.text(),
            }

            if not all(datos_cliente.values()):
                QMessageBox.warning(self, "Atención", "Por favor, completa todos los campos.")
                return

            db.collection("clientes").document(nuevo_id).set(datos_cliente)

            QMessageBox.information(self, "Éxito", f"Cliente agregado con ID {nuevo_id}")

            self.nombre_input.clear()
            self.empresa_input.clear()
            self.correo_input.clear()
            self.numero_input.clear()

            self.cargar_clientes()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo agregar cliente:\n{e}")

    def seleccionar_cliente(self, cliente_id):
        try:
            doc = db.collection("clientes").document(cliente_id).get()
            if doc.exists:
                from gui.ventana_editar_cliente import VentanaEditarCliente
                self.ventana_editar = VentanaEditarCliente(cliente_id, doc.to_dict(), self.cargar_clientes)
                self.ventana_editar.show()
            else:
                QMessageBox.warning(self, "Error", "Cliente no encontrado.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo obtener cliente:\n{e}")
