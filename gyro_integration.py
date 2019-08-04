import pandas as pd
from helperFunctions import *


# Gyro Integration
def gyro_integration():
    # Import data from CSV
    data = pd.read_csv("IMUData.csv")

    # Columns are: (Gyroscope) X, Y, Z | (Accelerometer) X, Y, Z | (Magnetometer) X, Y, Z
    # Vals init in deg / s (Gyroscope), m / s^2 (accelerometer), G [gauss] (magnetometer)
    time = data['time'].tolist()
    gyro_X = data['gyroscope.X'].tolist()
    gyro_Y = data['gyroscope.Y'].tolist()
    gyro_Z = data['gyroscope.Z'].tolist()

    # Convert gyro data (angular velocity) : deg/s -> rad/s
    gyro_X, gyro_Y, gyro_Z = convert_deg_to_rads(gyro_X, gyro_Y, gyro_Z)

    # init orientation = identity quaternion : [w, x, y, z]
    q = [[1, 0, 0, 0]]

    # Start @ t=1 as @ t=0, orientation = [1,0,0,0]
    for i in range(1, len(gyro_X)):
        # --- Gyro Integration (Gyroscope) ---

        # Calc l, magnitude of gyro reading
        l = math.sqrt(gyro_X[i] ** 2 + gyro_Y[i] ** 2 + gyro_Z[i] ** 2)
        # Calc v_xyz, normalized gyro readings
        v_x = gyro_X[i] / l
        v_y = gyro_Y[i] / l
        v_z = gyro_Z[i] / l
        # Calc theta
        theta = l * (time[i] - time[i - 1])
        # Calc quaternion
        w, x, y, z = v_theta_to_quaternion([v_x, v_y, v_z], theta)
        # Calc new q val
        q_new = quaternion_product(q[-1], [w, x, y, z])

        q.append(q_new)

    return q
