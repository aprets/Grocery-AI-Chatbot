FROM python:3.8

WORKDIR python-docker

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN python3 -m spacy download en_core_web_md

COPY . .

ENV FLASK_APP=server

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]