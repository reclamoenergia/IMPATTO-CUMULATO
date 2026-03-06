"""QGIS processing algorithm for cumulative wind-visibility analysis."""

from __future__ import annotations

import os

import numpy as np
from osgeo import gdal
from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (
    QgsCoordinateTransform,
    QgsFeature,
    QgsFeatureSink,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsMessageLog,
    QgsPointXY,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterFolderDestination,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterString,
    QgsProject,
    QgsRasterLayer,
    QgsRectangle,
    QgsSpatialIndex,
    Qgis,
)

from .calculator import DemGrid, Turbine, compute_cell_metrics


class CumulativeVisibilityAlgorithm(QgsProcessingAlgorithm):
    INPUT_TURBINES = "INPUT_TURBINES"
    HUB_FIELD = "HUB_FIELD"
    ROT_FIELD = "ROT_FIELD"
    INPUT_DEM = "INPUT_DEM"
    RADIUS = "RADIUS"
    OUTPUT_DIR = "OUTPUT_DIR"
    PREFIX = "PREFIX"
    INPUT_RECEPTORS = "INPUT_RECEPTORS"
    OUTPUT_RECEPTORS = "OUTPUT_RECEPTORS"

    def tr(self, string):
        return QCoreApplication.translate("CumulativeVisibility", string)

    def createInstance(self):
        return CumulativeVisibilityAlgorithm()

    def name(self):
        return "cumulative_visibility"

    def displayName(self):
        return self.tr("Cumulative Wind Visibility")

    def group(self):
        return self.tr("IMPATTO-CUMULATO")

    def groupId(self):
        return "impatto_cumulato"

    def shortHelpString(self):
        return self.tr(
            "Compute Aapp_sum_vis, Hocc, Dsky and ASTOR rasters from turbines and DEM using line-of-sight horizon logic."
        )

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(self.INPUT_TURBINES, self.tr("Turbine points"), [QgsProcessing.TypeVectorPoint]))
        self.addParameter(QgsProcessingParameterField(self.HUB_FIELD, self.tr("Hub height field"), parentLayerParameterName=self.INPUT_TURBINES, type=QgsProcessingParameterField.Numeric))
        self.addParameter(QgsProcessingParameterField(self.ROT_FIELD, self.tr("Rotor diameter field"), parentLayerParameterName=self.INPUT_TURBINES, type=QgsProcessingParameterField.Numeric))
        self.addParameter(QgsProcessingParameterRasterLayer(self.INPUT_DEM, self.tr("DEM raster")))
        self.addParameter(QgsProcessingParameterNumber(self.RADIUS, self.tr("Analysis radius (m)"), QgsProcessingParameterNumber.Double, defaultValue=5000.0, minValue=0.1))
        self.addParameter(QgsProcessingParameterFolderDestination(self.OUTPUT_DIR, self.tr("Output folder")))
        self.addParameter(QgsProcessingParameterString(self.PREFIX, self.tr("Output file prefix"), defaultValue="impact"))
        self.addParameter(QgsProcessingParameterFeatureSource(self.INPUT_RECEPTORS, self.tr("Optional receptor points"), [QgsProcessing.TypeVectorPoint], optional=True))
        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT_RECEPTORS, self.tr("Receptor metrics output"), QgsProcessing.TypeVectorPoint, optional=True))

    def processAlgorithm(self, parameters, context, feedback):
        turbine_source = self.parameterAsSource(parameters, self.INPUT_TURBINES, context)
        dem_layer = self.parameterAsRasterLayer(parameters, self.INPUT_DEM, context)
        hub_field = self.parameterAsString(parameters, self.HUB_FIELD, context)
        rot_field = self.parameterAsString(parameters, self.ROT_FIELD, context)
        radius_m = self.parameterAsDouble(parameters, self.RADIUS, context)
        output_dir = self.parameterAsString(parameters, self.OUTPUT_DIR, context)
        prefix = self.parameterAsString(parameters, self.PREFIX, context)
        receptor_source = self.parameterAsSource(parameters, self.INPUT_RECEPTORS, context)

        if turbine_source is None or dem_layer is None:
            raise QgsProcessingException(self.tr("Missing required inputs."))

        dem_crs = dem_layer.crs()
        if dem_crs.isGeographic():
            feedback.pushWarning(self.tr("DEM CRS is geographic. Distances and radius are treated as layer units."))

        transform_turb = None
        if turbine_source.sourceCrs() != dem_crs:
            transform_turb = QgsCoordinateTransform(turbine_source.sourceCrs(), dem_crs, QgsProject.instance())

        dem_source_path = dem_layer.source().split("|")[0]
        dataset = gdal.Open(dem_source_path)
        if dataset is None:
            raise QgsProcessingException(self.tr("Unable to open DEM dataset."))

        band = dataset.GetRasterBand(1)
        dem_data = band.ReadAsArray().astype(np.float32)
        geotransform = dataset.GetGeoTransform()
        projection = dataset.GetProjection()
        nodata = band.GetNoDataValue()
        dem = DemGrid(dem_data, geotransform, nodata)

        turbines: list[Turbine] = []
        transformed_features: dict[int, QgsFeature] = {}
        index = QgsSpatialIndex()

        for feature in turbine_source.getFeatures():
            if feedback.isCanceled():
                break
            geom = feature.geometry()
            if geom is None or geom.isEmpty():
                continue
            point = geom.asPoint()
            qpt = QgsPointXY(point.x(), point.y())
            if transform_turb:
                qpt = transform_turb.transform(qpt)
            hbase = dem.value_at(qpt.x(), qpt.y())
            if hbase is None:
                continue
            hub_h = float(feature[hub_field])
            rot_d = float(feature[rot_field])
            turbine = Turbine(qpt.x(), qpt.y(), hub_h, rot_d, hbase)
            turbines.append(turbine)

            idx = len(turbines) - 1
            tf = QgsFeature()
            tf.setId(idx)
            tf.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(turbine.x, turbine.y)))
            transformed_features[idx] = tf
            index.addFeature(tf)

        if not turbines:
            raise QgsProcessingException(self.tr("No valid turbines available after DEM sampling."))

        rows, cols = dem_data.shape
        outputs = {
            "AappSumVis": np.full((rows, cols), nodata if nodata is not None else np.nan, dtype=np.float32),
            "Hocc": np.full((rows, cols), nodata if nodata is not None else np.nan, dtype=np.float32),
            "Dsky": np.full((rows, cols), nodata if nodata is not None else np.nan, dtype=np.float32),
            "ASTOR": np.full((rows, cols), nodata if nodata is not None else np.nan, dtype=np.float32),
        }

        for row in range(rows):
            if feedback.isCanceled():
                break
            for col in range(cols):
                hp = float(dem_data[row, col])
                if nodata is not None and np.isclose(hp, nodata):
                    continue
                px, py = dem.pixel_center(row, col)
                search = QgsRectangle(px - radius_m, py - radius_m, px + radius_m, py + radius_m)
                candidate_ids = index.intersects(search)
                if not candidate_ids:
                    outputs["AappSumVis"][row, col] = 0.0
                    outputs["Hocc"][row, col] = 0.0
                    outputs["Dsky"][row, col] = 0.0
                    outputs["ASTOR"][row, col] = 0.0
                    continue
                candidates = [turbines[idx] for idx in candidate_ids]
                metrics = compute_cell_metrics(px, py, hp, candidates, dem, radius_m)
                outputs["AappSumVis"][row, col] = metrics["aapp_sum"]
                outputs["Hocc"][row, col] = metrics["hocc"]
                outputs["Dsky"][row, col] = metrics["dsky"]
                outputs["ASTOR"][row, col] = metrics["astor"]

            feedback.setProgress(int((row + 1) * 100 / rows))

        os.makedirs(output_dir, exist_ok=True)
        output_paths = {}
        for key, arr in outputs.items():
            path = os.path.join(output_dir, f"{prefix}_{key}.tif")
            self._write_geotiff(path, arr, geotransform, projection, nodata)
            output_paths[key] = path
            rlayer = QgsRasterLayer(path, os.path.basename(path))
            if rlayer.isValid():
                QgsProject.instance().addMapLayer(rlayer)

        results = {
            "AappSumVis": output_paths["AappSumVis"],
            "Hocc": output_paths["Hocc"],
            "Dsky": output_paths["Dsky"],
            "ASTOR": output_paths["ASTOR"],
        }

        if receptor_source is not None:
            receptor_fields = QgsFields()
            receptor_fields.append(QgsField("n_vis", QVariant.Int))
            receptor_fields.append(QgsField("d_min", QVariant.Double))
            receptor_fields.append(QgsField("aapp_sum", QVariant.Double))
            receptor_fields.append(QgsField("hocc", QVariant.Double))
            receptor_fields.append(QgsField("dsky", QVariant.Double))
            receptor_fields.append(QgsField("astor", QVariant.Int))

            sink, sink_id = self.parameterAsSink(
                parameters,
                self.OUTPUT_RECEPTORS,
                context,
                receptor_fields,
                receptor_source.wkbType(),
                receptor_source.sourceCrs(),
            )
            if sink is not None:
                transform_receptor = None
                if receptor_source.sourceCrs() != dem_crs:
                    transform_receptor = QgsCoordinateTransform(receptor_source.sourceCrs(), dem_crs, QgsProject.instance())

                for feature in receptor_source.getFeatures():
                    if feedback.isCanceled():
                        break
                    geom = feature.geometry()
                    if geom is None or geom.isEmpty():
                        continue
                    rp = geom.asPoint()
                    dem_pt = QgsPointXY(rp.x(), rp.y())
                    if transform_receptor:
                        dem_pt = transform_receptor.transform(dem_pt)
                    hp = dem.value_at(dem_pt.x(), dem_pt.y())
                    if hp is None:
                        continue
                    search = QgsRectangle(dem_pt.x() - radius_m, dem_pt.y() - radius_m, dem_pt.x() + radius_m, dem_pt.y() + radius_m)
                    candidates = [turbines[idx] for idx in index.intersects(search)]
                    metrics = compute_cell_metrics(dem_pt.x(), dem_pt.y(), hp, candidates, dem, radius_m)

                    out_feature = QgsFeature(receptor_fields)
                    out_feature.setGeometry(geom)
                    out_feature["n_vis"] = metrics["n_vis"]
                    out_feature["d_min"] = metrics["d_min"]
                    out_feature["aapp_sum"] = metrics["aapp_sum"]
                    out_feature["hocc"] = metrics["hocc"]
                    out_feature["dsky"] = metrics["dsky"]
                    out_feature["astor"] = metrics["astor"]
                    sink.addFeature(out_feature, QgsFeatureSink.FastInsert)

                results[self.OUTPUT_RECEPTORS] = sink_id

        QgsMessageLog.logMessage("Cumulative visibility completed.", "IMPATTO-CUMULATO", Qgis.Info)
        return results

    @staticmethod
    def _write_geotiff(path, array, geotransform, projection, nodata):
        driver = gdal.GetDriverByName("GTiff")
        rows, cols = array.shape
        ds = driver.Create(path, cols, rows, 1, gdal.GDT_Float32)
        ds.SetGeoTransform(geotransform)
        ds.SetProjection(projection)
        band = ds.GetRasterBand(1)
        if nodata is not None:
            band.SetNoDataValue(float(nodata))
        band.WriteArray(array)
        band.FlushCache()
        ds.FlushCache()
        ds = None
