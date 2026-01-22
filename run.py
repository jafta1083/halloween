# Lightweight entrypoint for Streamlit deployments
import subprocess
import sys

if __name__ == '__main__':
    # Run the Streamlit app
    subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'src/web_game_streamlit.py'])
