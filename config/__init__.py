"""
Configuration package for Habitalytics.
Exports all path variables for easy importing.
"""
from .paths import (
    PROJECT_ROOT,
    DATA_RAW,
    DATA_PROCESSED,
    DATA_ANALYTICS,
    DATA_RECOMMENDER,
    MODELS_DIR,
    SCRIPTS_DIR,
    NOTEBOOKS_DIR,
    verify_paths
)

__all__ = [
    'PROJECT_ROOT',
    'DATA_RAW',
    'DATA_PROCESSED',
    'DATA_ANALYTICS',
    'DATA_RECOMMENDER',
    'MODELS_DIR',
    'SCRIPTS_DIR',
    'NOTEBOOKS_DIR',
    'verify_paths',
]