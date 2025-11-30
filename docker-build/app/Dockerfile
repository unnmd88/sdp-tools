FROM ghcr.io/astral-sh/uv:python3.12-bookworm

# Setup a non-root user
#RUN groupadd --system --gid 999 nonroot \
# && useradd --system --gid 999 --uid 999 --create-home nonroot

WORKDIR /sdp-tools-app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy
# Ensure installed tools can be executed out of the box
ENV UV_TOOL_BIN_DIR=/usr/local/bin

#COPY ./pyproject.toml ./uv.lock ./.python-version .

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY ./app /sdp-tools-app/app
COPY ./pyproject.toml ./uv.lock ./.python-version  /sdp-tools-app


RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Place executables in the environment at the front of the path
ENV PATH="/sdp-tools-app/.venv/bin:$PATH"
ENV PYTHONPATH="/sdp-tools-app:/sdp-tools-app/app"


# Reset the entrypoint, don't invoke `uv`
#ENTRYPOINT []

# Use the non-root user to run our application
#USER nonroot


# Run the FastAPI application by default
# Uses `fastapi dev` to enable hot-reloading when the `watch` sync occurs
# Uses `--host 0.0.0.0` to allow access from outside the container
# Note in production, you should use `fastapi run` instead

WORKDIR /sdp-tools-app/app

RUN chmod +x prestart-app.sh
#ENTRYPOINT ["./prestart-app.sh"]

CMD ["fastapi", "dev", "--host", "0.0.0.0", "main.py", "--port", "8080"]
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
