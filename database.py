import os
from googletrans import Translator
from Levenshtein import distance as levenshtein_distance
from metaphone import doublemetaphone
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from PyDictionary import PyDictionary

class Database:
    def __init__(self):
        self.translator = Translator()
        self.target_languages = [
            "da", "de", "nl", "cs", "it", "es", "pt", "ro", "en", "no", "fr", "is"
        ]
        self.dictionary = PyDictionary()
    
    def get_synonyms(self, word):
        synonyms = self.dictionary.synonym(word)
        if synonyms is None:
            return []
        return synonyms.get('Noun', [])

    def translate_and_compare(self, word):
        translations = {}
        similarities = {}

        for lang in self.target_languages:
            try:
                translated = self.translator.translate(word, dest=lang).text
                if lang not in translations:
                    translations[lang] = []
                translations[lang].append(translated)
            except Exception as e:
                translations[lang] = []
                print(f"Error translating '{word}' to '{lang}': {e}")

        for lang, translated_words in translations.items():
            for translated_word in translated_words:
                if translated_word:
                    lev_similarity = self.levenshtein_similarity(word, translated_word)
                    meta_similarity = self.metaphone_similarity(word, translated_word)
                    cos_similarity = self.cosine_similarity(word, translated_word)

                    combined_score = 0.7 * lev_similarity + 0.3 * meta_similarity
                    similarities[translated_word] = (round(combined_score * 100, 2), lang)

        sorted_similarities = sorted(similarities.items(), key=lambda x: x[1][0], reverse=True)
        return sorted_similarities

    def levenshtein_similarity(self, word, translated_word):
        lev_dist = levenshtein_distance(word.lower(), translated_word.lower())
        max_len = max(len(word), len(translated_word))
        similarity = 1 - lev_dist / max_len
        return similarity

    def metaphone_similarity(self, word, translated_word):
        original_meta_primary, original_meta_secondary = doublemetaphone(word)
        trans_meta_primary, trans_meta_secondary = doublemetaphone(translated_word)
        
        meta_dist = levenshtein_distance(original_meta_primary, trans_meta_primary)
        max_len = max(len(original_meta_primary), len(trans_meta_primary))
        similarity = 1 - meta_dist / max_len
        return similarity

    def cosine_similarity(self, word, translated_word):
        vectorizer = CountVectorizer().fit_transform([word, translated_word])
        cosine_sim = cosine_similarity(vectorizer[0], vectorizer[1])
        return cosine_sim[0][0]