import numpy as np
from numpy import linalg as LN
import physics.constants as const


def energy_conservation(r, v, t_eval):
    r = LN.norm(r, axis=1)
    v = LN.norm(v, axis=1)
    En = ((v**2 / 2) - ( const.MU / r))
    return np.column_stack([t_eval, En])