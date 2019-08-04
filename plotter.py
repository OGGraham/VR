import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from helperFunctions import *

# --- Plot Stuff ---


# 3D Orientation Plot
def orientation_plot_3d(q1, q2, q3, halfTime, video, time):
    """
    Produces 3d orientation plot (which has various options)
    :param q1: set of results -> gyro
    :param q2: set of results -> + drift correction
    :param q3: set of results -> + yaw correction
    :param halfTime: bool -> T = half time, F = real time
    :param video: produces a video output instead of a matplotlib interactable plot
    :return: graph/video of orientations
    """
    # Set Real Time or Half Time
    # NB: I am unsure whether these params will produce half/real time on all machines!
    # These params give me correct results but unsure if this is reproducible for you!
    # (I have included the option to output a video file below if that helps)
    if halfTime:
        jump = 5
    else:
        jump = 7

    # Initial Orientations
    U1 = [1, 0, 0]  # X
    U2 = [1, 0, 0]  # X
    U3 = [1, 0, 0]  # X
    V1 = [0, 1, 0]  # Y
    V2 = [0, 1, 0]  # Y
    V3 = [0, 1, 0]  # Y
    W1 = [0, 0, 1]  # Z
    W2 = [0, 0, 1]  # Z
    W3 = [0, 0, 1]  # Z

    # Create figure
    fig = plt.figure(figsize=plt.figaspect(0.25))

    # --- Fig 1 ---
    ax = fig.add_subplot(1, 3, 1, projection='3d')
    Q1 = ax.quiver(0, 0, 0, U1[0], U1[1], U1[2], color='r', length=1)
    Q2 = ax.quiver(0, 0, 0, V1[0], V1[1], V1[2], color='g', length=1)
    Q3 = ax.quiver(0, 0, 0, W1[0], W1[1], W1[2], color='y', length=1)

    # --- Fig 2 ---
    ax2 = fig.add_subplot(1, 3, 2, projection='3d')
    Q4 = ax2.quiver(0, 0, 0, U2[0], U2[1], U2[2], color='r', length=1)
    Q5 = ax2.quiver(0, 0, 0, V2[0], V2[1], V2[2], color='g', length=1)
    Q6 = ax2.quiver(0, 0, 0, W2[0], W2[1], W2[2], color='y', length=1)

    # --- Fig 3 ---
    ax3 = fig.add_subplot(1, 3, 3, projection='3d')
    Q7 = ax3.quiver(0, 0, 0, U3[0], U3[1], U3[2], color='r', length=1)
    Q8 = ax3.quiver(0, 0, 0, V3[0], V3[1], V3[2], color='g', length=1)
    Q9 = ax3.quiver(0, 0, 0, W3[0], W3[1], W3[2], color='y', length=1)

    # Get new values for quivers
    def update_quiver(i, U1, V1, W1, U2, V2, W2, U3, V3, W3):
        """
        Function called by animate. Calculates new quivers.
        :param i: time step
        :param U1: plot 1, X
        :param V1: plot 1, Y
        :param W1: plot 1, Z
        :param U2: plot 2, X
        :param V2: plot 2, Y
        :param W2: plot 2, Z
        :param U3: plot 3, X
        :param V3: plot 3, Y
        :param W3: plot 3, Z
        :return: None, but updates quivers on plots
        """
        # Calc New Vals
        U1 = point_rotation_by_quaternion(U1, q1[jump * i + 1])
        V1 = point_rotation_by_quaternion(V1, q1[jump * i + 1])
        W1 = point_rotation_by_quaternion(W1, q1[jump * i + 1])
        U2 = point_rotation_by_quaternion(U2, q2[jump * i + 1])
        V2 = point_rotation_by_quaternion(V2, q2[jump * i + 1])
        W2 = point_rotation_by_quaternion(W2, q2[jump * i + 1])
        U3 = point_rotation_by_quaternion(U3, q3[jump * i + 1])
        V3 = point_rotation_by_quaternion(V3, q3[jump * i + 1])
        W3 = point_rotation_by_quaternion(W3, q3[jump * i + 1])
        # Clear Axes
        ax.clear()
        ax2.clear()
        ax3.clear()
        # Replot Data
        Q1 = ax.quiver(0, 0, 0, U1[0], U1[1], U1[2], color='r', length=1)
        Q2 = ax.quiver(0, 0, 0, V1[0], V1[1], V1[2], color='g', length=1)
        Q3 = ax.quiver(0, 0, 0, W1[0], W1[1], W1[2], color='y', length=1)
        Q4 = ax2.quiver(0, 0, 0, U2[0], U2[1], U2[2], color='r', length=1)
        Q5 = ax2.quiver(0, 0, 0, V2[0], V2[1], V2[2], color='g', length=1)
        Q6 = ax2.quiver(0, 0, 0, W2[0], W2[1], W2[2], color='y', length=1)
        Q7 = ax3.quiver(0, 0, 0, U3[0], U3[1], U3[2], color='r', length=1)
        Q8 = ax3.quiver(0, 0, 0, V3[0], V3[1], V3[2], color='g', length=1)
        Q9 = ax3.quiver(0, 0, 0, W3[0], W3[1], W3[2], color='y', length=1)
        # Axis Stuff
        ax.set_title("Gyro Only")
        ax.set_xlabel("$X$")
        ax.set_ylabel("$Y$")
        ax.set_zlabel("$Z$")
        ax2.set_title("Gyro + Drift Correction")
        ax2.set_xlabel("$X$")
        ax2.set_ylabel("$Y$")
        ax2.set_zlabel("$Z$")
        ax3.set_title("Gyro + Drift & Yaw Correction")
        ax3.set_xlabel("$X$")
        ax3.set_ylabel("$Y$")
        ax3.set_zlabel("$Z$")
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])
        ax2.set_xticklabels([])
        ax2.set_yticklabels([])
        ax2.set_zticklabels([])
        ax3.set_xticklabels([])
        ax3.set_yticklabels([])
        ax3.set_zticklabels([])
        plt.suptitle("t: %ss" % str(round(time[jump * i + 1], 3)))

    # Animate function -> updates the plots
    anim = animation.FuncAnimation(fig, update_quiver, frames=range(1, int(6958/jump), jump), fargs=(U1, V1, W1, U2, V2, W2, U3, V3, W3),
                                   interval=100, blit=False, repeat=False)

    # Either show plot, or produce a video using the anim data
    if not video:
        plt.show()
    else:
        # Output video
        print("Rendering 3D Plot...")
        # Output vid as mp4
        writer = animation.writers['ffmpeg']
        # 5 Fps keeps at real/half time
        output = writer(fps=5, metadata=dict(artist='Me'), bitrate=1000)
        anim.save('plot.mp4', writer=output)
        print("Done. Check folder.")


# Plots single XYZ vals from singular set of results, q
def orientation_plot_2d(q, val, alpha, alpha_2, time):
    """
    Plots orientation (XYZ values [degrees]) from list of results, q (WXYZ, rads) over time
    :param q: list of orientations, quaternions, rad/s
    :return: graph of XYZ angle vs Time
    """
    # Convert to euler & degrees
    try:
        for i in range(len(q)):
            q[i] = quaternion_to_euler(q[i])
            q[i] = [math.degrees(x) for x in q[i]]
    except IndexError:
        pass

    # Plot Triaxial data side by side (singular plot)
    plt.subplot(1, 1, 1)
    plt.plot(time, [x[0] for x in q], '-')
    plt.plot(time, [x[1] for x in q], '-')
    plt.plot(time, [x[2] for x in q], '-')
    if val == 0:
        plt.title('Orientation vs Time - Gyro')
    elif val == 1:
        plt.title('Orientation vs Time - Gyro + Accelerometer:\nAlpha = ' + str(alpha))
    else:
        plt.title('Orientation vs Time - Gyro + Accelerometer + Magnet:\nAlpha = ' + str(alpha) + ", Alpha2 = " + str(alpha_2))

    plt.legend(['X', 'Y', 'Z'])
    plt.ylabel('Orientation (deg/s)')
    plt.xlabel('Time (s)')
    plt.show()


# Plot XYZ vals from q1, q2, q3 (gyro, +drift, +yaw)
def triaxial_orientation(q_1, q_2, q_3, alpha, alpha_2, time):
    """
    Plots orientation (XYZ values [deg]) from list of results, q (WXYZ, rad) over time
    :param q_1: quaternion list of results 1
    :param q_2: quaternion list of results 2
    :param q_3: quaternion list of results 3
    :return: Graph containing 3 subgraphs, displaying difference in results
    """
    # Convert to Euler & into Degrees
    try:
        for i in range(len(q_1)):
            q_1[i] = quaternion_to_euler(q_1[i])
            q_2[i] = quaternion_to_euler(q_2[i])
            q_3[i] = quaternion_to_euler(q_3[i])
            q_1[i] = [math.degrees(x) for x in q_1[i]]
            q_2[i] = [math.degrees(x) for x in q_2[i]]
            q_3[i] = [math.degrees(x) for x in q_3[i]]
    except IndexError:
        pass

    fig, axs = plt.subplots(3, 3, figsize=(20, 20))

    # Plot Triaxial data side by side (singular plot)
    plt.subplot(3, 1, 1)
    plt.plot(time, [x[0] for x in q_1], '-')
    plt.plot(time, [x[1] for x in q_1], '-')
    plt.plot(time, [x[2] for x in q_1], '-')
    plt.title('Gyro Integration')
    plt.legend(['X', 'Y', 'Z'])
    plt.ylabel('Euler Angle (deg)')

    plt.subplot(3, 1, 2)
    plt.plot(time, [x[0] for x in q_2], '-')
    plt.plot(time, [x[1] for x in q_2], '-')
    plt.plot(time, [x[2] for x in q_2], '-')
    plt.title('Gyro + Accelerometer - Alpha: %s' % str(alpha))
    plt.legend(['X', 'Y', 'Z'])
    plt.ylabel('Euler Angle (deg)')

    plt.subplot(3, 1, 3)
    plt.plot(time, [x[0] for x in q_3], '-')
    plt.plot(time, [x[1] for x in q_3], '-')
    plt.plot(time, [x[2] for x in q_3], '-')
    plt.title('Gyro + Accelerometer + Magnetometer - Alpha: %s, Alpha_2: %s' % (str(alpha), str(alpha_2)))
    plt.legend(['X', 'Y', 'Z'])
    plt.ylabel('Euler Angle (deg)')
    plt.xlabel('Time (s)')

    plt.show()


# Plot vals from data
def triaxial_plot(gX, gY, gZ, aX, aY, aZ, mX, mY, mZ, time):
    """
    PLot data from csv XYZ axis
    :param gX: gyro X
    :param gY: gyro Y
    :param gZ: gyo Z
    :param aX: accelerometer X
    :param aY: accelerometer Y
    :param aZ: accelerometer Z
    :param mX: magnetometer X
    :param mY: magnetometer Y
    :param mZ: magnetometer Z
    :return: Plot w/ 3 subplots showing gyro, accelerometer & magnetometer data
    """
    # Plot Triaxial data side by side (singular plot)
    fig, axs = plt.subplots(3, 3, figsize=(20, 20))
    plt.subplot(3, 1, 1)
    plt.plot(time, gX, '-')
    plt.plot(time, gY, '-')
    plt.plot(time, gZ, '-')
    plt.title('Gyroscope')
    plt.legend(['X', 'Y', 'Z'])
    plt.ylabel('Angular Rate (deg/s)')

    plt.subplot(3, 1, 2)
    plt.plot(time, aX, '-')
    plt.plot(time, aY, '-')
    plt.plot(time, aZ, '-')
    plt.title('Accelerometer')
    plt.legend(['X', 'Y', 'Z'])
    plt.ylabel(r'Acceleration (m/s$^{2}$)')

    plt.subplot(3, 1, 3)
    plt.plot(time, mX, '-')
    plt.plot(time, mY, '-')
    plt.plot(time, mZ, '-')
    plt.title('Magnetometer')
    plt.legend(['X', 'Y', 'Z'])
    plt.ylabel(r'Gauss ($G$)')
    plt.xlabel('Time (s)')

    plt.show()
