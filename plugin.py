"""Minimal QGIS plugin shell that exposes cumulative-impact calculation."""

from qgis.PyQt.QtWidgets import QAction, QMessageBox

from .calculator import ImpactComponent, compute_cumulative_impact


class ImpattoCumulatoPlugin:
    """QGIS plugin main class."""

    def __init__(self, iface):
        self.iface = iface
        self.action = None

    def initGui(self):
        self.action = QAction("IMPATTO-CUMULATO: calcolo demo", self.iface.mainWindow())
        self.action.triggered.connect(self.run_demo)
        self.iface.addPluginToMenu("IMPATTO-CUMULATO", self.action)

    def unload(self):
        if self.action is not None:
            self.iface.removePluginMenu("IMPATTO-CUMULATO", self.action)
            self.action = None

    def run_demo(self):
        value = compute_cumulative_impact(
            [
                ImpactComponent("visibilita", 0.75, 0.5),
                ImpactComponent("rumore", 0.30, 0.3),
                ImpactComponent("distanza", 0.55, 0.2),
            ]
        )
        QMessageBox.information(
            self.iface.mainWindow(),
            "IMPATTO-CUMULATO",
            f"Indice cumulato demo: {value:.3f}",
        )
