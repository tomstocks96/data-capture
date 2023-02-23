FROM 3.11.2-slim-buster
WORKDIR /app/
COPY . .
RUN pip install poetry==1.3.2 \
    && poetry install \
    && poetry run main.py