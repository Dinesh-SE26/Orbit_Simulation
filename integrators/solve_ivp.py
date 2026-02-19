import numpy as np
from physics.orbital_equations import Gravt_accel
from scipy.integrate import solve_ivp

def Gravity_Accel(t, y):                                            # Calculating Gravitaion accelaration      
    pos = y[: 3]
    vel = y[3: ]
    acc = Gravt_accel(r_vect=pos)        
    return np.hstack([vel, acc])


def runge_kutta_45(t_span, y0, t_eval, method, rtol, atol):          # Using RK45 method(default) from "solve_ivp" function
    """
    Docstring for solver

    :param y0: Initial State
    """

    Solution = solve_ivp(Gravity_Accel, t_span=t_span, y0=y0, t_eval=t_eval, method=method, rtol=rtol, atol=atol)
    pos_vect = Solution.y[: 3].T
    vel_vect = Solution.y[3: ].T
    t_eval = Solution.t
    return pos_vect, vel_vect, t_eval