# cruiseplan/utils/constants.py

# --- Depth/Bathymetry Constants ---

# Sentinel value indicating that depth data is missing, the station is outside
# the bathymetry grid boundaries, or a calculation failed.
# This value is defined in the specs as the fallback depth if ETOPO data is not found.
FALLBACK_DEPTH = -9999.0

# --- Default Cruise Parameters ---
# These are used as code-level fallbacks if a configuration parameter is
# required before the CruiseConfig object is fully initialized or if a
# required field is missing (though the YAML schema should prevent the latter).

# Default vessel transit speed in knots (kt)
DEFAULT_VESSEL_SPEED_KT = 10.0

# Default profile turnaround time in minutes (minutes)
# Corresponds to CruiseConfig.turnaround_time default.
DEFAULT_TURNAROUND_TIME_MIN = 30.0

# Default CTD descent/ascent rate in meters per second (m/s)
# Corresponds to CruiseConfig.ctd_descent_rate/ascent_rate default.
DEFAULT_CTD_RATE_M_S = 1.0
