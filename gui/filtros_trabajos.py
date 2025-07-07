from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QDateEdit, QComboBox, QMessageBox
)
from PyQt5.QtCore import QDate
from firebase_config import db  # Asumiendo que aquí tienes configurada la conexión

class FiltroTrabajosDialog(QDialog):
    def __init__(self, aplicar_filtros_callback):
        super().__init__()
        self.aplicar_filtros_callback = aplicar_filtros_callback
        self.setWindowTitle("Filtrar Trabajos")
        self.setGeometry(300, 300, 500, 200)
        self.setup_ui()
        self.cargar_nombres_clientes()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.id_input = QLineEdit()

        # Ahora usamos combo para nombres
        self.nombre_combo = QComboBox()
        self.nombre_combo.addItem("", None)  # opción vacía para que no filtre si no se elige nada

        self.fecha_inicio = QDateEdit(calendarPopup=True)
        self.fecha_inicio.setDisplayFormat("yyyy-MM-dd")
        self.fecha_inicio.setMinimumDate(QDate(2000, 1, 1))
        self.fecha_inicio.setMaximumDate(QDate(3000, 1, 1))
        self.fecha_inicio.setSpecialValueText("No seleccionada")
        self.fecha_inicio.setDate(self.fecha_inicio.minimumDate())

        self.fecha_fin = QDateEdit(calendarPopup=True)
        self.fecha_fin.setDisplayFormat("yyyy-MM-dd")
        self.fecha_fin.setMinimumDate(QDate(2000, 1, 1))
        self.fecha_fin.setMaximumDate(QDate(3000, 1, 1))
        self.fecha_fin.setSpecialValueText("No seleccionada")
        self.fecha_fin.setDate(self.fecha_fin.minimumDate())

        layout.addWidget(QLabel("ID Trabajo:"))
        layout.addWidget(self.id_input)
        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.nombre_combo)
        layout.addWidget(QLabel("Fecha Inicio:"))
        layout.addWidget(self.fecha_inicio)
        layout.addWidget(QLabel("Fecha Fin:"))
        layout.addWidget(self.fecha_fin)

        botones_layout = QHBoxLayout()
        boton_buscar = QPushButton("Buscar")
        boton_cancelar = QPushButton("Cancelar")
        boton_buscar.clicked.connect(self.buscar)
        boton_cancelar.clicked.connect(self.reject)
        botones_layout.addWidget(boton_buscar)
        botones_layout.addWidget(boton_cancelar)

        layout.addLayout(botones_layout)
        self.setLayout(layout)

    def cargar_nombres_clientes(self):
        try:
            self.nombre_combo.clear()
            self.nombre_combo.addItem("", None)  # para dejar opción vacía
            clientes_ref = db.collection("clientes").stream()
            for cliente in clientes_ref:
                datos = cliente.to_dict()
                nombre = datos.get("nombre", "")
                if nombre:
                    self.nombre_combo.addItem(nombre, cliente.id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar los nombres:\n{e}")

    def buscar(self):
        filtros = {}

        id_trabajo = self.id_input.text().strip()
        nombre = self.nombre_combo.currentText().strip()
        # Para que si no eliges nada no filtre
        if nombre == "":
            nombre = None

        # Verifica si el usuario modificó las fechas desde el valor mínimo
        fecha_inicio_seleccionada = self.fecha_inicio.date() != self.fecha_inicio.minimumDate()
        fecha_fin_seleccionada = self.fecha_fin.date() != self.fecha_fin.minimumDate()

        if id_trabajo:
            filtros["id_trabajo"] = id_trabajo
        if nombre:
            filtros["nombre"] = nombre
        if fecha_inicio_seleccionada:
            filtros["fecha_inicio"] = self.fecha_inicio.date().toString("yyyy-MM-dd")
        if fecha_fin_seleccionada:
            filtros["fecha_fin"] = self.fecha_fin.date().toString("yyyy-MM-dd")

        self.aplicar_filtros_callback(filtros)
        self.accept()
