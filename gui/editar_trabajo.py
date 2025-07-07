from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QDateEdit, QMessageBox, QComboBox
)
from PyQt5.QtCore import QDate
from firebase_config import db

class EditarTrabajoDialog(QDialog):
    def __init__(self, trabajo_id, ventana_padre, recargar_callback):
        super().__init__(ventana_padre)
        self.trabajo_id = trabajo_id
        self.recargar_callback = recargar_callback
        self.setWindowTitle("Editar/Eliminar Trabajo")
        self.setGeometry(300, 300, 400, 300)
        self.setup_ui()
        self.cargar_datos()

    def setup_ui(self):
        self.layout = QVBoxLayout()

        self.nombre_combo = QComboBox()
        self.nombre_combo.setEditable(False)
        self.descripcion_input = QLineEdit()
        self.precio_input = QLineEdit()
        self.fecha_inicio = QDateEdit(calendarPopup=True)
        self.fecha_fin = QDateEdit(calendarPopup=True)

        self.boton_editar = QPushButton("Editar y Guardar")
        self.boton_eliminar = QPushButton("Eliminar")

        self.boton_editar.clicked.connect(self.editar_trabajo)
        self.boton_eliminar.clicked.connect(self.eliminar_trabajo)

        self.layout.addWidget(QLabel("Cliente:"))
        self.layout.addWidget(self.nombre_combo)
        self.layout.addWidget(QLabel("Descripción:"))
        self.layout.addWidget(self.descripcion_input)
        self.layout.addWidget(QLabel("Precio:"))
        self.layout.addWidget(self.precio_input)
        self.layout.addWidget(QLabel("Fecha Inicio:"))
        self.layout.addWidget(self.fecha_inicio)
        self.layout.addWidget(QLabel("Fecha Fin:"))
        self.layout.addWidget(self.fecha_fin)
        self.layout.addWidget(self.boton_editar)
        self.layout.addWidget(self.boton_eliminar)

        self.setLayout(self.layout)

    def cargar_datos(self):
        doc = db.collection("trabajos").document(self.trabajo_id).get()
        if not doc.exists:
            QMessageBox.warning(self, "Error", "Trabajo no encontrado")
            self.close()
            return

        data = doc.to_dict()
        cliente_id_actual = data.get("cliente_id", "")

        # Llenar el combo con los clientes
        self.nombre_combo.clear()
        clientes_ref = db.collection("clientes").stream()
        index_a_seleccionar = 0
        for i, cliente in enumerate(clientes_ref):
            cliente_data = cliente.to_dict()
            nombre = cliente_data.get("nombre", "")
            self.nombre_combo.addItem(nombre, cliente.id)
            if cliente.id == cliente_id_actual:
                index_a_seleccionar = i

        self.nombre_combo.setCurrentIndex(index_a_seleccionar)
        self.descripcion_input.setText(data.get("descripcion", ""))
        self.precio_input.setText(str(data.get("precio", "")))
        self.fecha_inicio.setDate(QDate.fromString(data.get("fecha_inicio", ""), "yyyy-MM-dd"))
        self.fecha_fin.setDate(QDate.fromString(data.get("fecha_fin", ""), "yyyy-MM-dd"))

    def editar_trabajo(self):
        descripcion = self.descripcion_input.text().strip()
        precio = self.precio_input.text().strip()

        if not descripcion or not precio:
            QMessageBox.warning(self, "Campos incompletos", "Completa todos los campos obligatorios.")
            return

        datos_actualizados = {
            "nombre": self.nombre_combo.currentText(),
            "cliente_id": self.nombre_combo.currentData(),
            "descripcion": descripcion,
            "precio": precio,
            "fecha_inicio": self.fecha_inicio.date().toString("yyyy-MM-dd"),
            "fecha_fin": self.fecha_fin.date().toString("yyyy-MM-dd"),
        }

        db.collection("trabajos").document(self.trabajo_id).update(datos_actualizados)
        QMessageBox.information(self, "Éxito", "Trabajo actualizado correctamente.")
        self.recargar_callback()
        self.close()

    def eliminar_trabajo(self):
        respuesta = QMessageBox.question(
            self, "Confirmar eliminación", "¿Estás seguro de eliminar este trabajo?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            db.collection("trabajos").document(self.trabajo_id).delete()
            QMessageBox.information(self, "Eliminado", "Trabajo eliminado correctamente.")
            self.recargar_callback()
            self.close()
