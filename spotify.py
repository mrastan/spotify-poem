import requests
import json
import itertools
import re

class SearchAPI(object):
    """ Simple search API for Spotify track metadata. """

    def __init__(self, base_url = 'http://ws.spotify.com/search/1/track.json'):
        self.base_url = base_url
        self._cache = {}
        self.is_same_track = lambda x, y: x.lower() == y.lower()
    
    def search(self, query, page=1):
        """ Queries Spotify API for track name and page number. Returns all
            matching tracks with accompanying metadata.
        """

        if not query: return []
        params = {'q': query, 'page': page}
        r = requests.get(self.base_url, params=params)
        r.raise_for_status()
        return r.json()
    
    def find_track(self, track_name, page_limit=1):
        """ Finds track_id with matching track_name. """

        if not track_name: return None
        tname = track_name.lower()

        if tname in self._cache:
            return self._cache.get(tname)

        for page in range(1, page_limit + 1):
            tracks = self.search(tname, page).get('tracks')
            if not tracks:
                break
            for track in tracks:
                if self.is_same_track(track.get('name'), tname):
                    track_id = self._cache[tname] = track.get('href')
                    return track_id

        self._cache[tname] = None
        return None

    def find_tracks(self, track_names, page_limit=1):
        """ Finds multiple tracks. Returns list of pairs (track_name, track_id). """

        results = []
        for track_name in track_names:
            results.append((track_name, self.find_track(track_name, page_limit)))
        return results

class PoemSentence:
    """ A poem sentence. """
    
    def __init__(self, sentence):
        self.sentence = re.sub(r'[.,?!]', '', sentence)
        self.words = self.sentence.split()
        self.best_result = []
        self.best_score = 0

    def __str__(self):
        return self.sentence

    def __coverage(self, result):
        """ Calculates word coverage (0.0 - 1.0) score for a result. Internal method. """
        
        words_all = len(self.words)
        words_with_track = 0

        for pair in result:
            phrase, track = pair
            if not track == None:
                words_with_track += len(phrase.split())
        
        return words_with_track/float(words_all)

    def coverage(self):
        """ Returns word coverage score (0.0 - 1.0) for the sentence. """
        
        return self.best_score

    def partitions(self):
        """ Generator of all possible partitions of the sentence. """
        
        ns = range(1, len(self.words)) 
        for n in ns: 
            for break_idxs in list(itertools.combinations(ns, n)):
                ranges = zip((0,) + break_idxs, break_idxs + (None,))
                yield [' '.join(self.words[i:j]) for i, j in ranges]
    
    def spotifize(self, api):
        """ Converts sentence to a list of Spolify tacks. """
        
        if not api or not isinstance(api, SearchAPI):
            raise ValueError('API instance is required to spotifize poem sentence.')

        for partition in self.partitions():
            result = api.find_tracks(partition)
            score = self.__coverage(result)

            if score > self.best_score:
                self.best_score = score
                self.best_result = result

            if score == 1.0:
                return self.best_result
        
        return self.best_result
