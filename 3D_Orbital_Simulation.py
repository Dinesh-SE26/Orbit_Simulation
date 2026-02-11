
### Here I have used velocity verlet to understand about it. You can use any other methods such as Runge-Kutta method
### using solve_ivp from scipy.integrate library


#############      Importing required Libraries...      #############

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
R_Earth = 6371e3        # in km
M_Earth = 5.972e24      # in kg
G_const = 6.6743e-11    # in N m^2 / kg^2

# Intial Conditions
mu = G_const * M_Earth
steps = 5000            # Each step is equal to dt. Assume if dt = 10, then each step is equal to 10s
dt = 10                 # in seconds
i_deg = 20  # in deg            



Orbit_Select = int(input("Which orbit do you want to perform?\n"        # Choosing the type of Orbit        
                "1.Circular Orbit\n"
                "2.Elliptical Orbit\n"))

if Orbit_Select == 1:
    altitude = int(input("At which distance from earth surface you want to place the satellite in km: ")) * 1e3
    r_peri = altitude + R_Earth
    a = r_peri                                                       # a = r for circular orbit
    print("Executing Circular Orbit....")

elif Orbit_Select == 2:
    r_peri = int(input("Perigee Distance in km: ")) * 1e3 + R_Earth
    r_apo = int(input("Apogee Distance in km: ")) * 1e3 + R_Earth
    a = (r_peri + r_apo) * 0.5                                       # a = (r_perigee + r_apogee) / 2
    print("Executing Elliptical Orbit....")

def norm(vector):                                      # Function for finding norm of a vector
    return np.linalg.norm(vector)

r_vect = np.array([r_peri, 0.0, 0.0])                  # Position towards earth (X Axis)
v_mag = np.sqrt(mu * (2 / norm(r_vect) - 1/a))         # Vis-Viva Equation
v_vect = np.array([0.0, v_mag, 0.0])                   # Velocity should be perpendicular to position (Y Axis)

### Velocit Verlet Integration Method
def velocity_verlet(r_vect, v_vect, step):
    pos_vect = []

    for _ in range(step):
        r_mag = norm(r_vect)
        a = -(mu * r_vect) / r_mag**3                   # Calculating Gravitational Accelaration
        r_vect += v_vect * dt + 0.5 * a * dt**2         # Finding position from old position with Accelaration
        r_mag_new = norm(r_vect)                      
        a_new = -(mu * r_vect) / r_mag_new**3           # Calculating new Gravitational Accelaration using new position vector (One step ahead)
        v_vect += 0.5 * (a + a_new) * dt                # Finding velocity vector
        pos_vect.append(r_vect.copy())

    return np.array(pos_vect)

position = velocity_verlet(r_vect=r_vect, v_vect=v_vect, step=steps)

### Inclination rotation matrix (rotate about x-axis)
i_rad = np.radians(i_deg)                                       #inclination in radians
rot_mat = np.array([[1, 0, 0],                                  # Rotation Matrix about X-axis
                   [0,  np.cos(i_rad), -1 * np.sin(i_rad)], 
                   [0, np.sin(i_rad), np.cos(i_rad)]])

positions = position @ rot_mat.T                        # .T transforms row to column vectors and doing matrix multiplication (@)

x, y, z = positions[:steps, 0], positions[:steps, 1], positions[:steps, 2]

### Plotting 3D
fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection='3d')

# 3D figure Coordinate Limits
limits = np.max(np.abs(positions))
margin = 1.2
ax.set_xlim(-limits * margin, limits * margin)
ax.set_ylim(-limits * margin, limits * margin)
ax.set_zlim(-limits * margin, limits * margin)

# 3D Earth
u_E = np.linspace(0, 2 * np.pi, 30)
v_E = np.linspace(0, np.pi, 30)
u, v = np.meshgrid(u_E, v_E)                    # Creates mesh around the points
E_x = R_Earth * np.sin(v) * np.cos(u)                 # Spherical Coordinate formula        
E_y = R_Earth * np.sin(v) * np.sin(u)
E_z = R_Earth * np.cos(v)
ax.plot_surface(E_x, E_y, E_z, color = 'orange', alpha = 0.7, label = "Earth")

# 2D Satellite Body and Trial
Sat_Mod = ax.scatter([], [], [], color = 'blue', s = 25, label = "Satellite")
Sat_Trail, = ax.plot([], [], [], color = "blue")

# Labels
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.set_zlabel("Z Axis")
ax.set_aspect("equal")

def update(frame):
    Sat_Trail.set_data(x[:frame],y[:frame])
    Sat_Trail.set_3d_properties(z[:frame])

    S_x, S_y, S_z = positions[frame]
    Sat_Mod._offsets3d = ([S_x], [S_y], [S_z])
    return

Simulate = FuncAnimation(fig=fig, func=update, frames=steps, interval = 25)

ax.set_title("3D Orbit Simulation", loc="center",pad = 20)
ax.legend()
ax.grid()
plt.show()

