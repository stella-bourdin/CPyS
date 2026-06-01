import matplotlib.pyplot as plt


def plot_cps(tracks, title=""):
    """Plot a pair of CPS diagrams for the given track

    Parameters
    ----------
    tracks : xarray.Dataset
        The tracks containing the variables for the CPS parameters (B, VTL, VTU)
    title : str

    """
    fig, axs = plt.subplots(1, 2, figsize=[10, 5])
    fig.suptitle(title)

    # Left plot (B vs. VTL)
    ## Data
    axs[0].plot(tracks.VTL, tracks.B, marker=".", color="k")
    axs[0].scatter(tracks.VTL.isel(record = 0), tracks.B.isel(record = 0), 
                                            marker = "s", color = "k", zorder = 10)
    axs[0].scatter(tracks.VTL.isel(record = -1), tracks.B.isel(record = -1), 
                                            marker = "*", color = "k", zorder = 10)
    ## x-axis
    axs[0].axvline(x=0, color="k", alpha=0.5, linestyle="--", linewidth=1)
    axs[0].set_xlabel("$-V_T^L$ / m")
    ## y-axis
    axs[0].axhline(y=10, color="k", alpha=0.5, linestyle="--", linewidth=1)
    axs[0].set_ylabel("B / m")

    # Right plot (VTU vs. VTL)
    ## Data
    axs[1].plot(tracks.VTL, tracks.VTU, marker=".", color="k")
    axs[1].scatter(tracks.VTL.isel(record = 0), tracks.VTU.isel(record = 0), marker = "s", 
                                            label = "start", color = "k", zorder = 10)
    axs[1].scatter(tracks.VTL.isel(record = -1), tracks.VTU.isel(record = -1), marker = "*", 
                                            label = "end", color = "k", zorder = 10)
    ## x-axis
    axs[1].axvline(x=0, color="k", alpha=0.5, linestyle="--", linewidth=1)
    axs[1].set_xlabel("$-V_T^L$ / m")
    ## y-axis
    axs[1].axhline(y=0, color="k", alpha=0.5, linestyle="--", linewidth=1)
    axs[1].set_ylabel("$-V_T^U$ / m")

    plt.legend()
    plt.tight_layout()
    plt.show()
