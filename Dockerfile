# Base Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy application files into the container
#COPY . .
COPY requirements.txt .
COPY wlmData-7.264.2-x86_64.deb .

RUN dpkg -i wlmData-7.264.2-x86_64.deb
RUN pip install -r requirements.txt
# Install artiq_highfinesse module
# Mount the volume when running the container
# docker run -v $(pwd):/usr/src/app -it highfinesse
#RUN pip install .

ENV PYTHONPATH=/usr/src/app
ENV PYTHONUNBUFFERED=1

# Specify the default command to run the service
#CMD ["python", "artiq_highfinesse/aqctl_artiq_highfinesse.py", "--device_ip", "10.88.1.93"]
CMD ["python", "artiq_highfinesse/aqctl_artiq_highfinesse.py", "--simulation"]
#CMD ["pytest", "artiq_highfinesse/test_artiq_highfinesse.py"]
