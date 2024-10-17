import os
from googletrans import Translator
from Levenshtein import distance as levenshtein_distance
from metaphone import doublemetaphone

def find_word_in_files(word, folder_path):
    found_category = None

    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if line.strip().lower() == word.lower():
                        found_category = filename[:-4]  # Usunięcie '.txt' z nazwy pliku
                        break
        if found_category:
            break

    return found_category

def translate_word(word):
    translator = Translator()
    languages = [
        'en', 'de', 'nl', 'cs', 'it', 'es', 'pt', 'ro', 
        'da', 'no', 'fr', 'is'
    ]
    translations = {}

    for lang in languages:
        translated = translator.translate(word, dest=lang)
        translations[lang] = translated.text

    return translations

def combine_levenshtein_metaphone(original_word, translations):
    original_meta_primary, original_meta_secondary = doublemetaphone(original_word)
    
    results = []
    
    for lang, translation in translations.items():
        trans_meta_primary, trans_meta_secondary = doublemetaphone(translation)
        
        # Obliczanie odległości Levenshteina między oryginalnym słowem a tłumaczeniem
        lev_dist = levenshtein_distance(original_word.lower(), translation.lower())
        
        # Sprawdzenie podobieństwa fonetycznego
        meta_dist = 0
        if original_meta_primary and trans_meta_primary:
            meta_dist = levenshtein_distance(original_meta_primary, trans_meta_primary)
        
        # Kombinowanie odległości Levenshteina z fonetyką, dodajemy wagę 0.7 dla Levenshteina i 0.3 dla fonetyki
        combined_score = 0.7 * lev_dist + 0.3 * meta_dist
        results.append((combined_score, translation, lang))
    
    # Sortowanie wyników według połączonego wyniku
    results.sort(key=lambda x: x[0])
    
    return results

def main():
    folder_path = 'set_of_topics'
    word = input("Podaj słowo do przeszukania: ")

    category = find_word_in_files(word, folder_path)
    
    if category:
        print(f'Znaleziono kategorię: {category}')
        translations = translate_word(word)

        # Sortowanie tłumaczeń według kombinacji Levenshteina i Metaphone
        sorted_translations = combine_levenshtein_metaphone(word, translations)

        print("Tłumaczenia (posortowane według połączonego podobieństwa Levenshteina i fonetycznego):")
        for score, translation, lang in sorted_translations:
            print(f'{lang}: {translation} (połączony wynik: {score})')
    else:
        print('Nie znaleziono słowa w żadnej kategorii.')

if __name__ == "__main__":
    main()
