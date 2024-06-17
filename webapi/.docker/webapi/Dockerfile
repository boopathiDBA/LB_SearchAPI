FROM python:3.11-slim-bullseye

ENV PATH=/home/nonroot/.local/bin:$PATH

RUN apt-get update
RUN apt-get install -y

RUN adduser nonroot
USER nonroot

WORKDIR /app

COPY --chown=nonroot:nonroot requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install --user -r requirements.txt

COPY --chown=nonroot:nonroot .env /app/.env
COPY --chown=nonroot:nonroot src/ /app/src/

EXPOSE 8080

CMD [ "python", "-m", "uvicorn", "src.delivery.http.main:app", "--env-file", ".env", "--port", "8080", "--host", "0.0.0.0", "--no-server-header", "--no-date-header" ]
