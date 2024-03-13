FROM python:3.12.2

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY poetry.lock pyproject.toml /app/
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /app/
COPY cronfile /etc/cron.d/cronfile

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
