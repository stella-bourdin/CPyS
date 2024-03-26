import matplotlib.pyplot as plt

def plot_CPS(tracks, title = ""):
    fig, axs = plt.subplots(1,2, figsize = [10,5])
    fig.suptitle(title)

    # Left plot (B vs. VTL)
    ## Data
    axs[0].plot(tracks.VTL, tracks.B, marker = "o", color = "k")
    ## x-axis
    axs[0].axvline(x=0, color = "k", alpha = 0.5, linestyle = "--", linewidth = 1)
    axs[0].set_xlabel("$-V_T^L$ / m")
    ## y-axis
    axs[0].axhline(y=10, color = "k", alpha = 0.5, linestyle = "--", linewidth = 1)
    axs[0].set_ylabel("B / m")

    #Right plot (VTU vs. VTL)
    ## Data
    axs[1].plot(tracks.VTL, tracks.VTU, marker = "o", color = "k")
    ## x-axis
    axs[1].axvline(x=0, color = "k", alpha = 0.5, linestyle = "--", linewidth = 1)
    axs[1].set_xlabel("$-V_T^L$ / m")
    ## y-axis
    axs[1].axhline(y=0, color = "k", alpha = 0.5, linestyle = "--", linewidth = 1)
    axs[1].set_ylabel("$-V_T^U$ / m")

    plt.tight_layout()
    plt.show()
