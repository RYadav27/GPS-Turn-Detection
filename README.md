# GPS-Based Turn Detection and Road Trajectory Analysis

## Project Overview

This project focuses on detecting and analyzing vehicle turning movements using GPS trajectory data.

The GPS data is collected from a moving vehicle and contains information such as GPS time, latitude, longitude, vehicle speed, and course/heading. Python is used to process the raw GPS data, analyze the vehicle trajectory, detect turning movements, and classify them into different turn types.

The project is developed from a **Transportation Engineering** perspective and demonstrates the use of GPS data processing and Python-based trajectory analysis.

---

## Objectives

The main objectives of this project are:

- Process raw GPS trajectory data.
- Extract valid GPS observations from NMEA records.
- Convert latitude and longitude into decimal degrees.
- Convert vehicle speed from knots to km/h.
- Convert GPS coordinates into local X-Y coordinates.
- Reduce GPS trajectory noise using smoothing.
- Calculate vehicle heading changes.
- Detect potential turning movements.
- Classify detected movements as left turns, right turns, and U-turns.
- Calculate turning characteristics such as duration, distance, and speed.
- Visualize the vehicle trajectory and detected turns.

---

## Methodology

The overall workflow of the project is:

Raw GPS Data  
↓  
GPS Preprocessing  
↓  
Coordinate Conversion  
↓  
Trajectory Smoothing  
↓  
Heading Calculation  
↓  
Turn Detection  
↓  
Turn Classification  
↓  
Trajectory Analysis  
↓  
Visualization  
↓  
Results

---

## Project Structure

```text
GPS-Turn-Detection/
│
├── data/
│   └── raw_gps.txt
│
├── src/
│   ├── gps_preprocessing.py
│   ├── coordinate_conversion.py
│   ├── trajectory_smoothing.py
│   ├── heading_calculation.py
│   ├── turn_detection.py
│   ├── turn_classification.py
│   ├── trajectory_analysis.py
│   └── visualization.py
│
├── results/
│
├── main.py
├── requirements.txt
└── README.md
