import rps.robotarium as robotarium
from rps.utilities.transformations import *
from rps.utilities.barrier_certificates import *
from rps.utilities.misc import *
from rps.utilities.controllers import *

import numpy as np

# Instantiate Robotarium object
N = 20
r = robotarium.Robotarium(number_of_agents=N, show_figure=True, save_data=True, update_time=0.1)

# Define goal points by removing orientation from poses
goal_points = generate_initial_conditions(N)

# Get barrier certificates to avoid collisions
uni_barrier_cert = create_unicycle_barrier_certificate(N, safety_radius=0.05)

# define x initially
x = r.get_poses()
r.step()

# While the number of robots at the required poses is less
# than N...
while(np.size(at_pose(x, goal_points)) != N):

    # Get poses of agents
    x = r.get_poses()

    # Unicycle control inputs
    dxu = unicycle_pose_controller(x, goal_points)

    # Create safe input s
    dxu = uni_barrier_cert(dxu, x)

    r.set_velocities(np.arange(N), dxu)
    r.step()
