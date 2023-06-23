FROM phidata/jupyter:3.6.3

COPY requirements.txt /
RUN pip install -r /requirements.txt
