FROM python:3.7
ADD client.py /
ADD cifar.py /
RUN pip install numpy torch flwr 
RUN pip install git+https://github.com/remde/vision.git
CMD [ "python","-u","./client.py" ]
