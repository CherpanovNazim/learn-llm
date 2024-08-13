import warnings
from collections import defaultdict
from tempfile import NamedTemporaryFile

import spacy
import pandas as pd
from langchain.llms.openai import OpenAIChat


def get_ner_few_shot_examples_file(df, llm_task):
    data = list()
    for _, row in df.iterrows():
        if 'v1' in llm_task or 'v2' in llm_task:
            data.append({'text':  row.text, 'entities': row.labels})
        elif 'v3' in llm_task:
            spans = list()
            for entity_name, entity_values in row.labels.items():
                for entity_value in entity_values:
                    spans.append({"text": entity_value,
                                  "is_entity": True,
                                  "label": entity_name,
                                  "reason": f"is an {entity_name} entity"})
                    # you also can add some negatives by using
                    # "is_entity": False, "label": "==NONE=="
                data.append({'text':  row.text, 'spans': spans})
        else:
            raise ValueError('Unknown LLM task version')

    output_file = NamedTemporaryFile(suffix='.jsonl', delete=False)
    pd.DataFrame(data).to_json(output_file.name, orient='records', lines=True)

    return output_file.name


def span_to_dict(doc):
    predictions = defaultdict(list)
    for ent in doc.spans['sc']:
        predictions[ent.label_].append(ent.text)
    return dict(predictions)


def ner_to_dict(doc):
    predictions = defaultdict(list)
    for ent in doc.ents:
        predictions[ent.label_].append(ent.text)
    return dict(predictions)


class SpacyTask():
    def __init__(self, config: dict, use_chat_model=True):
        self.nlp = spacy.blank("en")
        self.config = config
        self.ner = self.nlp.add_pipe("llm", config=config)
        self.nlp.initialize()

        # monkey patch to use OpenAIChat instead of OpenAI (text-completion)
        if use_chat_model:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.ner._model._langchain_model = OpenAIChat(model_name=config['model']['name'],
                                                              **config['model']['config'])

    def predict(self, text, return_doc = False):
        doc = self.nlp(text)

        if return_doc:
            return doc
        
        task = self.config['task']['@llm_tasks']
        if 'SpanCat' in task:
            return span_to_dict(doc)
        elif 'NER' in task:
            return ner_to_dict(doc)
        else:
            raise NotImplementedError