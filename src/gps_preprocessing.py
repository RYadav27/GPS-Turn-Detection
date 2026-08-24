import pandas as pd


def convert_coordinate(value, direction):
    """
    Convert NMEA coordinate format into decimal degrees.

    Example:
    2630.6421 N → 26.5107017
    08014.4983 E → 80.2416383
    """

    value = float(value)

    degrees = int(value / 100)

    minutes = value - (degrees * 100)

    decimal_degree = (
        degrees + minutes / 60
    )

    if direction == "S" or direction == "W":
        decimal_degree = -decimal_degree

    return decimal_degree


def convert_gps_time(time_value):
    """
    Convert GPS time HHMMSS.sss
    into seconds from midnight.
    """

    time_value = str(time_value)

    hours = int(time_value[0:2])
    minutes = int(time_value[2:4])
    seconds = float(time_value[4:])

    total_seconds = (
        hours * 3600
        + minutes * 60
        + seconds
    )

    return total_seconds


def read_gps_file(file_path):

    gps_data = []

    with open(
        file_path,
        "r",
        errors="ignore"
    ) as file:

        for line in file:

            line = line.strip()

            # We only need GNRMC records
            if "$GNRMC" not in line:
                continue

            parts = line.split(",")

            if len(parts) < 10:
                continue

            try:

                log_time = parts[0].strip()

                gps_time = parts[2].strip()

                status = parts[3].strip()

                latitude = parts[4].strip()
                latitude_direction = parts[5].strip()

                longitude = parts[6].strip()
                longitude_direction = parts[7].strip()

                speed_knots = parts[8].strip()

                course = parts[9].strip()

                gps_date = parts[10].strip()

                # A means valid GPS position
                if status != "A":
                    continue

                # Convert latitude
                latitude = convert_coordinate(
                    latitude,
                    latitude_direction
                )

                # Convert longitude
                longitude = convert_coordinate(
                    longitude,
                    longitude_direction
                )

                # Convert speed
                speed_knots = float(
                    speed_knots
                )

                speed_kmph = (
                    speed_knots * 1.852
                )

                # Convert GPS time
                gps_seconds = (
                    convert_gps_time(
                        gps_time
                    )
                )

                course = float(course)

                gps_data.append({

                    "Log_Time":
                        log_time,

                    "GPS_Date":
                        gps_date,

                    "GPS_Time":
                        gps_time,

                    "GPS_Seconds":
                        gps_seconds,

                    "Latitude":
                        latitude,

                    "Longitude":
                        longitude,

                    "Speed_knots":
                        speed_knots,

                    "Speed_kmph":
                        speed_kmph,

                    "Course":
                        course
                })

            except (
                ValueError,
                IndexError
            ):

                # Skip records that cannot be read
                continue

    df = pd.DataFrame(
        gps_data
    )

    return df


def create_relative_time(df):

    df = df.copy()

    # Time from the beginning of the GPS data
    first_time = (
        df["GPS_Seconds"].iloc[0]
    )

    df["Time_sec"] = (
        df["GPS_Seconds"]
        - first_time
    )

    return df


def save_processed_data(
    df,
    output_file
):

    df.to_csv(
        output_file,
        index=False
    )

    print(
        "Processed GPS data saved:"
    )

    print(output_file)
