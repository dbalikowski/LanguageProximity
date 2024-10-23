import Levenshtein

def areSimilar(word1, word2, threshold=0.7):
    """
    Compares two words for lexical similarity.

    Parameters:
    - word1, word2: words to compare
    - threshold: similarity threshold (from 0 to 1), above which words are considered similar

    Returns:
    - True if the similarity exceeds the threshold, False otherwise
    """
    distance = Levenshtein.ratio(word1, word2)
    return distance >= threshold

