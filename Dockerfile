# Base Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /usr/src/app


COPY . .
RUN apt-get update && apt-get install -y wget unzip
RUN wget -O HighFinesseNetAccessAccessories.zip https://www.highfinesse-downloads.com/download/edcsc5ypvsua
RUN unzip HighFinesseNetAccessAccessories.zip
RUN dpkg -i HighFinesse\ NetAccess\ Accessories/Client_Linux/wlmData-7.264.2-x86_64.deb
RUN cp HighFinesse\ NetAccess\ Accessories/Example\ Python/DataDemo_Basic/wlmData.py ./artiq_highfinesse/
RUN cp HighFinesse\ NetAccess\ Accessories/Example\ Python/DataDemo_Basic/wlmConst.py ./artiq_highfinesse/


RUN pip install -r requirements.txt

ENV PYTHONPATH=/usr/src/app
ENV PYTHONUNBUFFERED=1

# Specify the default command to run the service
#CMD ["python", "artiq_highfinesse/aqctl_artiq_highfinesse.py", "--device_ip", "10.88.1.93"]
CMD ["python", "artiq_highfinesse/aqctl_artiq_highfinesse.py", "--simulation"]
#CMD ["pytest", "artiq_highfinesse/test_artiq_highfinesse.py"]
