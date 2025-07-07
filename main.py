from gui.ventana_inicio import VentanaInicio
from PyQt5.QtWidgets import QApplication
import sys
import firebase_config  
from gui.ventana_inicio import VentanaInicio

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaInicio()
    ventana.show()
    sys.exit(app.exec_())


