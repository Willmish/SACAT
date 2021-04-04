"""
SETTINGS
"""
import sys

settings = {
    "APP_TITLE":     "SACAT",
    "VERSION" :     "0.1.5.",
    "ALLOWED_FILE_EXTENSIONS" : "*.py;",
    "TEST_COUNT_DEFAULT": 50,
    "TEST_COUNT_MIN": 1,
    "TEST_COUNT_MAX": 100,
    "TEST_COUNT_STEP": 1,
    "TEST_STEP_DEFAULT": 100,
    "TEST_STEP_MIN": 1,
    "TEST_STEP_MAX": 1000,
    "TEST_STEP_STEP": 10,
    "T_SMALL_DEFAULT" :  1.0,
    "T_SMALL_MIN" :  1.0,
    "T_SMALL_MAX" :  5.0,
    "T_SMALL_INC": 1.0,
    "T_SMALL_STEP": 0.5,
    "T_LARGE_DEFAULT" :  10.0,
    "T_LARGE_MIN" :  5.0,
    "T_LARGE_MAX" : sys.maxsize,
    "T_LARGE_STEP" : 1.0,
    "DEFAULT_PLOT_COLOR": "#006400", # dark green
}
