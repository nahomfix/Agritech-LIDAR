import json
from pathlib import Path

import geopandas
import laspy
import matplotlib.pyplot as plt
import pandas as pd
import pdal
import rasterio
from rasterio.plot import show, show_hist
from shapely.geometry import Point, Polygon

from logger import Logger


class LoadData:
    def __init__(self, bounds_x, bounds_y, region) -> None:
        self.logger = Logger("load_data").get_app_logger()
        self.bounds_x = bounds_x
        self.bounds_y = bounds_y
        self.region = region
        self.data_dir = Path().cwd().parent / "data"

    def fetch_data(self) -> dict:
        """
        Fetch las and geotif data from public aws entwine dataset.

        Returns
        ---
            dict: a dictionary of the year to geopandas dataframe mapping
        """
        pipeline_flow = [
            {
                "type": "readers.ept",
                "filename": f"http://s3-us-west-2.amazonaws.com/usgs-lidar-public/{self.region}/ept.json",
                "resolution": 5,
                "bounds": f"({self.bounds_x}, {self.bounds_y})",
            },
            # {"type": "filters.hag_nn"},
            # {"type": "filters.ferry", "dimensions": "HeightAboveGround=Z"},
            # {
            #     "type": "filters.crop",
            #     "polygon": f"{self.polygon}",
            # },
            # {"type": "filters.locate", "dimension": "Z", "minmax": "max"},
            {
                "type": "writers.las",
                "compression": "false",
                "minor_version": "2",
                "dataformat_id": "0",
                "filename": str(self.data_dir / f"{self.region}.las"),
            },
            {
                "type": "writers.gdal",
                "gdaldriver": "GTiff",
                "output_type": "all",
                "resolution": "5.0",
                "filename": str(self.data_dir / f"{self.region}.tif"),
            },
        ]

        try:
            self.logger.info("Starting data pipeline...")
            pipeline = pdal.Pipeline(json.dumps(pipeline_flow))
            count = pipeline.execute()
            arrays = pipeline.arrays
            metadata = pipeline.metadata
            log = pipeline.log

            # xyz = pipeline.arrays[0][["X", "Y", "Z"]][0]
            self.logger.info("Ran data pipeline successfully!")

            las = laspy.read(str(self.data_dir / f"{self.region}.las"))

            geometry = [
                Point((x, y)) for x, y in zip(las.x.array, las.y.array)
            ]

            self.logger.info("Constructing geopandas dataframe...")

            geo_df = geopandas.GeoDataFrame(
                columns=["elevation_m", "geometry"]
            )
            geo_df["geometry"] = geometry
            geo_df["elevation_m"] = las.z.array

            geo_df.to_csv(
                str(self.data_dir / f"{self.region}.csv"), index=False
            )

            year = self.region.split("_")[-1]

            self.logger.info("Geopandas dataframe ran successfully!")

            return {year: geo_df}

        except Exception as error:
            self.logger.error(error)

    def plot_dem_contours(self) -> None:
        """
        Plots DEM with its contours

        """

        src = rasterio.open(str(self.data_dir / f"{self.region}.tif"))

        fig, ax = plt.subplots(1, figsize=(20, 10))
        show((src), cmap="Greys_r", ax=ax)
        show((src), contour=True, linewidths=0.7, ax=ax)

        plt.show()

    def plot_2D(self) -> None:
        """
        Plots side by side of DEM and histogram.

        """

        src = rasterio.open(str(self.data_dir / f"{self.region}.tif"))

        fig, (ax_rgb, ax_hist) = plt.subplots(1, 2, figsize=(20, 10))
        show((src), cmap="Greys_r", contour=True, ax=ax_rgb)
        show_hist(
            src,
            bins=50,
            histtype="stepfilled",
            lw=0.0,
            stacked=False,
            alpha=0.3,
            ax=ax_hist,
        )

        plt.show()
