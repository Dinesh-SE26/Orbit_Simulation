
### Here I have used velocity verlet to understand about it. You can use any other methods such as Runge-Kutta method
### using solve_ivp from scipy.integrate library



#############      Importing required Libraries...      #############
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

### Initial Conditions
R_earth = 6371e3        # in km
M_earth = 5.972e24      # in km
G_const = 6.6743e-11    # in km
R_Sat = 20e4            # in km (exaggerated Radius)

# R_sat = int(input("At which altitude you want to place the body: ")) * 1e3
R_sat = 1000 * 1e3
steps = 6000
dt = 10                 # in seconds

### Assume if dt = 10, then each step is equal to 10s

def norm(vector):                           # Function for finding norm of a vector
    return np.linalg.norm(vector)

r_vect = np.array([R_earth + R_sat, 0.0])
v_mag = np.sqrt((G_const * M_earth) / norm(r_vect))
v_vect = np.array([0.0, v_mag])

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

# 2D Satellite Body
sat = plt.Circle((0, 0), R_Sat, color='blue')
axis.add_patch(sat)

sat_orbit, = axis.plot([], [], color = "blue")
axis.set_aspect("equal")

# 2D figure Coordinate Limits
limits = np.max(np.abs(positions))
margin = 1.2
axis.set_xlim(-limits * margin, limits * margin)
axis.set_ylim(-limits * margin, limits * margin)

### Simulation...
def update(frame):
    sat_orbit.set_data(positions[:frame, 0], positions[:frame, 1])
    sat.center = positions[frame]
    return

Simulate = FuncAnimation(fig=fig, func=update, frames=steps, interval = 25)

plt.grid()
plt.show()