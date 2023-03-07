FROM datacapture:latest
WORKDIR /app/
COPY . .
CMD [ "poetry", "run", "python", "main.py" ]