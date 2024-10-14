def soundex(word):
    # Krok 1: Zachowaj pierwszą literę
    first_letter = word[0].upper()
    
    # Krok 2: Mapa zamieniająca litery na cyfry według zasad Soundex
    soundex_mapping = {
        'B': '1', 'F': '1', 'P': '1', 'V': '1',
        'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
        'D': '3', 'T': '3',
        'L': '4',
        'M': '5', 'N': '5',
        'R': '6'
    }
    
    # Krok 3: Ignorowane litery
    vowels_and_ignored = set('AEIOUHWY')
    
    # Krok 4: Zamień litery na cyfry, zignoruj niepotrzebne litery
    soundex_code = first_letter
    previous_digit = None
    
    for char in word[1:].upper():
        if char in vowels_and_ignored:
            continue
        
        digit = soundex_mapping.get(char, '')
        
        # Nie dodawaj tej samej cyfry dwa razy pod rząd
        if digit != previous_digit:
            soundex_code += digit
            previous_digit = digit

    # Krok 5: Uzupełnij zerami lub skróć do czterech znaków
    soundex_code = soundex_code[:4].ljust(4, '0')
    
    return soundex_code

# Przykład dla dwóch słów
word1 = "Telephone"
word2 = "Telefono"

soundex_code1 = soundex(word1)
soundex_code2 = soundex(word2)

print(soundex_code1) 
print(soundex_code2) 