import math
import numpy as np

# --- Helper Functions ----


# Deg/s -> Rad/s
def convert_deg_to_rads(X, Y, Z):
    """
    Converts all values in 3 lists in radian equivalent
    :param X: list X
    :param Y: list Y
    :param Z: list Z
    :return: lists XYZ w/ values converted into radians
    """
    X = [math.radians(x) for x in X]
    Y = [math.radians(x) for x in Y]
    Z = [math.radians(x) for x in Z]
    return X, Y, Z


# Normalize Vectors
def normalize(X, Y, Z):
    """
    Normalizes 3 vectors, XYZ. In the case of a vector with 0 magnitude, to avoid NaN errors,
    the 0 vector is simply returned.
    :param X: list X
    :param Y: list Y
    :param Z: list Z
    :return: normalized vectors XYZ
    """
    # Calculate magnitude of vectors
    mag_X = math.sqrt(sum([x ** 2 for x in X]))
    mag_Y = math.sqrt(sum([x ** 2 for x in Y]))
    mag_Z = math.sqrt(sum([x ** 2 for x in Z]))

    # Normalize vectors (handling 0 cases)
    if mag_X != 0:
        X = [x / mag_X for x in X]
    else:
        X = [0 for x in X]
    if mag_Y != 0:
        Y = [x / mag_Y for x in Y]
    else:
        Y = [0 for x in Y]
    if mag_Z != 0:
        Z = [x / mag_Z for x in Z]
    else:
        Z = [0 for x in Z]

    return X, Y, Z


# Convert V & Theta angles to Quaternions
def v_theta_to_quaternion(v, theta):
    """
    Converts normalized vector v and angle of rotation theta into quaternion format
    :param v: normalized 3d vector, v_x, v_y, v_z
    :param theta: angle of rotation, rads
    :return: quaternion equivalent of v, theta -> wxyz
    """
    v_x, v_y, v_z = v[0], v[1], v[2]
    w = math.cos(theta / 2)
    x = v_x * math.sin(theta / 2)
    y = v_y * math.sin(theta / 2)
    z = v_z * math.sin(theta / 2)
    return w, x, y, z


# Convert Euler Angle to Quaternion
def euler_to_quaternion(yaw, pitch, roll):
    """
    Converts euler (yaw, pitch, roll) to quaternion equivalent (x, x, y, z)
    :param yaw: radians
    :param pitch: radians
    :param roll: radians
    :return: quaternion wxyz
    """
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)
    w = cy * cp * cr + sy * sp * sr
    x = cy * cp * sr - sy * sp * cr
    y = sy * cp * sr + cy * sp * cr
    z = sy * cp * cr - cy * sp * sr
    return w, x, y, z


# Convert Quaternion to Euler (assumes quaternion is normalized)
def quaternion_to_euler(q):
    """
    Converts quaternion wxyz into euler format xyz
    :param q: quaternion
    :return: euler representation, xyz
    """
    W = q[0]
    X = q[1]
    Y = q[2]
    Z = q[3]

    # roll(x - axis rotation)
    sinr_cosp = +2.0 * (W * X + Y * Z)
    cosr_cosp = +1.0 - 2.0 * (X * X + Y * Y)
    roll = math.atan2(sinr_cosp, cosr_cosp)

    # pitch(y - axis rotation)
    sinp = +2.0 * (W * Y - Z * X)
    if abs(sinp) >= 1:
        pitch = np.copysign(math.pi / 2, sinp)  # use 90 degrees if out of range
    else:
        pitch = math.asin(sinp)

    # yaw(z - axis rotation)
    siny_cosp = +2.0 * (W * Z + X * Y)
    cosy_cosp = +1.0 - 2.0 * (Y * Y + Z * Z)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    return roll, pitch, yaw


# Quaternion to conjugate (inverse rotation)
def quaternion_to_conjugate(q):
    """
    Calculates conjugate of quaternion
    :param q: quaternion
    :return: quaternion conjugate
    """
    # q = [s,v] | The conjugate, q* = [s, -v]
    return [q[0], -q[1], -q[2], -q[3]]


# Quaternion Product A * B
def quaternion_product(q1, q2):
    """
    Returns the quaternion product
    :param q1: quaternion q1
    :param q2: quaternion q2
    :return: quaternion product q1 * q2
    """
    Wa = q1[0]
    Wb = q2[0]
    Xa = q1[1]
    Xb = q2[1]
    Ya = q1[2]
    Yb = q2[2]
    Za = q1[3]
    Zb = q2[3]
    x = Xa * Wb + Ya * Zb - Za * Yb + Wa * Xb
    y = -Xa * Zb + Ya * Wb + Za * Xb + Wa * Yb
    z = Xa * Yb - Ya * Xb + Za * Wb + Wa * Zb
    w = -Xa * Xb - Ya * Yb - Za * Zb + Wa * Wb
    return [w, x, y, z]


# Calcs angle between two 3D vectors
def angle_between_vectors(u, v):
    """
    Returns angle between two 3d vectors
    :param u: 3d vector
    :param v: 3d vector
    :return: angle between two vectors
    """
    mag_u = math.sqrt(u[0]**2 + u[1]**2 + u[2]**2)
    mag_v = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    dot_prod = u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
    return math.acos(dot_prod/(mag_u*mag_v))


# Rotates xyz vector by quaternion wxyz
def point_rotation_by_quaternion(v, q):
    """
    Rotates vector xyz by quaternion wxyz
    :param point: 3d vector xyz
    :param q: quaternionn wxyz
    :return: new orientation of vector xyz
    """
    r = [0] + v
    q_conj = [q[0], -q[1], -q[2], -q[3]]
    return quaternion_product(quaternion_product(q, r), q_conj)[1:]

