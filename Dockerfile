FROM python

ENV PYTHONUNBUFFERED 1

ARG GUNICORN_WORKERS
ENV GUNICORN_WORKERS ${GUNICORN_WORKERS:-3}

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["gunicorn", "--workers", "${GUNICORN_WORKERS}", "chatApp.asgi:application"]