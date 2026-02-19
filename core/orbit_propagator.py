
################################ Importing required libraries and files... ################################

import numpy as np
import config as cfg
from integrators.solve_ivp import runge_kutta_45
from integrators.velocity_verlet import velocity_verlet


def run_solver(solver, y0, end_t):
    start = cfg.config["start"]
    end = end_t
    dt = cfg.config["dt"]

    t_span = (start, end)
    N = int((end - start) / dt) + 1
    t_eval = np.linspace(*t_span, N)

    if solver == "solve_ivp":
        return runge_kutta_45(t_span = t_span,
                              y0 = y0,
                              t_eval = t_eval,
                              method = cfg.config["method"],
                              rtol = cfg.config["rtol"],
                              atol=cfg.config["atol"]
                              )                                                   
                                                    
    elif solver == "Velocity_Verlet":
        return velocity_verlet(state_0 = y0,
                               tim_arr = t_eval
                               )
    else:
        raise ValueError("Solver must be 'solve_ivp' or 'Velocity_Verlet'")


