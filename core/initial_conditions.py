
################################ Importing required libraries and files... ################################

import numpy as np
import physics.orbital_equations as OE
import physics.constants as const


# For Circular Orbit
def Circular_orbit(alt):
    r_p = alt + const.R_Earth
    a = r_p
    return r_p, a

# For Elliptical Orbit
def Elliptical_Orbit(r_p, r_a):
    """
    Docstring for Elliptical_Orbit
        
    :param r_p: Perigee Altitude
    :param r_a: Apogee Altitude
    """
    a = (r_p + r_a) * 0.5
    return r_p, a

# The function calculates the intial velocity using Vis-Viva Equation 
def state_vector(r_p, a):
    """
    Docstring for state_vector
        
    :param r_p: Perigee Altitude
    :param a: Semi-Major Axis
    """
    r_vect = (r_p, 0.0 , 0.0)
    v_mag = OE.Vis_Viva_EQ(r_vect, a)                    
    v_vect = np.array([0.0, v_mag, 0.0])
    state_vect = np.hstack([r_vect, v_vect])
    return state_vect