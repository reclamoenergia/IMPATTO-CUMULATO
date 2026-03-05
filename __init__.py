"""QGIS entry-point for the IMPATTO-CUMULATO plugin."""


def classFactory(iface):
    """Load ImpattoCumulatoPlugin class for QGIS."""
    from .plugin import ImpattoCumulatoPlugin

    return ImpattoCumulatoPlugin(iface)
