import ujson as json
import spacy
import fastai
from pathlib import Path
from fastai.text import load_data, text_classifier_learner, AWD_LSTM
from typing import Tuple

bs=48
path=Path('/app/model/sentiment')
data_clas = load_data(path, 'data_clas.pkl', bs=bs)
learn = text_classifier_learner(data_clas, AWD_LSTM, drop_mult=0.5)
learn.load('third')
learn.model.eval()
nlp = spacy.load('en_core_web_md')

def message_to_sentences(message:str, minimum_characters:int=5) -> str:
    text = message
    sentences = []
    for line in text.split('\n'):
        sentences += line.split('.')
    return [s for s in sentences if len(s) > minimum_characters]

def predict_sentiment(sentence:str) -> Tuple[str, float]:
    categorical, class_id, scores = learn.predict(sentence)
    score = round(scores[class_id].item(), 4)
    return "negative" if class_id == 0 else "positive", score

def model(message):
    sentence = json.loads(message)
    doc = nlp(sentence)
    entities = nlp(sentence).ents
    if len(entities) == 0:
        return None

    ner = dict(
        sentence=sentence, 
        entities=[str(e) for e in entities]
    )

    cat, score = predict_sentiment(ner['sentence'])    

    output = [dict(
        entity=entity,
        sentiment=cat,
        score=score
    ) for entity in ner['entities']]

    return json.dumps(output)
