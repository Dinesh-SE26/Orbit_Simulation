

config = {"i_deg" : 30,
          "start" : 0,
          "num_periods" : 5,
          "dt" : 1,
          "solver" : "solve_ivp",  # Choose between solve_ivp & Velocity_Verlet
          "method" : "RK45",
          "rtol" : 1e-12,
          "atol" : 1e-12,
          "interval" : 1,
          "trial_length" : 200,
          "margin" : 1.2,
          "figure_size_3d" : (8, 8),
          "unit" : "deg"
          }


