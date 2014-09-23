import unittest
import spotify

class TestPoemSentence(unittest.TestCase):

    def setUp(self):
        self.poem = spotify.PoemSentence("It's #Spotify\npoem!")

    def test_cleaned_sentence(self):
        expected = "It's Spotify poem"
        self.assertEquals(self.poem.sentence, expected)

    def test_words(self):
        expected = ["It's", "Spotify", "poem"]
        self.assertEquals(len(self.poem.words), 3)
        self.assertListEqual(self.poem.words, expected)

    def test_paritions(self):
        expected = [
            ["It's Spotify poem"],
            ["It's", 'Spotify poem'],
            ["It's Spotify", 'poem'],
            ["It's", 'Spotify', 'poem']]
        result = list(self.poem.partitions())
        self.assertListEqual(result, expected)

class TestPoemSentenceToPlaylist(unittest.TestCase):
    def setUp(self):
        self.api = spotify.SearchAPI()

    def test_empty(self):
        poem = spotify.PoemSentence('')
        result = poem.spotifize(self.api)
        self.assertEquals(len(result), 0)

    def test_poem_playlist(self):
        poem = spotify.PoemSentence('What is your name, Stranger.')
        expected = [('What is your name', u'spotify:track:0APF0zBtGLD0rtAtqeXyC2'),
                    ('Stranger',          u'spotify:track:1Ft6KgjMR7TSVkryV7gq8n')]
        result = poem.spotifize(self.api)
        self.assertEquals(len(result), 2)
        self.assertListEqual(result, expected)
        self.assertEquals(poem.coverage(), 1.0)

if __name__ == '__main__':
    unittest.main()