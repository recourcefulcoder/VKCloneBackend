# Stage 1 - package installation
FROM python:3.12-alpine as builder

RUN mkdir /app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
COPY requirements.txt /app/
COPY test-req.txt /app/
COPY ../../shared /app/shared

RUN pip install /app/shared
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r test_req.txt

# Stage 2 - building
FROM python:3.12-alpine


COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy the service-specific code
WORKDIR /app

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python", "main.py"]
