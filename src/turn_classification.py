import pandas as pd


def calculate_turn_angle(
    df,
    start_index,
    end_index
):
    """
    Calculate the total heading change
    during a detected turning segment.
    """

    start_heading = df.loc[
        start_index,
        "Heading"
    ]

    end_heading = df.loc[
        end_index,
        "Heading"
    ]

    # Calculate the smallest angle between
    # the starting and ending headings.
    turn_angle = (
        end_heading
        - start_heading
        + 180
    ) % 360 - 180

    return turn_angle


def classify_turn(
    turn_angle,
    straight_threshold=15,
    u_turn_threshold=135
):
    """
    Classify a detected movement based
    on its total heading change.
    """

    # Very small heading change
    if abs(turn_angle) < straight_threshold:
        return "Straight"

    # Large heading change
    if abs(turn_angle) >= u_turn_threshold:
        return "U-Turn"

    # Positive angle = right turn
    if turn_angle > 0:
        return "Right Turn"

    # Negative angle = left turn
    return "Left Turn"


def classify_all_turns(
    df,
    detected_turns
):
    """
    Classify all detected turning segments.
    """

    classified_turns = []

    for turn in detected_turns:

        start_index = turn[
            "Start_Index"
        ]

        end_index = turn[
            "End_Index"
        ]

        # Calculate total heading change
        turn_angle = calculate_turn_angle(
            df,
            start_index,
            end_index
        )

        # Classify the movement
        turn_type = classify_turn(
            turn_angle
        )

        classified_turns.append({

            "Turn_ID":
                turn["Turn_ID"],

            "Start_Index":
                start_index,

            "End_Index":
                end_index,

            "Start_Time_sec":
                turn[
                    "Start_Time_sec"
                ],

            "End_Time_sec":
                turn[
                    "End_Time_sec"
                ],

            "Duration_sec":
                turn[
                    "Duration_sec"
                ],

            "Start_Heading":
                df.loc[
                    start_index,
                    "Heading"
                ],

            "End_Heading":
                df.loc[
                    end_index,
                    "Heading"
                ],

            "Turn_Angle_deg":
                turn_angle,

            "Turn_Type":
                turn_type
        })

    return pd.DataFrame(
        classified_turns
    )
