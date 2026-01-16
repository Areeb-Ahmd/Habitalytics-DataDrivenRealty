"""
Path configuration for Habitalytics project.
Defines all data and model directory paths.
"""
from pathlib import Path

def get_project_root():
    """
    Find project root directory by looking for 'data' and 'notebooks' folders.
    Works from both notebooks and scripts.
    """
    # If running as a script, this file is in config/paths.py
    if '__file__' in globals():
        # This file is in config/paths.py, so go up 2 levels to project root
        # paths.py -> config/ -> project_root
        return Path(__file__).resolve().parent.parent
    else:
        # If running in notebook, find project root
        current = Path().resolve()
        max_levels = 10
        for _ in range(max_levels):
            if (current / 'data').exists() and (current / 'notebooks').exists():
                return current
            if current.parent == current:
                break
            current = current.parent
        return current

# Get project root
PROJECT_ROOT = get_project_root()

# Define all data paths
DATA_RAW = PROJECT_ROOT / 'data' / 'raw'
DATA_PROCESSED = PROJECT_ROOT / 'data' / 'processed'
DATA_ANALYTICS = PROJECT_ROOT / 'data' / 'analytics'
DATA_RECOMMENDER = PROJECT_ROOT / 'data' / 'recommender'
MODELS_DIR = PROJECT_ROOT / 'models'
SCRIPTS_DIR = PROJECT_ROOT / 'scripts'
NOTEBOOKS_DIR = PROJECT_ROOT / 'notebooks'

def verify_paths():
    """Verify that data directories exist."""
    paths = {
        'Project Root': PROJECT_ROOT,
        'Raw Data': DATA_RAW,
        'Processed Data': DATA_PROCESSED,
        'Analytics Data': DATA_ANALYTICS,
        'Recommender Data': DATA_RECOMMENDER,
        'Models': MODELS_DIR,
        'Scripts': SCRIPTS_DIR,
        'Notebooks': NOTEBOOKS_DIR
    }
    
    print("=" * 60)
    print("Path Configuration")
    print("=" * 60)
    for name, path in paths.items():
        exists = "✓" if path.exists() else "✗"
        print(f"  {exists} {name:20s}: {path}")
    print("=" * 60)
    
    return paths