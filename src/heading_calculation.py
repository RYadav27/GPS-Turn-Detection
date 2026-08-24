import pandas as pd


def prepare_heading(df):
    """
    Use the GPS Course value as the vehicle heading.
    """

    df = df.copy()

    df["Heading"] = df["Course"]

    return df


def calculate_heading_change(df):
    """
    Calculate heading change between
    consecutive GPS observations.
    """

    df = df.copy()

    heading_change = [0.0]

    for i in range(1, len(df)):

        previous_heading = df.loc[
            i - 1,
            "Heading"
        ]

        current_heading = df.loc[
            i,
            "Heading"
        ]

        if pd.isna(previous_heading) or pd.isna(current_heading):

            heading_change.append(
                float("nan")
            )

            continue

        # Handle the 0/360 degree problem
        difference = (
            current_heading
            - previous_heading
            + 180
        ) % 360 - 180

        heading_change.append(
            difference
        )

    df["Heading_Change"] = (
        heading_change
    )

    return df
