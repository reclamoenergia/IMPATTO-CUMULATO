"""QGIS plugin UI for cumulative-impact calculation."""

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import (
    QAction,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .calculator import ImpactComponent, InvalidImpactData, compute_cumulative_impact


class ImpactCalculatorDialog(QDialog):
    """Dialog that lets users edit components and compute cumulative impact."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("IMPATTO-CUMULATO")
        self.resize(620, 380)

        layout = QVBoxLayout(self)

        help_label = QLabel(
            "Inserisci componenti con valore normalizzato [0,1] e peso >= 0."
        )
        help_label.setWordWrap(True)
        layout.addWidget(help_label)

        self.table = QTableWidget(0, 3, self)
        self.table.setHorizontalHeaderLabels(["Componente", "Valore [0-1]", "Peso"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        row_buttons = QHBoxLayout()
        add_row_button = QPushButton("Aggiungi riga")
        remove_row_button = QPushButton("Rimuovi riga selezionata")
        row_buttons.addWidget(add_row_button)
        row_buttons.addWidget(remove_row_button)
        row_buttons.addStretch(1)
        layout.addLayout(row_buttons)

        form_widget = QWidget(self)
        form_layout = QFormLayout(form_widget)
        self.decimals_spin = QDoubleSpinBox(self)
        self.decimals_spin.setDecimals(0)
        self.decimals_spin.setRange(0, 6)
        self.decimals_spin.setValue(3)
        self.decimals_spin.setSingleStep(1)
        self.decimals_spin.setToolTip("Numero decimali nel risultato")
        form_layout.addRow("Decimali risultato", self.decimals_spin)
        layout.addWidget(form_widget)

        self.result_label = QLabel("Indice cumulato: -")
        self.result_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.result_label)

        buttons = QDialogButtonBox(self)
        self.calculate_button = buttons.addButton("Calcola", QDialogButtonBox.ActionRole)
        close_button = buttons.addButton(QDialogButtonBox.Close)
        layout.addWidget(buttons)

        add_row_button.clicked.connect(self.add_row)
        remove_row_button.clicked.connect(self.remove_selected_row)
        self.calculate_button.clicked.connect(self.calculate)
        close_button.clicked.connect(self.reject)

        self._add_default_rows()

    def _add_default_rows(self):
        self.add_row("visibilita", "0.75", "0.5")
        self.add_row("rumore", "0.30", "0.3")
        self.add_row("distanza", "0.55", "0.2")

    def add_row(self, name="", value="", weight=""):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(name))
        self.table.setItem(row, 1, QTableWidgetItem(value))
        self.table.setItem(row, 2, QTableWidgetItem(weight))

    def remove_selected_row(self):
        selected = self.table.currentRow()
        if selected >= 0:
            self.table.removeRow(selected)

    def _to_components(self):
        components = []
        for row in range(self.table.rowCount()):
            name_item = self.table.item(row, 0)
            value_item = self.table.item(row, 1)
            weight_item = self.table.item(row, 2)

            name = (name_item.text() if name_item else "").strip() or f"comp_{row + 1}"
            try:
                value = float((value_item.text() if value_item else "").strip())
                weight = float((weight_item.text() if weight_item else "").strip())
            except ValueError as exc:
                raise InvalidImpactData(
                    f"Riga {row + 1}: valore/peso non numerici."
                ) from exc

            components.append(ImpactComponent(name=name, value=value, weight=weight))

        return components

    def calculate(self):
        try:
            components = self._to_components()
            result = compute_cumulative_impact(components)
        except InvalidImpactData as exc:
            QMessageBox.warning(self, "Dati non validi", str(exc))
            return

        decimals = int(self.decimals_spin.value())
        self.result_label.setText(f"Indice cumulato: {result:.{decimals}f}")


class ImpattoCumulatoPlugin:
    """QGIS plugin main class."""

    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.dialog = None

    def initGui(self):
        self.action = QAction("IMPATTO-CUMULATO: calcolo", self.iface.mainWindow())
        self.action.triggered.connect(self.open_calculator)
        self.iface.addPluginToMenu("IMPATTO-CUMULATO", self.action)

    def unload(self):
        if self.action is not None:
            self.iface.removePluginMenu("IMPATTO-CUMULATO", self.action)
            self.action = None
        self.dialog = None

    def open_calculator(self):
        self.dialog = ImpactCalculatorDialog(self.iface.mainWindow())
        self.dialog.show()
        self.dialog.raise_()
        self.dialog.activateWindow()
