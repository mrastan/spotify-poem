import requests
import json
import itertools
import re

# TODO 
# check UTF
# add testing 
# is_same_track can be replaced by similarity function

class SearchAPI(object):
    """ Simple search API for Spotify track metadata. """

    def __init__(self, base_url = 'http://ws.spotify.com/search/1/track.json'):
        self.base_url = base_url
    
    def search(self, query, page=1):
        """ Queries API for track name and page number. Returns all 
            matching tracks with accompanying metadata. 
            """
        params = {'q': query, 'page': page}
        r = requests.get(self.base_url, params=params)
        r.raise_for_status()
        return r.json()
    
    def search_track(self, track_name, page_limit=1):
        """ Finds track url that exactly matches the track name. """        
        tname = track_name.lower()
        is_same_track = lambda x: x.lower() == tname
        tracks = self.search(tname).get('tracks')
        for track in tracks:
            if is_same_track(track.get('name')):
                track_href = track.get('href')
                return track_href
        return None

    def search_tracks(self, track_names):
        """ Finds multiple Spotify tracks. """
        results = []
        for track_name in track_names:
            results.append((track_name, self.search_track(track_name)))
        return results

class PoemSentence:
    """Poem sentence that is going to be spotifized."""
    
    def __init__(self, sentence):
        self.sentence = re.sub(r'[.,?!]', '', sentence)
        self.words = self.sentence.split()

    def __str__(self):
        return self.sentence

    def __coverage(self, result):
        words_all = len(self.words)
        words_with_track = 0

        for pair in result:
            phrase, track = pair
            if not track == None:
                words_with_track += len(phrase.split())
        
        return words_with_track/float(words_all)

    def partitions(self):
        """Generator of all possible partitions of certain poem sentence."""
        ns = range(1, len(self.words)) 
        for n in ns: 
            for idxs in itertools.combinations(ns, n):
                yield [' '.join(self.words[i:j]) for i, j in zip((0,) + idxs, idxs + (None,))]
    
    def spotifize(self, api):
        """Converts a sentence to a list of Spolify tacks"""
        if not api or not isinstance(api, SearchAPI):
            raise ValueError('API object required to spotifize sentence.')

        self.best_result = []
        self.best_score = 0
        for partition in self.partitions():
            result = api.search_tracks(partition)
            score = self.__coverage(result)

            if score > self.best_score:
                self.best_score = score
                self.best_result = result

            if score == 1.0:
                return self.best_result
        
        return self.best_result

class Poem:
    def __init__(self, poem):
        self.sentences = re.split(r'[,.?!\n]\s*', poem)
        
    def spotifize(self, api):
        if not api or not isinstance(api, SearchAPI):
            raise ValueError('API object required to spotifize poem.')

        result = map(lambda s: PoemSentence(s).spotifize(api), self.sentences)
        return result
