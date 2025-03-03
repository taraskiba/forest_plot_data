# import libraries
import leafmap
import ee
import pandas as pd

# initialize the Earth Engine module
ee.Initialize()

# coordinates for the points of interest
point = ee.Geometry.Point([77.54849920033682, 12.91215102400037])

terraclimate = ee.ImageCollection("IDAHO_EPSCOR/TERRACLIMATE")
tmax = terraclimate.select("tmmx")


def scale_image(image):
    return image.multiply(0.1).copyProperties(image, ["system:time_start"])


tmax_scaled = tmax.map(scale_image)

start_date = "2000-01-01"
end_date = "2010-12-31"
filtered = tmax_scaled.filterDate(start_date, end_date)


def extract_values(image):
    return image.reduceRegion(
        reducer=ee.Reducer.first(),
        geometry=point,
        scale=4638.3,  # TerraClimate resolution
    )


extracted = filtered.map(extract_values)
