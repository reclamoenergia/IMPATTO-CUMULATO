"""Entry point per il plugin QGIS IMPATTO-CUMULATO."""


def classFactory(iface):
    """Carica la classe principale del plugin.

    Args:
        iface: QgisInterface fornita da QGIS.
    """
    from .plugin import ImpattoCumulatoPlugin

    return ImpattoCumulatoPlugin(iface)
