FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Add current directory code to working directory
ADD . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run main.py when the container launches
CMD ["python3", "main.py"]