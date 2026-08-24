import numpy as np


def convert_latlon_to_xy(df):
    """
    Convert latitude and longitude into
    local X-Y coordinates in metres.

    The first GPS point is taken as
    the reference point (0, 0).
    """

    df = df.copy()

    # Mean radius of the Earth in metres
    earth_radius = 6371000

    # First GPS point is used as reference
    reference_lat = np.radians(
        df["Latitude"].iloc[0]
    )

    reference_lon = np.radians(
        df["Longitude"].iloc[0]
    )

    # Convert all latitude and longitude
    # values from degrees to radians
    latitude = np.radians(
        df["Latitude"]
    )

    longitude = np.radians(
        df["Longitude"]
    )

    # Calculate local X coordinate
    # X represents east-west movement
    df["X"] = (
        (longitude - reference_lon)
        * np.cos(reference_lat)
        * earth_radius
    )

    # Calculate local Y coordinate
    # Y represents north-south movement
    df["Y"] = (
        (latitude - reference_lat)
        * earth_radius
    )

    return df
