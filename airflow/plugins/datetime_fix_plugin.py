from airflow.plugins_manager import AirflowPlugin
from datetime import datetime, timezone
import logging

# Get a logger
logger = logging.getLogger("airflow.datetime_fix")

# Store the original utcnow function
original_utcnow = datetime.utcnow

# Create a patched version that returns timezone-aware datetimes
def patched_utcnow():
    # Get the original naive datetime
    naive_dt = original_utcnow()
    # Make it timezone-aware
    aware_dt = naive_dt.replace(tzinfo=timezone.utc)
    # Log this once (to avoid spamming logs)
    if not hasattr(patched_utcnow, 'logged_once'):
        logger.info("Using patched utcnow() that returns timezone-aware datetimes")
        patched_utcnow.logged_once = True
    return aware_dt

# Apply the monkey patch
datetime.utcnow = patched_utcnow

# Create the plugin class
class DatetimeFixPlugin(AirflowPlugin):
    name = "datetime_fix"
    # The plugin doesn't need any specific hooks, operators, etc.
    # The real work is done by the monkey patching above