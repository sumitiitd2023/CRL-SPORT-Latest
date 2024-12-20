FROM python:3.6
WORKDIR /code
ADD . /code

#RUN pip3 install --upgrade pip3
RUN pip3 install -r requirement.txt
COPY . /code
CMD ["python", "main.py"]






