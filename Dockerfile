
# 1. Use Python base image
FROM python:3.12-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements file
COPY requirements.txt .

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy project files
COPY . .

# 6. Expose Flask port
EXPOSE 5000

# 7. Start Flask application
CMD ["python", "app.py"]
