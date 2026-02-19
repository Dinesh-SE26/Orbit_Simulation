
################################ Importing required libraries and files... ################################

from functools import partial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from physics.orbital_equations import Spherical_Coordinates, eccentricity
import config as cfg
import physics.constants as const


def plot_orbit_simulation(pos_traj, vel_traj, t_step, pixels):
    """
    Docstring for plot_data
    
    :param pos_traj: Trajectory Position values
    :param vel_traj: Trajectory Velocity values
    :param t_step: Time array
    :param pixels: Only plots the last pixel points instead of the full orbit for each frames
    """
    def plot_3d():                                                      #3D Plotting
        fig_3d = plt.figure(figsize=cfg.config["figure_size_3d"])
        axis_3d = fig_3d.add_subplot(111, projection="3d")
        axis_3d.set_box_aspect([1,1,1])
        return fig_3d, axis_3d


    def plot_2d():                                                      # 2D Plotting
        fig_2d, axis_2d = plt.subplots()
        return fig_2d, axis_2d
        

    def set_limits_2D(axis):                                            # 2D formatting 
        axis.set_xlabel("Time(s)")
        axis.set_ylabel("Eccentricity(e)")
        axis.set_ylim(-1, 1.2)
        return 


    def add_earth(axis):                                                # Spherical Model(Earth)
        u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:30j]
        x_E, y_E, z_E = Spherical_Coordinates(u, v)
        axis.plot_surface(x_E, y_E, z_E, color = "orange", alpha = 0.7)
        return


    def eccentricity_plot(axis):                                        # 2D eccentricity plotting                      
        ecc, = axis.plot([], [], color = "red")
        ecc_pt = axis.scatter([], [], color = "red", s = 25)
        return ecc, ecc_pt
    
    def eccentricity_data():
        ecc_data =  eccentricity(pos=pos_traj, vel=vel_traj)
        return ecc_data

    def satellite_objects(axis):                                         # Satellite Model and Trial
        sat_trial, = axis.plot([], [], [], color = "gray", alpha = 0.4)
        sat_sph = axis.scatter([], [], [], color = "blue", s = 50)
        return sat_trial, sat_sph


    def set_limits_3D(pos, axis, margin):                                # 3D Figure limits
        limits = np.max(np.abs(pos))
        axis.set_xlim(-limits * margin, limits * margin)
        axis.set_ylim(-limits * margin, limits * margin)
        axis.set_zlim(-limits * margin, limits * margin)
        axis.set_xlabel("X Axis")
        axis.set_ylabel("Y Axis")
        axis.set_zlabel("Z Axis")
        axis.set_title("3D Orbit Simulation", pad = 25)
        return


    def Global_axes_3d(axis):                                             # Axis for 3D figure
        Len_axis = const.R_Earth * 1.5                 

        axis.quiver(0, 0, 0, Len_axis, 0, 0, color='r', arrow_length_ratio=0.1)  # X-axis
        axis.quiver(0, 0, 0, 0, Len_axis, 0, color='g', arrow_length_ratio=0.1)  # Y-axis
        axis.quiver(0, 0, 0, 0, 0, Len_axis, color='b', arrow_length_ratio=0.1)  # Z-axis

        # Label axes
        axis.text(Len_axis, 2e6, 0, 'X', color='r')
        axis.text(0, Len_axis, 0, 'Y', color='g')
        axis.text(0, 0, Len_axis, 'Z', color='b')
        return


    def update_2d(frame, e_plt, e_pt, state_val):                            # Simulation function for 2D figure
        start = max(0 , frame - pixels)
        e_plt.set_data(state_val[:frame, 0], state_val[:frame, 1])
        e_pt.set_offsets([state_val[frame, 0], state_val[frame, 1]])
        return (e_plt, e_pt)


    def update_3d(frame, sat_pt, x_orbit, y_orbit, z_orbit):                       # Simulation function for 3D figure
        start = max(0 , frame - pixels)
        sat_pt._offsets3d = (np.array([x_orbit[frame]]),
                            np.array([y_orbit[frame]]),
                            np.array([z_orbit[frame]]))
        return sat_pt
    

    def animation_2d():                                                             # Simulation for 2D
        fig_2d, ecc_plt, ecc_pt =  setup_2D_scene()
        ecc_data = eccentricity_data()
        simulate_2d = FuncAnimation(fig=fig_2d, 
                                    func=partial(update_2d, e_plt=ecc_plt,e_pt=ecc_pt, state_val=ecc_data), 
                                    frames=range(0, len(t_step), 50), 
                                    interval = cfg.config["interval"],
                                    blit=True)
        return simulate_2d


    def animation_3d():                                                             # Simulation for 3D
        fig_3d, sat_pt, pos_x, pos_y, pos_z = setup_3D_scene()
        simulate_3d = FuncAnimation(fig=fig_3d, func=partial(update_3d, sat_pt=sat_pt, x_orbit=pos_x, y_orbit=pos_y, z_orbit=pos_z), 
                                                                              frames=range(0, len(t_step), 50),
                                                                              interval = cfg.config["interval"])
        return simulate_3d    

    def setup_3D_scene():                                                           # Combines all 3D scenes
        fig_3d, ax_3d = plot_3d()
        add_earth(axis=ax_3d)
        sat_orb, sat_pt = satellite_objects(axis=ax_3d)
        pos_x, pos_y, pos_z = pos_traj[:, 0], pos_traj[:, 1], pos_traj[:, 2]
        ax_3d.plot(pos_x, pos_y, pos_z, color = "blue", alpha = 0.4)
        set_limits_3D(pos=pos_traj, axis=ax_3d, margin=cfg.config["margin"])
        Global_axes_3d(axis=ax_3d)
        return fig_3d, sat_pt, pos_x, pos_y, pos_z

    def setup_2D_scene():                                                           # Combines all 2D scenes
        fig_2d, ax_2d = plot_2d()
        set_limits_2D(axis=ax_2d)
        ecc_plt, ecc_pt = eccentricity_plot(axis=ax_2d)
        ax_2d.set_xlim(t_step[0], t_step[-1])                                         
        return fig_2d, ecc_plt, ecc_pt
    
    return animation_2d(), animation_3d()