import numpy as np
from numpy import linalg as LA
import physics.constants as const


def velocity_verlet(state_0, tim_arr):
    r_vect = state_0[: 3].copy()
    v_vect = state_0[3: ].copy()

    n_steps = len(tim_arr)
    dt = tim_arr[1] - tim_arr[0]
    pos_arr = np.zeros((n_steps, 3))
    vel_arr = np.zeros((n_steps, 3))
    time_arr = tim_arr

    pos_arr[0] = r_vect
    vel_arr[0] = v_vect

    for i in range(1, n_steps):
        r_mag = LA.norm(r_vect)
        a = -(const.MU * r_vect) / r_mag**3                   # acceleration at old position
        r_vect += v_vect * dt + 0.5 * a * dt**2               # update position
        r_mag_new = LA.norm(r_vect)                      
        a_new = -(const.MU * r_vect) / r_mag_new**3           # new acceleration
        v_vect += 0.5 * (a + a_new) * dt                      # update velocity
        pos_arr[i] = r_vect
        vel_arr[i] = v_vect

    return pos_arr, vel_arr, time_arr