import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from functools import partial
from .energy_conservation import energy_conservation
from .angular_momentum import angular_momentum


def test_plotting(r1, v1, t1, r2, v2, t2, pixels):

    if t2 is not None:
        if np.allclose(t1, t2):
            t_eval = t1
        else:
            raise ValueError("Time Array not matching")
    else:
        t_eval = t1


    def plot_2d():                                                      # 2D Plotting for testing
        fig, axis = plt.subplots(1, 2, figsize=(10,10))
        return fig, axis
    

    def energy_objects(axis, color):
        En_con, = axis.plot([], [], color = color)
        En_con_pt = axis.scatter([], [], color = color, s = 25)
        return En_con, En_con_pt
    

    def Ang_moment_objects(axis, color):
        ang_acc, = axis.plot([], [], color = color)
        ang_acc_pt = axis.scatter([], [], color = color, s = 25)
        return ang_acc, ang_acc_pt

    def update_animation(En_ln_S, En_pt_S, E_data_S, ang_ln_S, ang_pt_S, ang_data_S, En_ln_V, En_pt_V, E_data_V, ang_ln_V, ang_pt_V, ang_data_V, frame):
        start = 0
        
        # Energy
        En_ln_S.set_data(E_data_S[start:frame, 0], E_data_S[start:frame, 1])
        En_pt_S.set_offsets([E_data_S[frame, 0], E_data_S[frame, 1]])
            
        En_ln_V.set_data(E_data_V[start:frame, 0], E_data_V[start:frame, 1])
        En_pt_V.set_offsets([E_data_V[frame, 0], E_data_V[frame, 1]])

        # Angular Momentum
        ang_ln_S.set_data(ang_data_S[start:frame, 0], ang_data_S[start:frame, 1])
        ang_pt_S.set_offsets([ang_data_S[frame, 0], ang_data_S[frame, 1]])

        ang_ln_V.set_data(ang_data_V[start:frame, 0], ang_data_V[start:frame, 1])
        ang_pt_V.set_offsets([ang_data_V[frame, 0], ang_data_V[frame, 1]])

        return (En_ln_S, En_pt_S, En_ln_V, En_pt_V, ang_ln_S, ang_pt_S, ang_ln_V, ang_pt_V)
        
        

    def animate():
        fig_t, En_ln_S, En_pt_S, E_data_S, ang_ln_S, ang_pt_S, ang_data_S, En_ln_V, En_pt_V, E_data_V, ang_ln_V, ang_pt_V, ang_data_V = test_scenes()
        animate_all = FuncAnimation(fig=fig_t, 
                                    func=partial(update_animation, En_ln_S, En_pt_S, E_data_S, ang_ln_S, ang_pt_S, ang_data_S, En_ln_V, En_pt_V, E_data_V, ang_ln_V, ang_pt_V, ang_data_V), 
                                    frames=range(0, len(t_eval), 50), 
                                    interval = 25)
        return animate_all
    

    def axis_limits(axis, E_data_S, ang_data_S, E_data_V, ang_data_V):

        # ENERGY plot
        axis[0].set_xlim(t_eval[0], t_eval[-1])

        E_all = np.hstack([E_data_S[:, 1], E_data_V[:, 1]])
        E_center = (E_all.max() + E_all.min()) / 2
        E_half_range = (E_all.max() - E_all.min()) / 2
        axis[0].set_ylim(E_center - E_half_range , E_center + E_half_range)
        axis[0].set_title("Energy Conservation", pad = 25)

        # ANGULAR MOMENTUM plot
        axis[1].set_xlim(t_eval[0], t_eval[-1])

        H_all = np.hstack([ang_data_S[:, 1], ang_data_V[:, 1]])
        H_center = (H_all.max() + H_all.min()) / 2
        H_half_range = (H_all.max() - H_all.min()) / 2
        axis[1].set_ylim(H_center - H_half_range, H_center + H_half_range)
        axis[1].set_title("Angular Momentum", pad = 25)
        
        return


    def test_scenes():
        fig_t, axis_t = plot_2d()

        En_ln_S, En_pt_S = energy_objects(axis=axis_t[0], color="red")
        ang_ln_S, ang_pt_S = Ang_moment_objects(axis=axis_t[1], color="red")
        E_data_S = energy_conservation(r1, v1, t1)
        ang_data_S = angular_momentum(r1, v1, t1)

        En_ln_V, En_pt_V = energy_objects(axis=axis_t[0], color="blue")
        ang_ln_V, ang_pt_V = Ang_moment_objects(axis=axis_t[1], color="blue")
        E_data_V = energy_conservation(r2, v2, t2)
        ang_data_V = angular_momentum(r2, v2, t2)

        axis_limits(axis_t, E_data_S, ang_data_S, E_data_V, ang_data_V)
        
        def set_labels():
            En_ln_S.set_label("RK45")
            En_ln_V.set_label("Velocity Verlet")
            axis_t[0].legend()

            axis_t[0].set_xlabel("Time(s)")
            axis_t[0].set_ylabel("Specific Mechanical Energy (J/kg)")
            
            ang_ln_S.set_label("RK45")
            ang_ln_V.set_label("Velocity Verlet")
            axis_t[1].legend()

            axis_t[1].set_xlabel("Time(s)")
            axis_t[1].set_ylabel("Specific Angular Momentum (m²/s)")
            
            return
        
        set_labels()

        return fig_t, En_ln_S, En_pt_S, E_data_S, ang_ln_S, ang_pt_S, ang_data_S, En_ln_V, En_pt_V, E_data_V, ang_ln_V, ang_pt_V, ang_data_V
    
    return animate()