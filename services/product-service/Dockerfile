FROM python:3.9-slim

WORKDIR /app 

COPY requirements.txt ./ 
RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

# Make sure the images directory exists and is accessible
RUN mkdir -p /app/images
COPY images/* /app/images/

EXPOSE 5000

CMD ["python3" , "run.py"]
