import os.path
import sqlite3


class Database():
    # Create tables for people, sentences, and tags
    def __init__(self):
        self.db_path = "PUT PATH HERE"
        # Connect to the database using the full path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.attributes = ['High logical intelligence', 'Low logical intelligence',  # Logical Intelligence
                           'High emotional intelligence', 'Emotionally Naive',  # Emotional intelligence
                           'Communicative', 'Reserved',  # Communication skills
                           'Emotionally resilient', 'Emotionally vulnerable',  # Mental Fortitude
                           'high creativity', 'low creativity',  # Creativity
                           'Initiative-taking', 'reluctant',  # willingness to act
                           'High motivation', 'Low motivation',  # motivation
                           'Compassionate', 'Inconsiderate',  # empathy
                           'Loyal', 'Untrustworthy',  # Honour / truthfulness
                           'high self-discipline', 'low self-discipline']  # Self-discipline

        self.categories = ["Social event", "Hobby", "Political opinion", "Personality trait",
                           "Wealth", "Education", "Date of birth", "Job",
                           "Birthplace", "Home", "Nationality", "Language", "Family",
                           "History", "Influencing others", "Philosophy", "Societies",
                           "Technical skill", "Trauma", "Award", "Strength", "Vulnerability", "Fear", "Love"]

        self.c10 = ["Logical Intelligence", "Emotional Intelligence", "Communication Skills",
                    "Mental Stability", "Creativity", "Willingness to Act", "Motivation", "Empathy",
                    "Honour", "Self-discipline"]

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS people
                          (id INTEGER PRIMARY KEY,
                          Name TEXT,
                          Sex TEXT,
                          Attributes TEXT,
                          Profiles TEXT,
                          Photo_id TEXT,
                          DOB DATE,
                          Birthplace TEXT,
                          Age INTEGER,
                          Summary TEXT)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sentences
                          (id INTEGER PRIMARY KEY,
                          Sentence TEXT,
                          Person_id INTEGER,
                          Parsed BOOL,
                          FOREIGN KEY (Person_id) REFERENCES people(id))''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS attributes
                          (id INTEGER PRIMARY KEY,
                          Attribute TEXT)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tags
                          (id INTEGER PRIMARY KEY,
                          Tag TEXT)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sentence_tags
                          (id INTEGER PRIMARY KEY,
                          Sentence_id INTEGER,
                          Tag_id INTEGER,
                          FOREIGN KEY (Sentence_id) REFERENCES sentences(id),
                          FOREIGN KEY (Tag_id) REFERENCES tags(id))''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sentence_attributes
                          (id INTEGER PRIMARY KEY,
                          Sentence_id INTEGER,
                          Attribute_id INTEGER,
                          FOREIGN KEY (Sentence_id) REFERENCES sentences(id),
                          FOREIGN KEY (Attribute_id) REFERENCES attributes(id))''')

        for attribute in self.c10:
            try:
                query = f"ALTER TABLE people ADD COLUMN '{attribute}' FLOAT;"
                self.cursor.execute(query)
            except sqlite3.OperationalError:
                pass

        for category in self.categories:
            try:
                query = f"ALTER TABLE people ADD COLUMN '{category}' TEXT;"
                self.cursor.execute(query)
            except sqlite3.OperationalError:
                pass

        self.conn.commit()

    def clear_table(self, table_name):
        try:
            self.cursor.execute(f"DELETE FROM {table_name}")
            self.conn.commit()
            print(f"Table '{table_name}' has been cleared.")
        except sqlite3.Error as e:
            print(f"Error occurred: {e}")

    def clear_all_tables(self):
        self.clear_table('people')
        self.clear_table('sentence_tags')
        self.clear_table('sentences')
        self.clear_table('tags')
        self.clear_table('attributes')
        self.clear_table('sentence_attributes')

        for tag in self.categories:
            self.add_tag(tag)
        for attr in self.attributes:
            self.add_attribute(attr)
        self.conn.commit()

    def add_person(self, name, attributes, profiles):
        self.cursor.execute("INSERT INTO people (Name, Attributes, Profiles) VALUES (?, ?, ?)",
                            (name, attributes, profiles))

        self.conn.commit()

    def add_person_without_data(self, name):
        self.cursor.execute("INSERT INTO people (Name, Attributes, Profiles) VALUES (?, ?, ?)", (name, None, None))
        self.conn.commit()

    def add_tag(self, tag):
        self.cursor.execute("INSERT INTO tags (Tag) VALUES (?)", (tag,))
        self.conn.commit()

    def add_attribute(self, attribute):
        self.cursor.execute("INSERT INTO attributes (Attribute) VALUES (?)", (attribute,))
        self.conn.commit()

    def add_sentence(self, sentence, person_id):
        sentence = sentence + " "
        self.cursor.execute("INSERT INTO sentences (Sentence, Parsed, Person_id) VALUES (?, ?, ?)",
                            (sentence, False, person_id))
        self.conn.commit()

    def add_sentence_tag(self, sentence_id, tag_id):
        self.cursor.execute("INSERT INTO sentence_tags (Sentence_id, Tag_id) VALUES (?, ?)", (sentence_id, tag_id))
        self.conn.commit()

    def add_sentence_attribute(self, sentence_id, attribute_id):
        self.cursor.execute("INSERT INTO sentence_attributes (Sentence_id, Attribute_id) VALUES (? ,?)",
                            (sentence_id, attribute_id))
        self.conn.commit()

    def add_sentence_with_tags(self, tags, person_id, sentence_text):
        self.cursor.execute("INSERT INTO sentences (Sentence, Parsed, Person_id) VALUES (?, ?, ?)",
                            (sentence_text, False, person_id))
        # Get the ID of the newly inserted sentence
        self.cursor.execute("SELECT last_insert_rowid()")
        sentence_id = self.cursor.fetchone()[0]
        # Add tags to the 'sentence_tags' table for the newly inserted sentence
        for tag in tags:
            self.add_tag(tag)
            tag_id = self.get_tag_id(tag)
            self.add_sentence_tag(sentence_id, tag_id)
        self.conn.commit()

    def add_sentence_with_attributes(self, attributes, person_id, sentence_text):
        self.cursor.execute("INSERT INTO sentences (Sentence, Person_id) VALUES (?, ?)", (sentence_text, person_id))
        # Get the ID of the newly inserted sentence
        self.cursor.execute("SELECT last_insert_rowid()")
        sentence_id = self.cursor.fetchone()[0]
        # Add tags to the 'sentence_tags' table for the newly inserted sentence
        for attribute in attributes:
            self.add_attribute(attributes)
            attribute_id = self.get_attribute_id(attribute)
            self.add_sentence_tag(sentence_id, attribute_id)

        self.conn.commit()

    def add_person_attribute(self, person_id, attribute_id, val):
        # convert the attribute id into c10 value
        attribute = self.c10[(attribute_id - 1) // 2]
        q = f"UPDATE people SET '{attribute}' = ? WHERE id = ?"
        self.cursor.execute(q, (val, person_id))
        self.conn.commit()

    def add_person_category(self, person_id, category_id, val):
        cat = self.categories[category_id]
        q = f"UPDATE people SET '{cat}' = ? WHERE id = ?"
        self.cursor.execute(q, (val[0]['summary_text'], person_id))
        self.conn.commit()

    def add_person_profile(self, person_id, profile):
        self.cursor.execute("UPDATE people SET profile = ? WHERE id = ?", (profile, person_id))
        self.conn.commit()

    def add_summary(self, person_id, summary):
        self.cursor.execute("UPDATE people SET summary = ? WHERE id = ?", (summary, person_id))
        self.conn.commit()

    def set_parsed(self, sentence_id):
        self.cursor.execute("UPDATE sentences SET Parsed = ? WHERE id = ?", (True, sentence_id))
        self.conn.commit()

    def get_all_tags(self):
        self.cursor.execute("SELECT Tag FROM tags")
        tags = self.cursor.fetchall()
        return [tag[0] for tag in tags]

    def get_all_attributes(self):
        self.cursor.execute("SELECT Attribute FROM attributes")
        attrs = self.cursor.fetchall()
        return [attr[0] for attr in attrs]

    def get_sentence_tags(self, sentence_id):
        self.cursor.execute(
            "SELECT tags.Tag FROM tags INNER JOIN sentence_tags ON tags.id = sentence_tags.Tag_id WHERE sentence_tags.Sentence_id = ?",
            (sentence_id,))
        tags = self.cursor.fetchall()
        return [tag[0] for tag in tags]

    def get_unparsed_sentences(self):
        self.cursor.execute(
            "SELECT id From sentences WHERE Parsed = FALSE"
        )
        sentences = self.cursor.fetchall()
        return [sentence[0] for sentence in sentences]

    def get_unparsed_person_sentences(self, person_id):
        self.cursor.execute(
            "SELECT id From sentences WHERE Parsed = FALSE and Person_id = person_id"
        )
        sentences = self.cursor.fetchall()
        return [sentence[0] for sentence in sentences]

    def get_person_sex(self, person_id):
        self.cursor.execute(
            "SELECT Sex From people WHERE id = ?", (person_id,)
        )
        return self.cursor.fetchone()

    def get_sentence(self, sentence_id):
        self.cursor.execute(
            "SELECT Sentence From sentences WHERE id = ?", (sentence_id,)
        )
        return self.cursor.fetchone()

    def get_tag_id(self, tag):
        try:
            return self.cursor.execute("SELECT tags.id FROM tags WHERE tags.Tag = ?", (tag,)).fetchone()[0]
        except sqlite3.Error as e:
            print(f"Error occurred: {e}")

    def get_attribute_id(self, attribute):
        try:
            return self.cursor.execute("SELECT attributes.id FROM attributes WHERE attributes.Attribute = ?",
                                       (attribute,)).fetchone()
        except sqlite3.Error as e:
            print(f"Error occurred: {e}")

    def get_person_sentences(self, person_id):
        self.cursor.execute("SELECT Sentence FROM sentences WHERE Person_id = ?", (person_id,))
        sentences = self.cursor.fetchall()
        return [sentence[0] for sentence in sentences]

    def get_tag_sentences(self, tag_id, person_id):
        self.cursor.execute(
            "SELECT sentences.Sentence FROM sentences INNER JOIN sentence_tags ON sentences.id = sentence_tags.Sentence_id WHERE sentence_tags.Tag_id = ? and sentences.Person_id = ?",
            (tag_id, person_id))
        sentences = self.cursor.fetchall()
        return [sentence[0] for sentence in sentences]

    def get_tag(self, tag_id):
        self.cursor.execute("SELECT Tag FROM tags WHERE id = ?", (tag_id,))
        return self.cursor.fetchone()

    def get_attribute_sentences(self, attribute_id, person_id):
        self.cursor.execute(
            "SELECT sentences.Sentence FROM sentences INNER JOIN sentence_attributes ON sentences.id = sentence_attributes.Sentence_id WHERE sentence_attributes.Attribute_id = ?  and sentences.Person_id = ?",
            (attribute_id, person_id))
        sentences = self.cursor.fetchall()
        return [sentence[0] for sentence in sentences]

    def get_recent_person_id(self):
        return self.cursor.execute("SELECT last_insert_rowid() FROM people").fetchone()[0]

    def get_recent_sentence_id(self):
        return self.cursor.execute("SELECT last_insert_rowid() FROM sentences").fetchone()[0]

    def get_recent_sentences_id(self, person_id):
        sents = self.cursor.execute("SELECT last_insert_rowid() FROM sentences WHERE Person_id = ?",
                                    (person_id,)).fetchmany(10)
        return [sent[0] for sent in sents] if sents else []

    def get_person_id(self, name):
        try:
            self.cursor.execute("SELECT id FROM people WHERE Name = ?", (name,))
            user_ids = self.cursor.fetchall()
            return [user_id[0] for user_id in user_ids] if user_ids else []
        except sqlite3.Error as e:
            print(f"Error occurred: {e}")
            return []

    def get_all_names(self):
        names = self.cursor.execute("SELECT Name FROM people").fetchall()
        return [name[0] for name in names]

    def get_person_column(self, column, person_id):
        q = "SELECT [{}] FROM people WHERE id = ?".format(column)
        self.cursor.execute(q, (person_id,))
        return self.cursor.fetchone()[0]

    def get_person_name(self, person_id):
        try:
            self.cursor.execute("SELECT Name FROM people WHERE Id = ?", (person_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error occurred: {e}")
            return -1

    def get_person_attributes(self, person_id):
        vals = []
        for attribute in self.c10:
            try:
                q = f"SELECT \"{attribute}\" FROM people WHERE id = ?"
                self.cursor.execute(q, (person_id,))
                vals.append({"attribute": attribute, "value": self.cursor.fetchone()[0]})
            except TypeError as e:
                print(f"Error occurred: {e}")
        return vals

    def get_person_categories(self, person_id):
        vals = []
        for category in self.categories:
            try:
                q = "SELECT [{}] FROM people WHERE id = ?".format(category)
                self.cursor.execute(q, (person_id,))
                vals.append({"category": category, "data": self.cursor.fetchone()[0]})
            except sqlite3.Error as e:
                print(f"Error occurred: {e}")
        return vals

    # Gets all the data from a specific person:
    # All their attributes' values and sentences and name.
    def get_person_all_data(self, person_id):
        sentences = self.get_person_sentences(person_id)
        name = self.get_person_name(person_id)
        categories_values = self.get_person_categories(person_id)

        return name, sentences, categories_values

    def close_connections(self):
        try:
            self.conn.commit()
            self.conn.close()
        except sqlite3.ProgrammingError:
            print("Database is already closed! ")


def create_entries_interface():
    db = Database()
    print(db.get_all_names())
    db.clear_all_tables()
    # print(db.get_person_id("Louis"))
    # print(db.get_user_sentences(db.get_person_id("Louis")[0]))
    # Collect user inputs
    # person_name = input("Enter person's name: ")
    # sentence_text = input("Enter the sentence: ")

    # tags_input = input("Enter tags (separated by commas): ")
    # # tags = [tag.strip() for tag in tags_input.split(",")]
    # #
    # # # Add the person to the 'people' table
    # db.add_person_without_data(person_name)  # Assuming Attributes and Profiles are empty for simplicity
    # person_id = db.get_recent_person_id()
    # # Add the sentence to the 'sentences' table
    # # db.add_sentence_with_tags(tags, person_id, sentence_text)  # Assuming person_id is 1 for the newly added person
    # db.add_sentence(sentence_text, person_id)
    db.close_connections()
    print("Entries created successfully!")

# Call the function to execute the interface
# create_entries_interface()
