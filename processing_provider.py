"""Processing provider registration for IMPATTO-CUMULATO."""

from qgis.core import QgsProcessingProvider

from .processing_algorithm import CumulativeVisibilityAlgorithm


class ImpattoCumulatoProvider(QgsProcessingProvider):
    def id(self):
        return "impatto_cumulato"

    def name(self):
        return "IMPATTO-CUMULATO"

    def longName(self):
        return self.name()

    def loadAlgorithms(self):
        self.addAlgorithm(CumulativeVisibilityAlgorithm())
