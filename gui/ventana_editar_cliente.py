from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from firebase_config import db

class VentanaEditarCliente(QWidget):
    def __init__(self, cliente_id, datos, recargar_callback):
        super().__init__()
        self.cliente_id = cliente_id
        self.recargar_callback = recargar_callback
        self.setWindowTitle(f"Editar Cliente {cliente_id}")
        self.setGeometry(300, 200, 400, 300)

        self.nombre = QLineEdit(datos.get("nombre", ""))
        self.empresa = QLineEdit(datos.get("empresa", ""))
        self.correo = QLineEdit(datos.get("correo", ""))
        self.numero = QLineEdit(datos.get("numero", ""))

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Nombre"))
        layout.addWidget(self.nombre)
        layout.addWidget(QLabel("Empresa"))
        layout.addWidget(self.empresa)
        layout.addWidget(QLabel("Correo"))
        layout.addWidget(self.correo)
        layout.addWidget(QLabel("Número"))
        layout.addWidget(self.numero)

        boton_guardar = QPushButton("Guardar cambios")
        boton_guardar.clicked.connect(self.guardar)
        boton_eliminar = QPushButton("Eliminar cliente")
        boton_eliminar.clicked.connect(self.eliminar)

        layout.addWidget(boton_guardar)
        layout.addWidget(boton_eliminar)

        self.setLayout(layout)

    def guardar(self):
        datos_actualizados = {
            "nombre": self.nombre.text(),
            "empresa": self.empresa.text(),
            "correo": self.correo.text(),
            "numero": self.numero.text()
        }
        db.collection("clientes").document(self.cliente_id).set(datos_actualizados)
        QMessageBox.information(self, "Éxito", "Cliente actualizado correctamente")
        self.recargar_callback()
        self.close()

    def eliminar(self):
        db.collection("clientes").document(self.cliente_id).delete()
        QMessageBox.information(self, "Eliminado", "Cliente eliminado correctamente")
        self.recargar_callback()
        self.close()
