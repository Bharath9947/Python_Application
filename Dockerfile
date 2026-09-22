FROM python:3.13-slim

WORKDIR /flight_app
RUN useradd app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=app:app . .
USER app
EXPOSE 5000
CMD ["python3","app.py"]
