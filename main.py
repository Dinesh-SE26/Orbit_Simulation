
"""
Orbital Dynamics Simulator
Entry point for orbit selection, propagation, and visualisation.
Units: SI (meters, seconds, degrees) unless specified.
"""

################################ Importing required libraries and files... ################################

import physics.orbital_equations as OE
import core.initial_conditions as IC
import physics.constants as const
import core.orbit_propagator as Orbit_prop
import config as cfg
from visualization.plot import plot_orbit_simulation
from validation.test_plot import test_plotting
import matplotlib.pyplot as plt

def Orbit_selection():

    orbit_sel = int(input("Which orbit do you want to perform?\n"
                "1.Circular Orbit\n"
                "2.Elliptical Orbit\n"))
    
    if orbit_sel == 1:
        altitude = int(input("At which distance from earth surface you want to place the satellite in km: ")) * 1e3
        r_peri, a = IC.Circular_orbit(alt=altitude)

    elif orbit_sel == 2:
        r_peri = int(input("Perigee Distance in km: ")) * 1e3 + const.R_Earth
        r_apo = int(input("Apogee Distance in km: ")) * 1e3 + const.R_Earth
        r_peri, a = IC.Elliptical_Orbit(r_p=r_peri, r_a=r_apo)

    return r_peri, a

r_peri, a = Orbit_selection()

Orb_per = OE.Orbital_Period(a)

end_time = cfg.config["num_periods"] * Orb_per

state_0 = IC.state_vector(r_p=r_peri, a=a)

pos_traj, vel_traj, t_eval = Orbit_prop.run_solver(solver=cfg.config["solver"], y0=state_0, end_t = end_time)

# testing
sec_pos, sec_vel, sec_t = Orbit_prop.run_solver(solver="Velocity_Verlet", y0=state_0, end_t=end_time)
anim = test_plotting(pos_traj, vel_traj, t_eval, sec_pos, sec_vel, sec_t, cfg.config["trial_length"])

pos_rot, vel_rot = OE.apply_inclination(i=cfg.config["i_deg"], pos=pos_traj, vel=vel_traj, unit=cfg.config["unit"])

animate_2d, animate_3d = plot_orbit_simulation(pos_traj=pos_rot, vel_traj=vel_rot, t_step=t_eval, pixels=cfg.config["trial_length"])

plt.show()