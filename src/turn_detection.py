import pandas as pd


def calculate_cumulative_heading_change(
    df,
    window_size=20
):
    """
    Calculate the cumulative heading change
    over a moving window.

    For 10 Hz GPS data, 20 points represent
    approximately 2 seconds.
    """

    df = df.copy()

    # Add small heading changes over the window
    df["Cumulative_Heading_Change"] = (
        df["Heading_Change"]
        .rolling(
            window=window_size,
            min_periods=1
        )
        .sum()
    )

    return df


def mark_turn_points(
    df,
    turn_threshold=25
):
    """
    Mark GPS observations where the cumulative
    heading change is large enough to indicate
    a possible turning movement.
    """

    df = df.copy()

    df["Turn_Flag"] = (
        df["Cumulative_Heading_Change"]
        .abs()
        >= turn_threshold
    )

    return df


def find_turn_segments(
    df,
    minimum_points=5
):
    """
    Find the start and end points of each
    possible turning movement.
    """

    turn_segments = []

    turn_started = False
    start_index = None

    for i in range(len(df)):

        turn_flag = df.loc[
            i,
            "Turn_Flag"
        ]

        # Start of a turn
        if (
            turn_flag
            and not turn_started
        ):

            start_index = i

            turn_started = True

        # End of a turn
        elif (
            not turn_flag
            and turn_started
        ):

            end_index = i - 1

            # Ignore very short segments
            if (
                end_index - start_index
                + 1
                >= minimum_points
            ):

                turn_segments.append({

                    "Start_Index":
                        start_index,

                    "End_Index":
                        end_index
                })

            turn_started = False
            start_index = None

    # If the last observation is still
    # inside a turning segment
    if turn_started:

        end_index = len(df) - 1

        if (
            end_index - start_index
            + 1
            >= minimum_points
        ):

            turn_segments.append({

                "Start_Index":
                    start_index,

                "End_Index":
                    end_index
            })

    return turn_segments


def add_turn_times(
    df,
    turn_segments
):
    """
    Add start time and end time to each
    detected turning segment.
    """

    turns = []

    for turn_id, turn in enumerate(
        turn_segments,
        start=1
    ):

        start = turn[
            "Start_Index"
        ]

        end = turn[
            "End_Index"
        ]

        start_time = df.loc[
            start,
            "Time_sec"
        ]

        end_time = df.loc[
            end,
            "Time_sec"
        ]

        duration = (
            end_time
            - start_time
        )

        turns.append({

            "Turn_ID":
                turn_id,

            "Start_Index":
                start,

            "End_Index":
                end,

            "Start_Time_sec":
                start_time,

            "End_Time_sec":
                end_time,

            "Duration_sec":
                duration
        })

    return turns


def detect_turns(
    df,
    window_size=20,
    turn_threshold=25,
    minimum_points=5
):
    """
    Complete turn detection process.
    """

    # Step 1:
    # Calculate cumulative heading change
    df = calculate_cumulative_heading_change(
        df,
        window_size
    )

    # Step 2:
    # Mark possible turning points
    df = mark_turn_points(
        df,
        turn_threshold
    )

    # Step 3:
    # Find continuous turning segments
    turn_segments = find_turn_segments(
        df,
        minimum_points
    )

    # Step 4:
    # Add time information
    turns = add_turn_times(
        df,
        turn_segments
    )

    return df, turns
