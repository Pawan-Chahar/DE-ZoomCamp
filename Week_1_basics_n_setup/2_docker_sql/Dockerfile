FROM python:3.9.1

#set the working directory 
WORKDIR /app   

#Copy files to the container
COPY  ingest_data.py  /app/ingest_data.py 
COPY requirments.txt  /app/requirments.txt


# Install system dependencies and distutils
RUN apt-get update && apt-get install -y \
    wget \
    && apt-get clean

# Install Python dependencies
RUN pip install --no-cache-dir -r requirments.txt


#Default Command
ENTRYPOINT [ "python","ingest_data.py" ]