FROM python:3.13-alpine

# Install system dependencies
RUN apk update && apk add --no-cache libpq-dev

# Install Poetry
RUN pip install --no-cache-dir uv

# Set the working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./
COPY app/ ./app

# Install dependencies
RUN uv sync --frozen

RUN mkdir -p /app/tmp
RUN ln -s /app/tmp /tmp
VOLUME /tmp

EXPOSE 8000
# Start the application
CMD ["uv", "run", "python", "-m", "app"]
