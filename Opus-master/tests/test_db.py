import unittest
import sqlite3
from init_db import Database
class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Initialize a Database object or perform setup actions before each test method
        self.db = Database()
        self.conn = sqlite3.connect('test_db.db')  # Use a temporary test database
        self.cursor = self.conn.cursor()

    def tearDown(self):
        # Close connections or perform cleanup actions after each test method
        self.db.close_connections()
        self.conn.close()

    def test_add_person(self):
        # Test adding a person and verify their existence in the database
        self.db.add_person("John Doe", "Attr1", "Profile1")
        user_ids = self.db.get_person_id("John Doe")
        self.assertTrue(len(user_ids) > 0)
        print("Test add_person Passes")

    def test_add_tag(self):
        self.db.add_tag("TestTag")
        try:
            tag_id = self.db.get_tag_id("TestTag")
            self.assertTrue(True)
        except sqlite3.Error:
            self.assertTrue(False)

    def test_sentence_values(self):
        self.db.add_person("Name", "", "")
        self.db.add_sentence("Test Sentence 1", 1)
        self.db.add_sentence("Test Sentence 2", 1)

        try:
            sentences_id = self.db.get_user_sentences(1)
            self.assertEqual(["Test Sentence 1","Test Sentence 2"], sentences_id)

        except sqlite3.Error:
            self.assertTrue(False)

    def test_add_sentence_with_tags(self):
        tags = ["tag1", "tag2", "tag3"]
        self.db.add_sentence_with_tags(tags, 1, "Test Sentence")
        sentence_tags = self.db.get_sentence_tags(3)
        self.assertEqual(len(tags), len(sentence_tags))

    def test_get_person_id(self):
        user_ids = self.db.get_person_id("NonExistentName")
        self.assertEqual(user_ids, [])

    def test_get_recent_person_id(self):
        self.db.add_person("Name","","")
        recent_id = self.db.get_recent_person_id()
        self.assertEqual(1, recent_id)

    def test_clear_all_tables(self):
        # Test clearing all tables and check if they are empty
        self.db.clear_all_tables()
        try:
            self.cursor.execute("SELECT * FROM people")
            people_data = self.cursor.fetchall()
            self.assertEqual(len(people_data), 0)

            self.cursor.execute("SELECT * FROM sentence_tags")
            sentence_tags_data = self.cursor.fetchall()
            self.assertEqual(len(sentence_tags_data), 0)

            self.cursor.execute("SELECT * FROM sentences")
            sentences_data = self.cursor.fetchall()
            self.assertEqual(len(sentences_data), 0)

            self.cursor.execute("SELECT * FROM tags")
            tags_data = self.cursor.fetchall()
            self.assertEqual(len(tags_data), 0)
        except sqlite3.Error:
            print("Test clear_all_tables Passes")


class TestExistingDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()
        self.conn = sqlite3.connect('DB NAME.db')  # Use a temporary test database
        self.cursor = self.conn.cursor()

    # Test all fields have a value

    def test_people_fields(self):
        pass

    def test_sentence_tags_fields(self):
        pass

    def test_sentence_fields(self):
        pass

    def test_tags_fields(self):
        pass


if __name__ == '__main__':
    unittest.main()


# Test the setters first.

# Then test the getters.