import numpy as np
import pandas as pd


def calculate_point_distance(df):
    """
    Calculate the distance travelled between
    two consecutive GPS observations.

    X and Y coordinates are in metres.
    """

    df = df.copy()

    distances = [0.0]

    for i in range(1, len(df)):

        x1 = df.loc[
            i - 1,
            "X_smooth"
        ]

        y1 = df.loc[
            i - 1,
            "Y_smooth"
        ]

        x2 = df.loc[
            i,
            "X_smooth"
        ]

        y2 = df.loc[
            i,
            "Y_smooth"
        ]

        # Distance between two consecutive points
        distance = np.sqrt(
            (x2 - x1) ** 2
            +
            (y2 - y1) ** 2
        )

        distances.append(
            distance
        )

    df["Point_Distance_m"] = distances

    return df


def calculate_turn_statistics(
    df,
    classified_turns
):
    """
    Calculate statistics for every
    detected turning movement.
    """

    results = []

    for turn in classified_turns:

        start = turn[
            "Start_Index"
        ]

        end = turn[
            "End_Index"
        ]

        # Select GPS observations
        # belonging to this turn
        turn_data = df.loc[
            start:end
        ].copy()

        if len(turn_data) == 0:
            continue

        # -----------------------------
        # Time information
        # -----------------------------

        start_time = turn_data[
            "Time_sec"
        ].iloc[0]

        end_time = turn_data[
            "Time_sec"
        ].iloc[-1]

        duration = (
            end_time - start_time
        )

        # -----------------------------
        # Distance
        # -----------------------------

        distance = turn_data[
            "Point_Distance_m"
        ].sum()

        # -----------------------------
        # Speed
        # -----------------------------

        average_speed = turn_data[
            "Speed_kmph"
        ].mean()

        minimum_speed = turn_data[
            "Speed_kmph"
        ].min()

        maximum_speed = turn_data[
            "Speed_kmph"
        ].max()

        # -----------------------------
        # Location
        # -----------------------------

        start_latitude = turn_data[
            "Latitude"
        ].iloc[0]

        start_longitude = turn_data[
            "Longitude"
        ].iloc[0]

        end_latitude = turn_data[
            "Latitude"
        ].iloc[-1]

        end_longitude = turn_data[
            "Longitude"
        ].iloc[-1]

        # Average location of the turn
        turn_latitude = turn_data[
            "Latitude"
        ].mean()

        turn_longitude = turn_data[
            "Longitude"
        ].mean()

        # -----------------------------
        # Create result
        # -----------------------------

        results.append({

            "Turn_ID":
                turn["Turn_ID"],

            "Start_Time_sec":
                start_time,

            "End_Time_sec":
                end_time,

            "Turn_Duration_sec":
                duration,

            "Turn_Type":
                turn["Turn_Type"],

            "Start_Heading_deg":
                turn[
                    "Start_Heading"
                ],

            "End_Heading_deg":
                turn[
                    "End_Heading"
                ],

            "Turn_Angle_deg":
                turn[
                    "Turn_Angle_deg"
                ],

            "Distance_m":
                distance,

            "Average_Speed_kmph":
                average_speed,

            "Minimum_Speed_kmph":
                minimum_speed,

            "Maximum_Speed_kmph":
                maximum_speed,

            "Start_Latitude":
                start_latitude,

            "Start_Longitude":
                start_longitude,

            "End_Latitude":
                end_latitude,

            "End_Longitude":
                end_longitude,

            "Turn_Latitude":
                turn_latitude,

            "Turn_Longitude":
                turn_longitude
        })

    return pd.DataFrame(
        results
    )


def create_turn_summary(
    turn_statistics
):
    """
    Create an overall summary of
    detected turning movements.
    """

    if turn_statistics.empty:

        return pd.DataFrame({
            "Message": [
                "No turns were detected."
            ]
        })

    total_turns = len(
        turn_statistics
    )

    left_turns = (
        turn_statistics["Turn_Type"]
        == "Left Turn"
    ).sum()

    right_turns = (
        turn_statistics["Turn_Type"]
        == "Right Turn"
    ).sum()

    u_turns = (
        turn_statistics["Turn_Type"]
        == "U-Turn"
    ).sum()

    straight_movements = (
        turn_statistics["Turn_Type"]
        == "Straight"
    ).sum()

    average_duration = (
        turn_statistics[
            "Turn_Duration_sec"
        ].mean()
    )

    average_distance = (
        turn_statistics[
            "Distance_m"
        ].mean()
    )

    average_speed = (
        turn_statistics[
            "Average_Speed_kmph"
        ].mean()
    )

    summary = {

        "Total_Turns":
            total_turns,

        "Left_Turns":
            left_turns,

        "Right_Turns":
            right_turns,

        "U_Turns":
            u_turns,

        "Straight_Movements":
            straight_movements,

        "Average_Turn_Duration_sec":
            average_duration,

        "Average_Turn_Distance_m":
            average_distance,

        "Average_Turning_Speed_kmph":
            average_speed
    }

    return pd.DataFrame(
        [summary]
    )
