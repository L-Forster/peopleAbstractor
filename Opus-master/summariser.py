from transformers import pipeline
import init_db


def summarise_person(person_id):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", revision="deb0f97cf6acb4f0a691356ed00ea06bf7e86e8f")
    # data is all the data from the person ID
    db = init_db.Database()
    name, sentences, categories_vals = db.get_person_all_data(person_id)
    data = str("Summarise the info about Name: " + name[0]) + ". Student at the University of Bristol in concise facts " + str(categories_vals)
    print(data)
    # format the data for summarizer input
    summary = summarizer(data, max_length=130, min_length=30, do_sample=False)
    print(summary[0]['summary_text'])

    db.add_summary(person_id, summary[0]['summary_text'])
    db.close_connections()


def summarise_person_categories(person_id):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", revision="deb0f97cf6acb4f0a691356ed00ea06bf7e86e8f")
    db = init_db.Database()
    for tag in db.categories:
        tag_id = db.get_tag_id(tag)
        sents = db.get_tag_sentences(tag_id, person_id)
        sents = "".join(sents)

        sex = db.get_person_sex(person_id)
        if sex[0] == "Male":
            sents = sents.replace("I ", "he ")
            sents = sents.replace("my", "his ")
            sents = sents.replace("My", "His ")
            sents = sents.replace("myself ", "himself ")
            sents = sents.replace("Myself ", "Himself ")
            sents = sents.replace("me ", "him ")
            sents = sents.replace("Me ", "Him ")
        elif sex[0] == "Female":
            sents = sents.replace("I ", "she ")
            sents = sents.replace("my ", "her ")
            sents = sents.replace("My ", "Her ")
            sents = sents.replace("Myself ", "Herself ")
            sents = sents.replace("myself ", "herself ")
            sents = sents.replace("Me ", "Her ")
            sents = sents.replace("me ", "her ")
        # convert sentences into third person
        # I -> He / She
        # My -> His / her
        # myself -> himself / herself
        # me -> him / her

        if len(sents) > 1000:
            sents = sents[:999]
        if len(sents) > 100:
            try:
                print(sents)
                sents = "Extract attributes about " + tag + " in the third person, shortly and concisely from the sentences: " + sents
                print(sents)
                summary = summarizer(sents, max_length=100, min_length=30, do_sample=False)
                print(summary)
                db.add_person_category(person_id, tag_id-1, summary)
            except TypeError:
                print("Type error")

    db.close_connections()


# summarise_person(1)
# summarise_person_categories(1)
# save summarised data to person summary
