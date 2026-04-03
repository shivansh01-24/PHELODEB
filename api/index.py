import sys
import os

# Add the project root to the python path so imports work correctly on Vercel
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import app

# Vercel requires the app variable to be exposed
if __name__ == '__main__':
    app.run()
