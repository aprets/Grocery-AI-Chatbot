FROM python:3.8

WORKDIR python-docker

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN python3 -m spacy download en_core_web_md

COPY . .

RUN python intent/make_model.py
RUN python intent/__init__.py
RUN python -m spacy train ner/model.cfg --training.max_epochs 15 --output ner/out
RUN rm -rf ner_model
RUN mv ner/out/model-best ner_model

ENV FLASK_APP=server

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]