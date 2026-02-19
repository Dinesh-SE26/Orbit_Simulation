import numpy as np
from numpy import linalg as LN
import physics.constants as const


### Equations
def Vis_Viva_EQ(r_vect, a):                                         # Elliptical Orbit/Circular orbit
    """
    Docstring for Vis_Viva_EQ
    
    :param r_vect: Position in vector
    :param a: Semi-major axis
    """
    r_mag = LN.norm(r_vect)
    return np.sqrt(const.MU * (2 / r_mag - 1/a))         

def Gravt_accel(r_vect):                                             # Gravitational Accelaration
    """
    Docstring for Gravt_accel
    
    :param r_vect: Position in vector
    """
    r_mag = LN.norm(r_vect)
    return -(const.MU * r_vect) / r_mag**3           

def Orbital_Period(a):
    """
    Docstring for Orbital_Period

    :param a: Orbital radius/Semi-major axis
    """                                                               # Orbital Period calculates the time period of an orbit
    return 2 * np.pi*np.sqrt(a**3 / const.MU)

def rotation_mat_x(i_rad):                                            # x-axis Rotation Matrix
    """
    Docstring for rotation_mat_x
    
    :param i_rad: Inclination in radians, rotates about x-axis
    """
    x = np.array([
                [1, 0, 0],
                [0, np.cos(i_rad), -1 * np.sin(i_rad)],
                [0, np.sin(i_rad), np.cos(i_rad)]
                ])
    return x

def rotation_mat_y(i_rad):                                             # y-axis Rotation Matrix
    """
    Docstring for rotation_mat_y
    
    :param i_rad: Inclination in radians, rotates about y-axis
    """
    y = np.array([
                [np.cos(i_rad), 0, np.sin(i_rad)],
                [0, 1, 0],
                [-1 * np.sin(i_rad), 0, np.cos(i_rad)]
                ])
    return y

def rotation_mat_z(i_rad):                                             # z-axis Rotation Matrix
    """
    Docstring for rotation_mat_z
    
    :param i_rad: Inclination in radians, rotates about z-axis
    """
    z = np.array([
                [np.cos(i_rad),-1 * np.sin(i_rad), 0],
                [np.sin(i_rad), np.cos(i_rad), 0],
                [0, 0, 1]
                ])
    return z

def Spherical_Coordinates(u, v):                                       # Spherical coordinates formula to create 3D Sphere(Earth)
    """
    Docstring for Spherical_Coordinate
    
    :param u: Longitude from 0 to pi
    :param v: Latitude from 0 to 2 * pi
    """
    x = const.R_Earth * np.sin(v) * np.cos(u)
    y = const.R_Earth * np.sin(v) * np.sin(u)
    z = const.R_Earth * np.cos(v)

    return x, y, z

def eccentricity(pos, vel):                                            # Eccentricity Calculation
    """
    Docstring for eccentricity
    
    :param pos: Position in vector
    :param vel: Velocity in vector
    """                                                                             
    e_t = []

    for step in range(len(pos)):
        h_vect = np.cross(pos[step], vel[step])
        e = ((np.cross(vel[step], h_vect)) / const.MU) - (pos[step] / np.linalg.norm(pos[step]))
        norm_e = [step, np.linalg.norm(e)]
        e_t.append(norm_e.copy())

    return np.array(e_t)

def apply_inclination(i, pos, vel, unit):                              # Inclination Calculation
    """
    Docstring for apply_inclination
    
    :param i: Inclination in degrees, rotates about x-axis
    :param pos: Position in vector
    :param vel: Velocity in vector
    :param unit: degrees/radians
    """
    if unit == "deg":
        if (0 <= i <=180):
            i_rad = np.radians(i)
        else:
            raise ValueError("Value should be under 0 to 180 deg")
    elif unit == "rad":
        if (0 <= i <= np.pi):
            i_rad = i
        else:
            raise ValueError("Value should be under 0 to pi")
    else:
        raise ValueError("unit must be 'deg' or 'rad'")
    
    rot_mat = rotation_mat_x(i_rad)
    pos_rot = pos @ rot_mat.T
    vel_rot = vel @ rot_mat.T
    return pos_rot, vel_rot