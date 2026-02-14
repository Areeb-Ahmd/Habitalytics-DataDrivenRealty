FROM python:3.12-slim AS builder

WORKDIR /app

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# Build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      build-essential \
      gcc \
      libfreetype6-dev \
      libpng-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN python -m pip install --upgrade pip setuptools wheel \
    && python -m pip wheel --wheel-dir /wheels -r requirements.txt


FROM python:3.12-slim AS final

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      fonts-dejavu-core \
      libfreetype6 \
      libpng16-16 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /wheels /wheels
COPY requirements.txt ./

RUN python -m pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt \
    && rm -rf /wheels

# Copy the Streamlit app (includes pages/, datasets/, static/, etc.)
COPY . .

# Cloud Run provides $PORT, default to 8080
EXPOSE 8080

CMD ["sh", "-c", "streamlit run Home.py --server.address=0.0.0.0 --server.port=${PORT:-8080} --server.enableCORS=false --server.enableXsrfProtection=false"]

