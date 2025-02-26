# Use an official Python image 
FROM python:3.12-slim

# Set the working directory in the container 
WORKDIR /app 

# Copy requirements.txt 
COPY requirements.txt .

# Install dependencies 
RUN pip install --no-cache-dir -r requirements.txt 

# Copy the rest of the project files
COPY . .

# Expose the port Flask runs on 
EXPOSE 5000 

# Command to run the application 
CMD ["python", "app.py"]