# Lightweight entrypoint for Gunicorn / Docker deployments
from src.web_game import app

if __name__ == '__main__':
    # Allow running locally with `python run.py`
    app.run(host='0.0.0.0', port=int(__import__('os').environ.get('PORT', 5000)), debug=False)
