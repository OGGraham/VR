import pandas as pd
from helperFunctions import *


# Drift correction
def drift_correction(alpha):
    # Import data from CSV
    data = pd.read_csv("IMUData.csv")

    # Columns are: (Gyroscope) X, Y, Z | (Accelerometer) X, Y, Z | (Magnetometer) X, Y, Z
    # Vals init in deg / s (Gyroscope), m / s^2 (accelerometer), G [gauss] (magnetometer)
    time = data['time'].tolist()
    gyro_X = data['gyroscope.X'].tolist()
    gyro_Y = data['gyroscope.Y'].tolist()
    gyro_Z = data['gyroscope.Z'].tolist()
    accel_X = data['accelerometer.X'].tolist()
    accel_Y = data['accelerometer.Y'].tolist()
    accel_Z = data['accelerometer.Z'].tolist()

    # Convert gyro data (angular velocity) : deg/s -> rad/s
    gyro_X, gyro_Y, gyro_Z = convert_deg_to_rads(gyro_X, gyro_Y, gyro_Z)

    # Normalize accel & magnet data
    accel_X, accel_Y, accel_Z = normalize(accel_X, accel_Y, accel_Z)

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

        # --- Pitch & Roll Drift Correction (Accelerometer) ---

        # Transform accelerometer to global frame
        # a^ = q^{-1} * a- * q  (multiply in reverse order)
        q_inverse = quaternion_to_conjugate(q_new)
        a_hat = quaternion_product(q_new, quaternion_product([0, accel_X[i], accel_Y[i], accel_Z[i]], q_inverse))[1:]
        # Calc angle between a^xyz & (0, 0, 1) - Z axis is up
        phi = angle_between_vectors([a_hat[0], a_hat[1], a_hat[2]], [0, 0, 1])
        # Tilt axis (y, -x, 0)
        t = [a_hat[1], -a_hat[0], 0]
        # Obtain q(t, -alpha*phi)
        theta = - alpha * phi
        w, x, y, z = v_theta_to_quaternion([t[0], t[1], t[2]], theta)
        # Correct for drift
        q_new = quaternion_product(q_new, [w, x, y, z])

        q.append(q_new)

    return q
