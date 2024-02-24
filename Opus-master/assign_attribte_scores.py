# takes the data for each attribute (positive and negative) and evaluates how much they fit into each category
from init_db import Database
from transformers import pipeline


def parse_person(p_id):
    classifier = pipeline('zero-shot-classification', model='roberta-large-mnli')
    db = Database()
    attr_vals = db.get_person_attributes(p_id)
    print(attr_vals)
    # Get sentences with the given tag, from a person
    sequence = " "
    for attr in db.attributes:
        attr_id = db.get_attribute_id(attr)[0]
        sents_by_tag_person = db.get_attribute_sentences(attr_id, p_id)
        if (attr_id - 1) % 2 == 1:
            sequence = sequence + sequence.join(sents_by_tag_person)
            try:
                result = classifier(sequence, attr)
                print(result)
                db.add_person_attribute(p_id, attr_id, round(10 - result['scores'][0]*10, 2))
            except ValueError:
                print("No data for ", attr)
        else:
            sequence = " ".join(sents_by_tag_person)


    db.close_connections()

