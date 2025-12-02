from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame, QSizePolicy
from PySide6.QtCore import Qt, QPropertyAnimation, QRect

class ProgressBarReact(QWidget):
    """
    Barra de progreso estilo React:
    - Barra gruesa
    - Bordes redondeados
    - Porcentaje centrado
    - Animación suave
    """
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        self.setLayout(layout)

        self.container = QFrame()
        self.container.setObjectName("ProgressContainer")
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.bar = QFrame(self.container)
        self.bar.setObjectName("ProgressBar")

        self.label_center = QLabel("0%")
        self.label_center.setAlignment(Qt.AlignCenter)
        self.label_center.setAttribute(Qt.WA_TransparentForMouseEvents)

        cont_layout = QHBoxLayout(self.container)
        cont_layout.setContentsMargins(0, 0, 0, 0)
        cont_layout.addWidget(self.label_center)

        layout.addWidget(self.container)

        self.animation = QPropertyAnimation(self.bar, b"geometry")
        self.animation.setDuration(350)

        self.progress_value = 0

    def resizeEvent(self, event):
        """Para que la barra azul pueda reajustarse al tamaño real."""
        self._update_bar_geometry(self.progress_value)
        super().resizeEvent(event)

    def setValue(self, value: int):
        value = max(0, min(100, value))

        self.progress_value = value

        self.label_center.setText(f"{value}%")

        self._update_bar_geometry(value)

    def _update_bar_geometry(self, value):
        """Actualiza la animación de la barra azul."""
        total_width = self.container.width()
        new_width = int((value / 100) * total_width)

        self.animation.stop()
        self.animation.setStartValue(self.bar.geometry())
        self.animation.setEndValue(QRect(0, 0, new_width, self.container.height()))
        self.animation.start()
