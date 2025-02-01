# This file makes the tests directory a Python package.
# It allows test discovery to work properly.
# It can be empty, but we can add test configuration if needed.

import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))