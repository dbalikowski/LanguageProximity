from googletrans import Translator
import Levenshtein

class Database:
    def __init__(self):
        self.translator = Translator()
        self.target_languages = [
            "en", "de", "nl", "cs", "it", "es", "pt", "ro", "da", "no", "fr", "is"
        ]

    # Funkcja do tłumaczenia polskiego słowa na wybrane języki
    def translate_and_compare(self, word):
        translations = {}
        similarities = {}

        # Tłumaczenie słowa na różne języki
        for lang in self.target_languages:
            try:
                translated = self.translator.translate(word, dest=lang).text
                translations[lang] = translated
            except Exception as e:
                translations[lang] = None
                print(f"Error translating '{word}' to '{lang}': {e}")

        # Obliczanie podobieństwa dla każdego tłumaczenia
        for lang, translated_word in translations.items():
            if translated_word:
                # Użycie funkcji Levenshtein do porównania
                similarity = Levenshtein.ratio(word, translated_word)  # Porównanie za pomocą Levenshtein
                similarities[translated_word] = (round(similarity * 100, 2), lang)  # Procentowe podobieństwo i język

        # Sortowanie wyników od najbardziej podobnych do najmniej podobnych
        sorted_similarities = sorted(similarities.items(), key=lambda x: x[1][0], reverse=True)

        return sorted_similarities
