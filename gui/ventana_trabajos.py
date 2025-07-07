from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QTableWidget, QTableWidgetItem, QDateEdit, QMessageBox, QHeaderView
)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QPixmap, QPainter, QCursor
from firebase_admin import firestore
from firebase_config import db

from gui.filtros_trabajos import FiltroTrabajosDialog
from gui.editar_trabajo import EditarTrabajoDialog
from PyQt5.QtGui import QIntValidator



class VentanaTrabajos(QWidget):
    def __init__(self, ventana_inicio):
        super().__init__()
        self.ventana_inicio = ventana_inicio
        self.setWindowTitle("Trabajos - TigMotors")
        self.setGeometry(100, 100, 1000, 600)


        self.ruta_logo = "assets/logo.png"
        self.logo_pixmap = QPixmap(self.ruta_logo).scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )

        self.setup_ui()
        self.cargar_nombres_clientes()
        self.cargar_trabajos()

    def setup_ui(self):
        layout = QVBoxLayout()


        self.boton_regresar = QPushButton("Regresar")
        self.boton_regresar.setFixedSize(80, 30)
        self.boton_regresar.setCursor(QCursor(Qt.PointingHandCursor))
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
        layout.addWidget(self.boton_regresar)


        self.combo_nombres = QComboBox()
        self.descripcion_input = QLineEdit()
        self.descripcion_input.setMaxLength(100)
        self.precio_input = QLineEdit()
        self.precio_input.setValidator(QIntValidator(0, 9999))
        self.fecha_inicio = QDateEdit(calendarPopup=True)
        self.fecha_inicio.setDate(QDate.currentDate())
        self.fecha_fin = QDateEdit(calendarPopup=True)
        self.fecha_fin.setDate(QDate.currentDate())

        self.boton_agregar = QPushButton("Agregar Trabajo")
        self.boton_agregar.setCursor(QCursor(Qt.PointingHandCursor))
        self.boton_agregar.clicked.connect(self.agregar_trabajo)

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Cliente:"))
        form_layout.addWidget(self.combo_nombres)
        form_layout.addWidget(QLabel("Descripción:"))
        form_layout.addWidget(self.descripcion_input)
        form_layout.addWidget(QLabel("Precio:"))
        form_layout.addWidget(self.precio_input)
        form_layout.addWidget(QLabel("Inicio:"))
        form_layout.addWidget(self.fecha_inicio)
        form_layout.addWidget(QLabel("Fin:"))
        form_layout.addWidget(self.fecha_fin)
        form_layout.addWidget(self.boton_agregar)

        layout.addLayout(form_layout)


        filtros_layout = QHBoxLayout()
        self.boton_filtros = QPushButton("Sistema de Filtros")
        self.boton_filtros.setFixedSize(150, 30)
        self.boton_filtros.setCursor(QCursor(Qt.PointingHandCursor))
        self.boton_filtros.clicked.connect(self.abrir_filtros)

        self.boton_borrar_filtros = QPushButton("Borrar Filtros")
        self.boton_borrar_filtros.setFixedSize(150, 30)
        self.boton_borrar_filtros.setCursor(QCursor(Qt.PointingHandCursor))
        self.boton_borrar_filtros.clicked.connect(self.cargar_trabajos)

        filtros_layout.addWidget(self.boton_filtros)
        filtros_layout.addWidget(self.boton_borrar_filtros)
        layout.addLayout(filtros_layout)


        self.tabla = QTableWidget()
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Descripción", "Precio", "Inicio", "Fin", "Acción"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.tabla)

        self.setLayout(layout)

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

    def cargar_nombres_clientes(self):
        try:
            self.combo_nombres.clear()
            clientes_ref = db.collection("clientes").stream()
            for cliente in clientes_ref:
                datos = cliente.to_dict()
                self.combo_nombres.addItem(datos.get("nombre", ""), cliente.id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar los nombres:\n{e}")

    def agregar_trabajo(self):
        try:
            nombre = self.combo_nombres.currentText()
            cliente_id = self.combo_nombres.currentData()
            descripcion = self.descripcion_input.text()
            precio = self.precio_input.text()
            inicio = self.fecha_inicio.date().toString("yyyy-MM-dd")
            fin = self.fecha_fin.date().toString("yyyy-MM-dd")

            if not descripcion or not precio:
                QMessageBox.warning(self, "Campos incompletos", "Completa todos los campos.")
                return

            trabajos_ref = db.collection("trabajos").stream()
            ids = [int(t.id) for t in trabajos_ref if t.id.isnumeric()]
            nuevo_id = str(max(ids) + 1) if ids else "1"

            db.collection("trabajos").document(nuevo_id).set({
                "cliente_id": cliente_id,
                "nombre": nombre,
                "descripcion": descripcion,
                "precio": precio,
                "fecha_inicio": inicio,
                "fecha_fin": fin
            })

            QMessageBox.information(self, "Éxito", f"Trabajo agregado con ID {nuevo_id}")
            self.cargar_trabajos()
            
            self.descripcion_input.clear()
            self.precio_input.clear()
            self.fecha_inicio.setDate(QDate.currentDate())
            self.fecha_fin.setDate(QDate.currentDate())
            self.combo_nombres.setCurrentIndex(0)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo agregar trabajo:\n{e}")

    def cargar_trabajos(self, filtros=None):
        try:
            self.tabla.setRowCount(0)
            trabajos = db.collection("trabajos").stream()

            for i, trabajo in enumerate(trabajos):
                data = trabajo.to_dict()
                id_trabajo = trabajo.id
                nombre = data.get("nombre", "")
                descripcion = data.get("descripcion", "")
                precio = str(data.get("precio", ""))
                fecha_inicio = data.get("fecha_inicio", "")
                fecha_fin = data.get("fecha_fin", "")


                if filtros:
                    if "id_trabajo" in filtros and filtros["id_trabajo"] != id_trabajo:
                        continue
                    if "nombre" in filtros and filtros["nombre"].lower() not in nombre.lower():
                        continue
                    if "fecha_inicio" in filtros and fecha_inicio < filtros["fecha_inicio"]:
                        continue
                    if "fecha_fin" in filtros and fecha_fin > filtros["fecha_fin"]:
                        continue

                self.tabla.insertRow(self.tabla.rowCount())
                row = self.tabla.rowCount() - 1
                self.tabla.setItem(row, 0, QTableWidgetItem(id_trabajo))
                self.tabla.setItem(row, 1, QTableWidgetItem(nombre))
                self.tabla.setItem(row, 2, QTableWidgetItem(descripcion))
                self.tabla.setItem(row, 3, QTableWidgetItem(precio))
                self.tabla.setItem(row, 4, QTableWidgetItem(fecha_inicio))
                self.tabla.setItem(row, 5, QTableWidgetItem(fecha_fin))

                boton = QPushButton("Seleccionar")
                boton.clicked.connect(lambda _, id=id_trabajo: self.seleccionar_trabajo(id))
                self.tabla.setCellWidget(row, 6, boton)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar los trabajos:\n{e}")

    def seleccionar_trabajo(self, trabajo_id):
        dialogo = EditarTrabajoDialog(trabajo_id, self, self.cargar_trabajos)
        dialogo.exec_()

    def abrir_filtros(self):
        dialogo = FiltroTrabajosDialog(self.cargar_trabajos)
        dialogo.exec_()
