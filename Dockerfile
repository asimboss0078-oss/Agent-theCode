FROM python:3.11-slim

WORKDIR /app

# Copy backend files
COPY backend/ /app/backend/
COPY web_ui/ /app/web_ui/

# Install dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Install Flask serve for static files
RUN pip install --no-cache-dir flask-serve

EXPOSE 5000

# Set environment variables
ENV FLASK_APP=backend/app.py
ENV FLASK_ENV=production

# Start the application
CMD ["python3", "backend/app.py"]
