from surface_guided_sim.model import Surface
from surface_guided_sim.forces.force import Force
from surface_guided_sim.model import SurfaceGuidedMassSystem

from surface_guided_sim.indexes import *

from typing import Tuple, Iterable

from mayavi import mlab

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import numpy as np


def mayavi_plot_surface(mesh: np.ndarray, trajectory: np.ndarray = None, plot_style=0):
    mlab.figure(1, bgcolor=(1, 1, 1), fgcolor=(0, 0, 0), size=(800, 800))
    mlab.clf()

    # colormap=cool / warm / binary / gray
    if plot_style == 0:
        mlab.mesh(*mesh, opacity=0.3, colormap='cool')  # , color=(0.1, 0.1, 0.6)
        mlab.mesh(*mesh, opacity=0.1, color=(0, 0, 0), representation='wireframe')
    elif plot_style == 1:
        mlab.mesh(*mesh, opacity=1.0, colormap='binary')  # , color=(0.1, 0.1, 0.6)
        mlab.mesh(*mesh, opacity=0.1, color=(0, 0, 0), representation='wireframe')
    else:
        raise Exception("plot_style undefined")

    if trajectory is not None:
        mlab.plot3d(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], color=(1, 0, 0), tube_radius=0.01)
        mlab.points3d(*trajectory[0], color=(0, 0, 1), scale_factor=0.05)

    mlab.orientation_axes()


def _matplotlib_subplot_curves(
        time: np.ndarray,
        tvector: np.ndarray,
        subplot: Tuple,
        title: str,
        ylabel: str,
        legends: Iterable[str]
):
    plt.subplot(*subplot)
    plt.plot(time, tvector)
    plt.title(title)
    plt.xlabel("time (sec)")
    plt.ylabel(ylabel)
    plt.legend(legends)
    plt.grid(True)


def matplotlib_plot_solutions(time: np.ndarray, physics: np.ndarray, system: SurfaceGuidedMassSystem):
    assert time.shape[0] == physics.shape[0]

    plt.figure(figsize=(18, 9))

    plt.subplots_adjust(left=0.08, bottom=0.08, right=1 - 0.04, top=1 - 0.04, wspace=0.1, hspace=0.2)

    _matplotlib_subplot_curves(time, physics[:, Si], (2, 3, 1), "Trajectory", "position (m)", ["X", "Y", "Z"])
    _matplotlib_subplot_curves(time, physics[:, Vi], (2, 3, 2), "Speed", "speed (m/s)", ["Vx", "Vy", "Vz"])
    _matplotlib_subplot_curves(time, physics[:, Eki], (2, 3, 3), "Kinetic energy", "ek (J)", ["Ek"])
    _matplotlib_subplot_curves(time, physics[:, Fi], (2, 3, 4), "SumForce", "force (N)", ["Fx", "Fy", "Fz"])
    _matplotlib_subplot_curves(time, physics[:, nVi], (2, 3, 5), "Absolute speed", "speed (m/s)", ["V"])

    plt.show()


def matplotlib_plot_surface(mesh: np.ndarray, trajectory: np.ndarray = None) -> Axes3D:
    fig = plt.figure(figsize=(6, 6))

    ax: Axes3D = fig.add_subplot(111, projection='3d')

    ul = np.max(mesh)
    ll = np.min(mesh)

    ax.set_xlim3d(ll, ul)
    ax.set_ylim3d(ll, ul)
    ax.set_zlim3d(ll, ul)

    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

    # Plot the surface

    # color map : https://matplotlib.org/tutorials/colors/colormaps.html
    # ax.plot_wireframe()
    ax.plot_surface(*mesh, rstride=1, cstride=1, edgecolor=(0.3, 0.3, 0.3, 0.3), color=(0.9, 0.9, 0.9, 0.1), alpha=0.3, antialiased=True)

    if trajectory is not None:
        ax.plot3D(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], color=(1, 0, 0))
        ax.scatter3D(*trajectory[0, :], s=10, color=(0, 0, 1, 1))
        ax.scatter3D(*trajectory[-1, :], s=10, color=(1, 0, 0, 1))

    return ax
