import huracanpy
import numpy as np


def theta(tracks):
    """
    Compute the angular direction for every tracks in a dataset.
    All tracks must have at least two points.

    Parameters
    ----------
    tracks (pd.DataFrame): The set of TC points including columns:
        * time
        * lon
        * lat

    Returns
    -------
    thetas (list): The list of angle for each point in the dataset
    """

    az = huracanpy.calc.azimuth(tracks.lon, tracks.lat, tracks.track_id, centering="forward")

    # Replace points at end of the track with previous azimuth
    idx = np.where(np.isnan(az))[0]
    az[idx] = az[idx - 1]

    # Convert to tempest extremes coordinates
    return -1 * (az - 90) % 360
