"""QGIS plugin shell for cumulative wind-visibility calculation."""

from qgis.PyQt.QtWidgets import QAction, QMessageBox
from qgis.core import QgsApplication

from .processing_provider import ImpattoCumulatoProvider


class ImpattoCumulatoPlugin:
    """QGIS plugin main class."""

    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.provider = None

    def initGui(self):
        self.provider = ImpattoCumulatoProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

        self.action = QAction("IMPATTO-CUMULATO: VAI visibility", self.iface.mainWindow())
        self.action.triggered.connect(self.run_analysis)
        self.iface.addPluginToMenu("IMPATTO-CUMULATO", self.action)

    def unload(self):
        if self.action is not None:
            self.iface.removePluginMenu("IMPATTO-CUMULATO", self.action)
            self.action = None
        if self.provider is not None:
            QgsApplication.processingRegistry().removeProvider(self.provider)
            self.provider = None

    def run_analysis(self):
        try:
            import processing

            processing.execAlgorithmDialog("impatto_cumulato:cumulative_visibility", {})
        except Exception as exc:  # pragma: no cover - runtime guard in QGIS
            QMessageBox.critical(
                self.iface.mainWindow(),
                "IMPATTO-CUMULATO",
                f"Unable to start processing dialog: {exc}",
            )
