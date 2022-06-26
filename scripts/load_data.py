import json
from pathlib import Path

import geopandas
import laspy
import pandas as pd
import pdal
from shapely.geometry import Point, Polygon

from logger import Logger


class LoadData:
    def __init__(self, bounds_x, bounds_y, region) -> None:
        self.logger = Logger("load_data").get_app_logger()
        self.bounds_x = bounds_x
        self.bounds_y = bounds_y
        self.region = region

    def fetch_data(self) -> dict:
        data_dir = Path().cwd().parent / "data"

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
                "filename": str(data_dir / f"{self.region}.las"),
            },
            {
                "type": "writers.gdal",
                "gdaldriver": "GTiff",
                "output_type": "all",
                "resolution": "5.0",
                "filename": str(data_dir / f"{self.region}.tif"),
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

            las = laspy.read(str(data_dir / f"{self.region}.las"))

            geometry = [
                Point((x, y)) for x, y in zip(las.x.array, las.y.array)
            ]

            self.logger.info("Constructing geopandas dataframe...")

            geo_df = geopandas.GeoDataFrame(
                columns=["elevation_m", "geometry"]
            )
            geo_df["geometry"] = geometry
            geo_df["elevation_m"] = las.z.array

            geo_df.to_csv(str(data_dir / f"{self.region}.csv"), index=False)

            year = self.region.split("_")[-1]

            self.logger.info("Geopandas dataframe ran successfully!")

            return {year: geo_df}

        except Exception as error:
            self.logger.error(error)
