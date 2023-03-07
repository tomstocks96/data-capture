FROM python:3.11.2-slim-buster
WORKDIR /app/
COPY ./pyproject.toml ./pyproject.toml
COPY ./poetry.lock ./poetry.lock
RUN pip install poetry==1.3.2 \
    && poetry install 

CMD [ "poetry", "run", "python", "main.py" ]