FROM python:3.7
MAINTAINER PEI-i1

RUN apt-get update && apt-get install -y \
    gcc \
    gfortran \
    libblas-dev \
    liblapack-dev \
    libhdf5-dev \
    git

COPY . ./Chat_Processor
WORKDIR Chat_Processor

RUN pip install -r requirements.txt
RUN python -m deeppavlov install ner_ontonotes_bert_mult

CMD ["python", "chat_processor/app.py"]
