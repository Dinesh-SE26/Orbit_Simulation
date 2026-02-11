
### Here I have used velocity verlet to understand about it. You can use any other methods such as Runge-Kutta method
### using solve_ivp from scipy.integrate library



#############      Importing required Libraries...      #############
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

### Constants
R_earth = 6371e3        # in km
M_earth = 5.972e24      # in kg
G_const = 6.6743e-11    # in N m^2 / kg^2

### Initial Conditions
Sat_pos = int(input("At which altitude you want to place the body: ")) * 1e3
dt = 10                 # in seconds
steps = 6000            # Each step is equal to dt. Assume if dt = 10, then each step is equal to 10s

def norm(vector):                           # Function for finding norm of a vector
    return np.linalg.norm(vector)

r_vect = np.array([R_earth + Sat_pos, 0.0])                    # Position towards earth (X Axis)
v_mag = np.sqrt((G_const * M_earth) / norm(r_vect))            # Orbital Speed
v_vect = np.array([0.0, v_mag])                                # Velocity should be perpendicular to position (Y Axis)

def velocity_verlet(r_vect, v_vect, steps):
    positions = []

    for _ in range(steps):
        r_mag = norm(r_vect)
        a = -(G_const * M_earth * r_vect) / r_mag**3            # Calculating Gravitational Accelaration
        r_vect += v_vect * dt + 0.5 * a * dt**2                 # Finding position from old position with Accelaration
        r_mag_new = norm(r_vect)                      
        a_new = -(G_const * M_earth * r_vect) / r_mag_new**3    # Calculating new Gravitational Accelaration using new position vector (One step ahead)
        v_vect += 0.5 * (a + a_new) * dt                        # Finding velocity vector
        positions.append(r_vect.copy())

    return np.array(positions)

positions = velocity_verlet(r_vect=r_vect, v_vect=v_vect, steps=steps)

### Plotting
fig, axis = plt.subplots()

# 2D Earth
Earth_sim = plt.Circle([0, 0], R_earth, color = 'Orange')
axis.add_patch(Earth_sim)

# 2D Satellite Body and Trial
Sat_sim = axis.scatter([], [], color = "blue", s = 40)
Sat_trial, = axis.plot([], [], color = "blue")

# 2D figure Coordinate Limits
limits = np.max(np.abs(positions))
margin = 1.5
axis.set_xlim(-limits * margin, limits * margin)
axis.set_ylim(-limits * margin, limits * margin)

# Labels
axis.set_xlabel("X Axis")
axis.set_ylabel("Y Axis")
Earth_sim.set_edgecolor("black")
Earth_sim.set_label("Earth")
Sat_sim.set_label("Satellite")
axis.set_aspect("equal")

### Simulation...
def update(frame):
    Sat_sim.set_offsets(positions[frame])
    Sat_trial.set_data(positions[:frame, 0], positions[:frame, 1])
    return

Simulate = FuncAnimation(fig=fig, func=update, frames=steps, interval = 25)

axis.set_title("2D Orbit Simulation",loc='center', pad=15)
axis.legend()
axis.grid()
plt.show()