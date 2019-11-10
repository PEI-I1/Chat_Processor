#!/usr/bin/env python3
from __future__ import unicode_literals, print_function

import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding

# training data
TRAIN_DATA = [
    # DATE datas
    # MOVIE nomes de filmes
    ("Quando dá o filme Joker?", {"entities": [(18, 23, "MOVIE")]}),
    ("Quero ver o filme Guerra dos Mundos amanhã.", {"entities": [(18, 24, "MOVIE"), (25, 28, "MOVIE"), (29, 35, "MOVIE"), (36, 42, "DATE")]}),
    ("Quero ver o filme Guerra dos Mundos amanhã.", {"entities": [(18, 35, "MOVIE"), (36, 42, "DATE")]}),
    ("Quando começa o filme A Herdade?", {"entities": [(22, 31, "MOVIE")]}),
    ("Qual a duração do filme Doutor Sono?", {"entities": [(24, 35, "MOVIE")]}),
    # LOC Local por coordenadas (latitude e longitude)
    ("Que filmes tens em Braga?", {"entities": [(19, 24, "LOC")]}),
    ("Que filmes tens no Porto?", {"entities": [(19, 24, "LOC")]}),
    # DURATION duração de algo
    ("Filmes com menos de 1h", {"entities": [(20, 22, "DURATION")]}),
    ("Filmes com menos de uma hora", {"entities": [(20, 28, "DURATION")]}),
    ("Filmes com mais de 1h", {"entities": [(19, 21, "DURATION")]}),
    ("Filmes com mais de uma hora", {"entities": [(19, 27, "DURATION")]}),
    ("Filmes com duração entre 1h e 2h", {"entities": [(25, 27, "DURATION"), (30, 32, "DURATION")]}),
    ("Filmes com duração entre uma hora e duas horas", {"entities": [(25, 33, "DURATION"), (36, 46, "DURATION")]}),
    ("Filmes com menos de 1 hora", {"entities": [(20, 26, "DURATION")]}),
    ("Filmes com menos de 1h30min", {"entities": [(20, 27, "DURATION")]}),
    ("Filmes com menos de 1:30min", {"entities": [(20, 27, "DURATION")]}),
    ("Filmes com menos de 1 hora e 30 minutos", {"entities": [(20, 39, "DURATION")]}),
    # GENRE genero do filme
    ("Quero ver filmes de terror", {"entities": [(20, 26, "GENRE")]}),
    ("Quero ver filmes de comédia", {"entities": [(20, 27, "GENRE")]}),
    ("Que filmes há de ação?", {"entities": [(17, 21, "GENRE")]}),
    ("Que filmes há de animação?", {"entities": [(17, 25, "GENRE")]}),
    # PER nomes, pessoas (atores, realizadores)
    ("Que filmes há com o Will Smith?", {"entities": [(20, 30, "PER")]}),
    ("Filmes com o Will Smith", {"entities": [(13, 23, "PER")]}),
    # AGERESTRIC restriçao de idade
    ("Que filmes há para crianças?", {"entities": [(19, 27, "AGERESTRIC")]}),
    ("Que filmes há para adultos?", {"entities": [(19, 26, "AGERESTRIC")]}),
    ("Que filmes há para 18+?", {"entities": [(19, 22, "AGERESTRIC")]}),
    ("Que filmes há para 18-?", {"entities": [(19, 22, "AGERESTRIC")]}),
    ("Que filmes há para mais de 18anos?", {"entities": [(27, 33, "AGERESTRIC")]}),
    ("Que filmes há para menos de 18anos?", {"entities": [(28, 34, "AGERESTRIC")]}),

    # MODEL modelo de telemovel
    ("Quero informações sobre o iPhone 8", {"entities": [(26, 34, "MODEL")]}),
    ("Quero informações sobre o iPhone 11", {"entities": [(26, 35, "MODEL")]}),
    ("Quero informações sobre o Asus Zenfone", {"entities": [(26, 38, "MODEL")]}),
    # BRAND marcas de telemovel
    ("Quero telemoveis da Apple", {"entities": [(20, 25, "BRAND")]}),
    ("Que telemoveis da Apple estão disponiveis?", {"entities": [(18, 23, "BRAND")]}),
    ("Telemoveis da Apple", {"entities": [(14, 19, "BRAND")]}),
    ("Quero telemoveis da Asus", {"entities": [(20, 24, "BRAND")]}),
    ("Quero telemoveis da Xiaomi", {"entities": [(20, 26, "BRAND")]}),
    # MONEY Valores monetários
    ("Telemoveis abaixo dos 100euros", {"entities": [(22, 30, "MONEY")]}),
    ("Telemoveis acima dos 100euros", {"entities": [(21, 29, "MONEY")]}),
    ("Telemoveis entre os 100euros e 200euros", {"entities": [(20, 28, "MONEY"), (31, 39, "MONEY")]}),
    ("Telemoveis abaixo dos 70euros", {"entities": [(22, 29, "MONEY")]}),
    ("Telemoveis abaixo dos 70euros e 50 centimos", {"entities": [(22, 43, "MONEY")]}),
    ("Telemoveis abaixo dos 70€", {"entities": [(22, 25, "MONEY")]}),
    ("Telemoveis abaixo dos 70,50€", {"entities": [(22, 28, "MONEY")]}),
    ("Tens algum telemovel abaixo dos 70€?", {"entities": [(28, 31, "MONEY")]}),
    # PACKAGE     Pacotes
    # SPEED       Velocidade da net
]

### entidades uteis ###
# Datas
## problemas tecnicos
## filmes
# MOVIE       Filmes
# LOC         Local por coordenadas (latitude e longitude)
# DURATION    Duração (tempo)
# GENRE       Géneros de filmes
# PER         Nomes de pessoas (atores, realizadores)
# AGERESTRIC  restriçao de idade
## assistencia
#       Assunto (linha apoio)
## telemoveis
# MODEL       Modelos de telemóveis
# BRAND       Marcas de telemóveis
# MONEY       Valores monetários
# PACKAGE     Pacotes
# SPEED       Velocidade da net
#       Tarifários
#       Locais (Lojas NOS)


@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int),
)
def main(model=None, output_dir=None, n_iter=100):
    """Load the model, set up the pipeline and train the entity recognizer."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("pt")  # create blank Language class
        print("Created blank 'en' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe("ner")

    # add labels
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):  # only train NER
        # reset and initialize the weights randomly – but only if we're
        # training a new model
        if model is None:
            nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    losses=losses,
                )
            print("Losses", losses)

    # test the trained model
    for text, _ in TRAIN_DATA:
        doc = nlp(text)
        print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
        print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        for text, _ in TRAIN_DATA:
            doc = nlp2(text)
            print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
            print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])


if __name__ == "__main__":
    plac.call(main)

    # Expected output:
    # Entities [('Shaka Khan', 'PERSON')]
    # Tokens [('Who', '', 2), ('is', '', 2), ('Shaka', 'PERSON', 3),
    # ('Khan', 'PERSON', 1), ('?', '', 2)]
    # Entities [('London', 'LOC'), ('Berlin', 'LOC')]
    # Tokens [('I', '', 2), ('like', '', 2), ('London', 'LOC', 3),
    # ('and', '', 2), ('Berlin', 'LOC', 3), ('.', '', 2)]
