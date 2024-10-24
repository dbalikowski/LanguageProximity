import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from deep_translator import GoogleTranslator  # Alternative to googletrans
import Levenshtein as lev
import time

# Initialize the Google Translator from deep-translator
def translate_word(word, target_lang, retries=3):
    for attempt in range(retries):
        try:
            translated = GoogleTranslator(source='en', target=target_lang).translate(word)
            if translated:
                return translated.lower()
        except Exception as e:
            print(f"Error translating {word} to {target_lang} (Attempt {attempt + 1}): {e}")
            time.sleep(2)  # Wait for 2 seconds before retrying
    return None

# Corrected list of languages (ISO language codes)
languages = ['en', 'fr', 'pl', 'it', 'de', 'es', 'pt', 'ro', 'cs', 'nl', 'da', 'no']  # 'cs' for Czech

# Extended dictionary of topics and words for analysis
words = {
    'fruit': ['pear', 'apple', 'grape', 'banana', 'orange'],
    'vegetables': ['carrot', 'potato', 'tomato', 'onion', 'cucumber'],
    'animals': ['dog', 'cat', 'horse', 'cow', 'lion'],
    'professions': ['doctor', 'teacher', 'engineer', 'artist', 'chef'],
    'numbers': ['one', 'two', 'three', 'four', 'five'],
    'countries': ['Poland', 'France', 'Germany', 'Italy', 'Spain'],
}

# Function to calculate Levenshtein distance
def calculate_similarity(word1, word2):
    if word1 and word2:  # Ensure both words are valid before calculating similarity
        return lev.distance(word1, word2)
    return None

# Function to calculate similarity between words across languages
def analyze_language_similarity(languages, words):
    data = []
    for topic, word_list in words.items():
        for word in word_list:
            translations = {lang: translate_word(word, lang) for lang in languages}
            similarities = {}
            
            # Calculate pairwise distances between translations
            for lang1, trans1 in translations.items():
                for lang2, trans2 in translations.items():
                    if lang1 != lang2 and trans1 and trans2:
                        sim_score = calculate_similarity(trans1, trans2)
                        if sim_score is not None:
                            similarities[(lang1, lang2)] = sim_score
                            data.append([topic, word, lang1, lang2, trans1, trans2, sim_score])

    return pd.DataFrame(data, columns=['Topic', 'Word', 'Language 1', 'Language 2', 'Translation 1', 'Translation 2', 'Similarity Score'])

# Function to save results to a CSV file
def save_results_to_file(df, filename='language_similarity_results.csv'):
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")

# Visualization using NetworkX and Matplotlib
def visualize_similarity_graph(df):
    G = nx.Graph()

    # Add nodes and weighted edges
    for _, row in df.iterrows():
        G.add_edge(row['Language 1'], row['Language 2'], weight=row['Similarity Score'])

    # Create layout for better visualization
    pos = nx.spring_layout(G)
    
    # Draw the graph with node labels, edge colors, and weighted edges
    plt.figure(figsize=(10, 8))
    weights = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, edge_color='gray', width=2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weights)
    
    # Show the graph
    plt.title('Language Similarity Based on Word Translations')
    plt.show()

# Function to compute and visualize statistics for each language pair
def analyze_statistics(df):
    # Group by language pairs and calculate average similarity scores
    grouped = df.groupby(['Language 1', 'Language 2'])['Similarity Score'].mean().reset_index()

    # Print a summary of the statistics
    print("\nAverage similarity scores by language pairs:")
    print(grouped)

# Main execution
if __name__ == "__main__":
    # Step 1: Analyze similarity across topics and words
    similarity_df = analyze_language_similarity(languages, words)
    
    # Step 2: Save results to a CSV file
    save_results_to_file(similarity_df)
    
    # Step 3: Visualize the language similarity graph
    visualize_similarity_graph(similarity_df)

    # Step 4: Analyze statistics and print results
    analyze_statistics(similarity_df)
