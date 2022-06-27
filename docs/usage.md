# Usage

Below are the functions defined in this package

## fetch_data

```
def fetch_data(self) -> dict:
```

Fetches las and geotif data from public aws entwine dataset.

## plot_dem_contours

```
def plot_dem_contours(self) -> None:
```

Plots DEM with its contours

## plot_2D

```
def plot_2D(self) -> None:
```

Plots side by side of DEM and histogram.

## plot_heatmap

```
def plot_heatmap(self, year: str, data_dict: dict) -> None:
```

Plots a heatmap view of a terrain

## Parameters

year: str

-   the year of the desired geopandas data

data_dict: dict

-   the dictionary mapping of the year to its geopandas data

## plot_3D

```
def plot_3D(self, year: str, data_dict: dict) -> None:
```

Plots a 3D view of a terrain

## Parameters

year: str

-   the year of the desired geopandas data

data_dict: dict

-   the dictionary mapping of the year to its geopandas data
