import pandas as pd
from gyro_integration import gyro_integration
from drift_correction import drift_correction
from yaw_correction import yaw_correction
from plotter import *

# --- READ ME ---

"""
- Python v3.6.5 used.

- Run the file from a command line and it will display all of the relevant
  graphs/figures one after another.

- The graphs that are produce you can control by scrolling to the bottom: I have
  included a few bools for you to make things easy. The default setting which I 
  have left will display all required graphs, starting with the 3d animated plot,
  followed by the other 2 tri-axial plots.
  
- The helper functions are all the functions from part 1 + a few extras (see helpderFunctions.py).

- Part 2,3 & 4 are all within their own files: part 2 -> gyro_integration, part 3 -> drift_correction,
  part 4 -> yaw_correction.
  
- Each file contains the prev. implemenation + the changes from the next section i.e. yaw correction = 
  drift correction + extra stuff: yaw > drift > gyro

- If you wish to change alpha values, these are located on lines 46-47
  

- Specifically regarding the 3d plot, use the halfTime param (again scroll down) to set
  whether half speed or not.

- Use the video param to output a video (requires FFMPEG installed)

"""

# --- Set Alpha values & Load data for producing graphs ---

# Set values of alpha (defaults give best results, alpha=0.05, alpha_2=0.00001)
alpha = 0.05  # Accelerometer
alpha_2 = 0.00001  # Magnetometer

# Generate 3 sets of data
q1 = gyro_integration()
q2 = drift_correction(alpha)
q3 = yaw_correction(alpha, alpha_2)

# Data Needed for Graphs
data = pd.read_csv("IMUData.csv")
time = data['time'].tolist()
gyro_X = data['gyroscope.X'].tolist()
gyro_Y = data['gyroscope.Y'].tolist()
gyro_Z = data['gyroscope.Z'].tolist()
accel_X = data['accelerometer.X'].tolist()
accel_Y = data['accelerometer.Y'].tolist()
accel_Z = data['accelerometer.Z'].tolist()
magnet_X = data['magnetometer.X'].tolist()
magnet_Y = data['magnetometer.Y'].tolist()
magnet_Z = data['magnetometer.Z'].tolist()
gyro_X, gyro_Y, gyro_Z = convert_deg_to_rads(gyro_X, gyro_Y, gyro_Z)


# --- Produce Plots ---

# Choose here what plots you want to produce
orientation_3d = True  # Orientation Tri-axial 3d
orientation_2d = True  # Orientation Tri-axial 2d
triax_plot = True  # CSV Data
plot_gyro = True  # Gyro
plot_tilt = True  # Gyro + Drift Correction
plot_yaw = True  # Gyro + Drift + Yaw Correction

halfTime = False  # Param for orientation_3d
video = False  # Param for orientation_3d

# --- Produce Graphs ---
if orientation_3d:
    orientation_plot_3d(q1, q2, q3, halfTime, video, time)
if orientation_2d:
    triaxial_orientation(q1, q2, q3, alpha, alpha_2, time)
if triax_plot:
    triaxial_plot(gyro_X, gyro_Y, gyro_Z, accel_X, accel_Y, accel_Z, magnet_X, magnet_Y, magnet_Z, time)
if plot_gyro:
    orientation_plot_2d(q1, 0, alpha, alpha_2, time)
if plot_tilt:
    orientation_plot_2d(q2, 1, alpha, alpha_2, time)
if plot_yaw:
    orientation_plot_2d(q3, 2, alpha, alpha_2, time)

print("Finished.")
