FROM python:3.6
MAINTAINER PEI-i1

RUN apt-get update && apt-get install -y \
    gcc \
    gfortran \
    libblas-dev \
    liblapack-dev \
    libhdf5-dev

COPY ./chat_processor ./chat_processor
COPY ./requirements.txt .
COPY ./frequency_words_models ./frequency_words_models

RUN pip install -r requirements.txt
RUN python -m deeppavlov install ner_ontonotes_bert_mult

CMD ["python", "chat_processor/app.py"]
