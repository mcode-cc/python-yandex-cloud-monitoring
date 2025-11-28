ARG PYTHON_IMAGE=python:3.6-alpine
FROM ${PYTHON_IMAGE} AS build

WORKDIR /src

COPY . /src

RUN pip install --upgrade pip && \
    pip install build && \
    python -m build -w

FROM ${PYTHON_IMAGE}

WORKDIR /app

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

COPY --from=build /src/dist/ /dist/
COPY tests /app/tests

RUN pip install --upgrade pip && \
    pip install /dist/*.whl

CMD ["python", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"]
