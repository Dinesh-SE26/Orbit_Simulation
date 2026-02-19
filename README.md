# Orbital Dynamics Simulator

A modular Python-based simulation tool for modelling Earth-centered satellite orbits using numerical integration techniques.


## Project Overview

This project implements a two-body gravitational model to simulate
satellite motion around Earth. The simulator propagates orbital
trajectories using numerical integrators and visualizes the results in
both 2D and 3D.

The simulator currently supports:
- Circular and elliptical orbit generation 
- Adjustable inclination and eccentricity 
- Two numerical solvers: 
	- Adaptive Runge–Kutta (RK45 via SciPy solve_ivp) 
	- Velocity Verlet 
- 2D and 3D visualization of orbital motion 
- Solver comparison for stability assessment


## Physical Model

The current implementation is based on the classical two-body problem.

Assumptions: 

- Earth is modelled as a point mass 
- Gravitational parameter (μ) is constant 
- No perturbations included 
- No atmospheric drag 
- No third-body effects 
- No relativistic corrections


## Numerical Methods

Adaptive Runge–Kutta (RK45)
- Variable step-size integrator 
- Embedded 4th/5th-order Runge–Kutta scheme 
- Automatically adjusts time step based on local truncation error 
- Controlled using relative (rtol) and absolute (atol) tolerances

Velocity Verlet
- Second-order symplectic integrator 
- Fixed time step 
- Designed for Hamiltonian systems with conservative forces 
- Preserves phase-space structure for improved long-term stability


## Project Structure

Core: Initial condition generation and orbit propagation logic. 

Physics: Orbital equations and physical constants. 

Integrators: Velocity Verlet and SciPy RK45 method. 

Visualization: 2D and 3D plotting and animation.

Testing: Solver comparison and validation utilities. 

config.py: Central configuration file. 

main.py: Entry point of the simulator.

requirements.txt: Required dependencies.


## Installation

Install dependencies using:

```bash
pip install -r requirements.txt
```
Required libraries: 
- NumPy
- SciPy 
- Matplotlib


## How to Run

Run: 
python main.py
The program will prompt for orbit type and relevant parameters.

Output:
- 3D orbital animation 
- 2D trajectory visualization 
- Solver comparison plots


## Units and Conventions

- Internal calculations use SI units (meters, seconds, m/s)
- User inputs for altitude, perigee, and apogee are in kilometers
- Angular values are in degrees
- Inclination is applied about the x-axis


## Configuration Parameters

Modify config.py to adjust: 
	- Inclination (i_deg)
	- Number of orbital periods 
	- Time step (dt) 
	- Solver selection 
	- RK method selection 
	- Relative and absolute tolerances 
	- Animation and plot settings


## Current Capabilities

- Two-body orbital propagation
- Circular and elliptical orbit generation
- Inclination handling
- Solver comparison
- 2D and 3D visualization


## Planned Extensions

- Full Keplerian orbital elements (RAAN, argument of periapsis, true anomaly)
- J2 perturbation
- Atmospheric drag
- Solar radiation pressure
- Collision detection
- Ground track plotting



