import numpy as np
from numpy import linalg as LN

def angular_momentum(r, v, t_eval):
    ang = np.cross(r, v)
    ang_mag = LN.norm(ang, axis=1)
    return np.column_stack([t_eval, ang_mag])