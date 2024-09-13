
FROM python:3.9-slim


WORKDIR /app


COPY . /app


RUN pip install --no-cache-dir -r requirements.txt


ENV FLASK_APP=workout_service.py
ENV FLASK_ENV=dev


EXPOSE 5000


CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]