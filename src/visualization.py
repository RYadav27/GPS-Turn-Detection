import matplotlib.pyplot as plt


def plot_trajectory(df):
    """
    Plot the complete smoothed vehicle trajectory.
    """

    plt.figure(
        figsize=(10, 7)
    )

    plt.plot(
        df["X_smooth"],
        df["Y_smooth"],
        linewidth=1.5
    )

    plt.xlabel(
        "X Coordinate (m)"
    )

    plt.ylabel(
        "Y Coordinate (m)"
    )

    plt.title(
        "Vehicle GPS Trajectory"
    )

    plt.grid(True)

    plt.axis("equal")

    plt.tight_layout()

    plt.savefig(
        "results/trajectory_map.png",
        dpi=300
    )

    plt.show()


def plot_detected_turns(
    df,
    classified_turns
):
    """
    Plot the vehicle trajectory and mark
    the locations of detected turns.
    """

    plt.figure(
        figsize=(10, 7)
    )

    # Plot complete vehicle trajectory
    plt.plot(
        df["X_smooth"],
        df["Y_smooth"],
        linewidth=1.2,
        label="Vehicle Trajectory"
    )

    # Keep track of which turn types
    # have already been added to the legend
    left_added = False
    right_added = False
    uturn_added = False

    for turn in classified_turns:

        start = turn[
            "Start_Index"
        ]

        end = turn[
            "End_Index"
        ]

        # Take the middle point of the
        # detected turning segment
        middle = (
            start + end
        ) // 2

        x = df.loc[
            middle,
            "X_smooth"
        ]

        y = df.loc[
            middle,
            "Y_smooth"
        ]

        turn_type = turn[
            "Turn_Type"
        ]

        # Left turn
        if turn_type == "Left Turn":

            if not left_added:

                plt.scatter(
                    x,
                    y,
                    s=60,
                    marker="o",
                    label="Left Turn"
                )

                left_added = True

            else:

                plt.scatter(
                    x,
                    y,
                    s=60,
                    marker="o"
                )

        # Right turn
        elif turn_type == "Right Turn":

            if not right_added:

                plt.scatter(
                    x,
                    y,
                    s=60,
                    marker="^",
                    label="Right Turn"
                )

                right_added = True

            else:

                plt.scatter(
                    x,
                    y,
                    s=60,
                    marker="^"
                )

        # U-turn
        elif turn_type == "U-Turn":

            if not uturn_added:

                plt.scatter(
                    x,
                    y,
                    s=70,
                    marker="s",
                    label="U-Turn"
                )

                uturn_added = True

            else:

                plt.scatter(
                    x,
                    y,
                    s=70,
                    marker="s"
                )

    plt.xlabel(
        "X Coordinate (m)"
    )

    plt.ylabel(
        "Y Coordinate (m)"
    )

    plt.title(
        "Vehicle Trajectory with Detected Turns"
    )

    plt.grid(True)

    plt.axis("equal")

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "results/detected_turns.png",
        dpi=300
    )

    plt.show()
