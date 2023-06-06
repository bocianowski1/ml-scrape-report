FROM python:3.9

# Install Firefox and dependencies
RUN apt-get update && apt-get install -y firefox-esr

# Download and install geckodriver
RUN apt-get install -y wget && \
    wget -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz && \
    tar -xf /tmp/geckodriver.tar.gz -C /usr/local/bin/ && \
    rm /tmp/geckodriver.tar.gz

# Set the PATH environment variable to include geckodriver
ENV PATH="/usr/local/bin:${PATH}"

# Set the working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Run the application
CMD [ "python", "main.py" ]
