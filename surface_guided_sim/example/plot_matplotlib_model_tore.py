from surface_guided_sim.model import *
from surface_guided_sim.surface import Tore, Plan

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np

tore = Tore(0.5, 1.0)
plan = Plan(0.0, 0.0)

surface = tore

######################################
# Simulation
######################################
s0 = np.array([
    1.0, 0.0,
    np.pi/2, 0.0
])

gdir = np.array([
    0.0,
    -1.0,
    -0.1
])

sim = SurfaceGuidedFallMassSystem(surface, s0, dir=gdir)

time = np.linspace(0, 5, 1000)

data = sim.solve(time)

# build trajectory
trajectory = sim.surface.trajectory(data[:, 0::2])
# speed = sim.surface.speed(data)
# kinetic_energy = 1/2*sim.m*np.linalg.norm(speed, 2)**2

# build speed


######################################
# Plot
######################################
U, V = surface.mesh(80, 20)
surface_mesh = surface.buildsurface(U, V)


if 1:
    fig = plt.figure()
    ax: Axes3D = fig.add_subplot(111, projection='3d')

    ul = np.max(surface_mesh)
    ll = np.min(surface_mesh)

    ax.set_xlim3d(ll, ul)
    ax.set_ylim3d(ll, ul)
    ax.set_zlim3d(ll, ul)

    # Plot the surface
    ax.plot_surface(*surface_mesh, color=(1.0, 1.0, 1.0, 0.25), rstride=1, cstride=1)

    ax.plot3D(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], color=(1, 0, 0))

    plt.figure()
    plt.subplot(1, 2, 1)
    plt.title("position")
    plt.xlabel("time (sec)")
    plt.ylabel("parameters")
    plt.plot(time, data[:, 0::2])
    plt.legend(["u", "v"])
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.title("speed")
    plt.xlabel("time (sec)")
    plt.ylabel("dt parameters")
    plt.plot(time, data[:, 1::2])
    plt.legend(["du", "dv"])
    plt.grid(True)

    plt.show()  # work for matplotlib & mlab

