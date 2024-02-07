# Use an official Python runtime as a parent image
FROM python:3.8.1

# Set the working directory to /app
WORKDIR /app

# Install Firefox and necessary dependencies
RUN apt-get update && \
    apt-get install -y firefox-esr && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install required Python packages
COPY requirements.txt requirements.txt
RUN pip install pip --upgrade && \
    pip install -r requirements.txt && \
    pip install webdriver_manager==3.4.2 
# Download and set up GeckoDriver
ENV GECKODRIVER_VERSION 0.30.0
#ENV GECKODRIVER_VERSION 0.34.0
RUN wget https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -xf geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin/ && \
    rm geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz

# Copy the current directory contents into the container at /app
COPY . .

RUN chmod +x /app/entrypoint.sh

RUN python /app/manage.py collectstatic

CMD ["/app/entrypoint.sh"]

