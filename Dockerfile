# Dockerfile for the Halloween Quiz Flask app
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

WORKDIR /app

# Install ffmpeg so we can optionally convert WAV -> MP3 during image build.
# This makes MP3 fallbacks available without relying on host tools.
RUN apt-get update \
        && apt-get install -y --no-install-recommends ffmpeg ca-certificates \
        && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Convert any WAV files under assets/sounds to MP3 so the image contains both formats.
RUN if [ -d assets/sounds ]; then \
            for f in assets/sounds/*.wav; do \
                [ -f "$f" ] || continue; \
                ffmpeg -y -loglevel error -i "$f" "${f%.wav}.mp3" || echo "ffmpeg conversion failed for $f"; \
            done; \
        fi

# Expose the port (informational)
EXPOSE ${PORT}

# Use gunicorn; allow PORT override via env var
CMD ["sh", "-c", "gunicorn -w 4 -b 0.0.0.0:${PORT:-5000} run:app"]
