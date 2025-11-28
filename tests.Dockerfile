ARG PYTHON_IMAGE=python:3.6-alpine
FROM ${PYTHON_IMAGE} AS build

WORKDIR /src

COPY . /src

RUN pip install --upgrade pip && \
    pip install build && \
    python -m build -w

FROM ${PYTHON_IMAGE}

WORKDIR /app

RUN if command -v apk >/dev/null 2>&1; then \
        apk add --no-cache gcc musl-dev libffi-dev openssl-dev; \
    elif command -v apt-get >/dev/null 2>&1; then \
        apt-get update && apt-get install -y gcc libffi-dev libssl-dev && rm -rf /var/lib/apt/lists/*; \
    fi

COPY --from=build /src/dist/ /dist/
COPY tests /app/tests

RUN pip install --upgrade pip && \
    pip install /dist/*.whl

CMD ["python", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"]
