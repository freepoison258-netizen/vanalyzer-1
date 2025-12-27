import numpy as np
import matplotlib.pyplot as plt


def plot_calibration(x, y, res, title=None):
    x = np.asarray(x)
    y = np.asarray(y)

    if x.size == 0 or y.size == 0:
        raise ValueError("No data to plot calibration")

    fig, ax = plt.subplots()

    ax.scatter(x, y)

    xx = np.linspace(x.min(), x.max(), 100)
    yy = res["slope"] * xx + res["intercept"]
    ax.plot(xx, yy)

    txt = (
        f"y = {res['slope']:.4g} x + {res['intercept']:.4g}\n"
        f"R² = {res['r2']:.4f}\n"
        f"LOD = {res['lod']:.4g}\n"
        f"LOQ = {res['loq']:.4g}\n"
        f"CI(slope) = [{res['slope_ci'][0]:.4g}, {res['slope_ci'][1]:.4g}]"
    )

    ax.text(0.05, 0.95, txt,
            transform=ax.transAxes,
            va="top")

    ax.set_xlabel("Concentration")
    ax.set_ylabel("Peak area")

    if title:
        ax.set_title(title)

    plt.tight_layout()
    return fig
