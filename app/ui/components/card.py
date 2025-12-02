from PySide6.QtWidgets import QWidget, QVBoxLayout

class Card(QWidget):
    """
    Contenedor estilo 'card' con fondo blanco y borde suave.
    """
    def __init__(self, child_widget):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(child_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        self.setLayout(layout)

        self.setObjectName("Card")
