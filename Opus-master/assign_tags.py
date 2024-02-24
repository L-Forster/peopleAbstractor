import numpy as np
from transformers import pipeline
from init_db import Database


def assign_categories_attributes(sequence_to_classify, candidate_labels, prob_threshold, classifier):
    result = classifier(sequence_to_classify, candidate_labels, multi_label=True)
    high_values = []
    threshold = 0.9
    for i in range(len(result['labels'])-1):
        # try alternative thresholds based on the variance of the scores.

        if result['scores'][i] > threshold:
            high_values.append({"key": str(result['labels'][i]), "value": str(result['scores'][i])})
        else:
            break

    print(result)
    print(result['sequence'])
    print(high_values)
    return result['sequence'], high_values


def save_to_db(high_values, ttype, sentence_id):
# save the sentence

    db = Database()
    for val in high_values:
        if ttype == "tags":
            db.add_sentence_tag(sentence_id, (db.get_tag_id(val['key'])))
            db.set_parsed(sentence_id)
        elif ttype == "attributes":
            db.add_sentence_attribute(sentence_id, (db.get_attribute_id(val['key']))[0])
            db.set_parsed(sentence_id)
    db.close_connections()


def assign_sentences(person_id):

    db = Database()
    categories = db.get_all_tags()
    attributes = db.get_all_attributes()
    sentence_ids = db.get_unparsed_person_sentences(person_id)
    # db.add_person_without_data("Person1")
    # db.add_sentence("He scored 95/100 on the most recent exam without even studying", 1)
    sequences_to_classify = []
    for sentence_id in sentence_ids:
        sequences_to_classify.append(db.get_sentence(sentence_id))
    db.close_connections()

    classifier = pipeline('zero-shot-classification', model='roberta-large-mnli')

    for i in range(len(sequences_to_classify)):
        # Assign the category types:
        text, high_values = assign_categories_attributes(sequences_to_classify[i], categories, 0.08, classifier)
        save_to_db(high_values, "tags", sentence_ids[i])

        # Assign most relevant attributes:
        text, high_values = assign_categories_attributes(sequences_to_classify[i], attributes, 0.10, classifier)
        save_to_db(high_values, "attributes", sentence_ids[i])

# assign_sentences(1)
