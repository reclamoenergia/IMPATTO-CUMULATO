"""Plugin QGIS base per IMPATTO-CUMULATO."""

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox


class ImpattoCumulatoPlugin:
    """Implementazione minima del plugin con una singola azione."""

    def __init__(self, iface):
        self.iface = iface
        self.action = None

    def initGui(self):
        """Registra l'azione nel menu Plugin e nella toolbar."""
        self.action = QAction(QIcon(), "IMPATTO-CUMULATO", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu("&IMPATTO-CUMULATO", self.action)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        """Rimuove l'azione registrata dal plugin."""
        if self.action is not None:
            self.iface.removePluginMenu("&IMPATTO-CUMULATO", self.action)
            self.iface.removeToolBarIcon(self.action)
            self.action = None

    def run(self):
        """Azione dimostrativa: mostra una finestra informativa."""
        QMessageBox.information(
            self.iface.mainWindow(),
            "IMPATTO-CUMULATO",
            "Plugin caricato correttamente. Implementa qui la logica di analisi.",
        )
