FROM node:22-bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv git ca-certificates \
 && rm -rf /var/lib/apt/lists/*
# Versión fija: súbela a mano después de probar (npm view @companion-ai/feynman version)
ARG FEYNMAN_VERSION=0.5.63
RUN npm install -g @companion-ai/feynman@${FEYNMAN_VERSION}
RUN python3 -m venv /venv && /venv/bin/pip install --no-cache-dir fastapi==0.115.12 uvicorn==0.34.2 httpx==0.28.1
WORKDIR /app
COPY app.py .
RUN useradd -m puente && mkdir /trabajo && chown puente /trabajo
USER puente
ENV FEYNMAN_TELEMETRY=off
EXPOSE 8080
CMD ["/venv/bin/uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
