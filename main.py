import os
import pandas as pd

from src.gps_preprocessing import (
    read_gps_file,
    create_relative_time,
    save_processed_data
)

from src.coordinate_conversion import (
    convert_latlon_to_xy
)

from src.trajectory_smoothing import (
    smooth_trajectory
)

from src.heading_calculation import (
    prepare_heading,
    calculate_heading_change
)

from src.turn_detection import (
    detect_turns
)

from src.turn_classification import (
    classify_all_turns
)

from src.trajectory_analysis import (
    calculate_point_distance,
    calculate_turn_statistics,
    create_turn_summary
)

from src.visualization import (
    plot_trajectory,
    plot_detected_turns
)


def main():

    print()
    print("==============================")
    print(" GPS TURN DETECTION PROJECT ")
    print("==============================")

    # Create results folder if it does not exist
    os.makedirs(
        "results",
        exist_ok=True
    )

    # --------------------------------
    # 1. Read GPS data
    # --------------------------------

    print("\n1. Reading GPS data...")

    df = read_gps_file(
        "data/raw_gps.txt"
    )

    print(
        "Valid GPS records:",
        len(df)
    )

    if df.empty:

        print(
            "No valid GPS data found."
        )

        return

    # --------------------------------
    # 2. Create relative time
    # --------------------------------

    print(
        "\n2. Creating relative GPS time..."
    )

    df = create_relative_time(
        df
    )

    # --------------------------------
    # 3. Save processed GPS data
    # --------------------------------

    print(
        "\n3. Saving processed GPS data..."
    )

    save_processed_data(
        df,
        "data/processed_gps.csv"
    )

    # --------------------------------
    # 4. Convert coordinates
    # --------------------------------

    print(
        "\n4. Converting coordinates..."
    )

    df = convert_latlon_to_xy(
        df
    )

    # --------------------------------
    # 5. Smooth trajectory
    # --------------------------------

    print(
        "\n5. Smoothing trajectory..."
    )

    df = smooth_trajectory(
        df,
        window_size=5
    )

    # --------------------------------
    # 6. Calculate heading
    # --------------------------------

    print(
        "\n6. Calculating heading..."
    )

    df = prepare_heading(
        df
    )

    df = calculate_heading_change(
        df
    )

    # --------------------------------
    # 7. Detect turns
    # --------------------------------

    print(
        "\n7. Detecting turns..."
    )

    df, detected_turns = detect_turns(
        df,
        window_size=20,
        turn_threshold=25,
        minimum_points=5
    )

    print(
        "Candidate turns detected:",
        len(detected_turns)
    )

    # --------------------------------
    # 8. Classify turns
    # --------------------------------

    print(
        "\n8. Classifying turns..."
    )

    classified_turns = classify_all_turns(
        df,
        detected_turns
    )

    # --------------------------------
    # 9. Calculate distance
    # --------------------------------

    print(
        "\n9. Calculating trajectory distance..."
    )

    df = calculate_point_distance(
        df
    )

    # --------------------------------
    # 10. Calculate turn statistics
    # --------------------------------

    print(
        "\n10. Calculating turn statistics..."
    )

    turn_statistics = (
        calculate_turn_statistics(
            df,
            classified_turns
        )
    )

    # --------------------------------
    # 11. Save detected turns
    # --------------------------------

    print(
        "\n11. Saving detected turns..."
    )

    turn_statistics.to_csv(
        "results/detected_turns.csv",
        index=False
    )

    # --------------------------------
    # 12. Create Excel summary
    # --------------------------------

    print(
        "\n12. Creating Excel results..."
    )

    summary = create_turn_summary(
        turn_statistics
    )

    with pd.ExcelWriter(
        "results/turn_statistics.xlsx"
    ) as writer:

        turn_statistics.to_excel(
            writer,
            sheet_name="Turn Details",
            index=False
        )

        summary.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

    # --------------------------------
    # 13. Create trajectory plot
    # --------------------------------

    print(
        "\n13. Creating trajectory map..."
    )

    plot_trajectory(
        df
    )

    # --------------------------------
    # 14. Plot detected turns
    # --------------------------------

    print(
        "\n14. Plotting detected turns..."
    )

    plot_detected_turns(
        df,
        classified_turns
    )

    # --------------------------------
    # 15. Final message
    # --------------------------------

    print()
    print("==============================")
    print(" ANALYSIS COMPLETED ")
    print("==============================")

    print(
        "\nProcessed GPS:"
    )

    print(
        "data/processed_gps.csv"
    )

    print(
        "\nDetected turns:"
    )

    print(
        "results/detected_turns.csv"
    )

    print(
        "\nTurn statistics:"
    )

    print(
        "results/turn_statistics.xlsx"
    )

    print(
        "\nTrajectory plots:"
    )

    print(
        "results/trajectory_map.png"
    )

    print(
        "results/detected_turns.png"
    )


if __name__ == "__main__":
    main()
