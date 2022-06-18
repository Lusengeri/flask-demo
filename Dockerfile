FROM python:3.10

WORKDIR /flask-demo

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /flask-demo

EXPOSE 5000

#CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
