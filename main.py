import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from database import Database
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pygame  # Import biblioteki Pygame

# Inicjalizacja bazy danych
db = Database()

# Globalna zmienna do przechowywania wykresu
canvas = None

# Inicjalizacja Pygame i załadowanie dźwięku
pygame.mixer.init()
click_sound = pygame.mixer.Sound("assets\sound.mp3")  # Upewnij się, że podajesz poprawną ścieżkę do dźwięku

# Funkcja do odtwarzania dźwięku
def play_click_sound():
    click_sound.play()

# Funkcja do wyświetlania wyników
def display_results(results):

    slide_frame.pack_forget()
    
    # Wyczyść poprzednie wyniki w ramce
    for widget in slide_frame.winfo_children():
        widget.destroy()
    
    slide_label = tk.Label(slide_frame, text="Wyniki podobieństwa:", font=("Arial", 16))
    slide_label.pack(pady=10)

    # Filtracja wyników powyżej 50%
    high_similarity_results = [(translated_word, (score, lang)) for translated_word, (score, lang) in results if score >= 50]

    # Jeśli nie ma wyników powyżej 50%, pokazujemy dwa najbliższe wyniki
    if high_similarity_results:
        for translated_word, (score, lang) in high_similarity_results:
            result_label = tk.Label(slide_frame, text=f"Tłumaczenie: {translated_word} (Język: {lang}), Podobieństwo: {score:.2f}%")
            result_label.pack()
    elif len(results) > 2:
        closest_results = results[:2]  # Dwa najbliższe wyniki
        for translated_word, (score, lang) in closest_results:
            result_label = tk.Label(slide_frame, text=f"Tłumaczenie: {translated_word} (Język: {lang}), Podobieństwo: {score:.2f}%")
            result_label.pack()
    else:
        no_result_label = tk.Label(slide_frame, text="Brak wyników dla podanego słowa.")
        no_result_label.pack()

    slide_frame.pack()

# Funkcja do wyszukiwania podobnych słów
def search_similar():
    word = entry.get()
    if not word:
        messagebox.showerror("Błąd", "Wpisz słowo do porównania.")
        return

    # Odtwarzanie dźwięku
    play_click_sound()

    # Ukrywamy wykres przed nowym wyszukiwaniem
    if canvas is not None:
        canvas.get_tk_widget().pack_forget()

    # Uruchamiamy tłumaczenie i porównanie
    similarities = db.translate_and_compare(word)  # Usunięto próg
    display_results(similarities)

# Funkcja do wykreślenia statystyk na wykresie
def plot_statistics(results):
    play_click_sound()
    global canvas  # Używamy globalnej zmiennej, aby mieć dostęp do wykresu
    if not results:
        messagebox.showinfo("Brak wyników", "Nie ma wyników do wyświetlenia na wykresie.")
        return
    
    # Ukrywamy wykres przed narysowaniem nowego
    if canvas is not None:
        canvas.get_tk_widget().pack_forget()

    # Rozpakowywanie przetłumaczonych słów i ich podobieństw
    translated_words, similarities = zip(*[(tw, (s[0], s[1])) for tw, s in results])  # dodajemy język

    # Przygotowanie kolorów na podstawie podobieństwa
    similarities = [s[0] for s in similarities]  # tylko procenty
    colors = [(1 - sim/100, sim/100, 0) for sim in similarities]  # RGB - czerwony do zielonego

    # Tworzenie posortowanej listy na podstawie podobieństwa
    sorted_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=False)
    sorted_translated_words = [translated_words[i] for i in sorted_indices]
    sorted_similarities = [similarities[i] for i in sorted_indices]
    sorted_colors = [colors[i] for i in sorted_indices]

    fig, ax = plt.subplots(figsize=(10, len(sorted_translated_words) * 0.5))  # Zwiększamy rozmiar wykresu
    ax.barh(sorted_translated_words, sorted_similarities, color=sorted_colors)
    ax.set_xlabel("Podobieństwo (%)")
    ax.set_title("Porównanie podobieństwa słów")

    # Tworzymy nowy wykres w ramce
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both')

    # Ustalamy nową wysokość dla okna
    new_height = max(900, len(sorted_translated_words) * 30 + 200)  # Gwarantujemy minimalną wysokość
    root.geometry(f"600x{new_height}")  # Zmiana rozmiaru okna

# Główne okno aplikacji
root = tk.Tk()
root.title("Podobieństwo Słów")
root.geometry("800x600")  # Ustawia większy rozmiar początkowy

# Ustawienie ikony aplikacji
root.iconbitmap("assets/logo.ico")  

# Ramka nagłówka
header_frame = tk.Frame(root)
header_frame.pack(pady=10)

# Dodanie logo
logo_image = Image.open("assets\logo.png")  
logo_image = logo_image.resize((200, 200), Image.LANCZOS)  # Użycie LANCZOS do wysokiej jakości przeskalowania
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(header_frame, image=logo_photo)
logo_label.image = logo_photo  # Zachowujemy referencję, aby nie została zgarnięta przez GC
logo_label.pack(side="left", padx=(0, 10))  # Przesunięcie logo do lewej

# Nagłówek
header_label = tk.Label(header_frame, text="Language Proximity", font=("Arial", 20))
header_label.pack(side="left")  # Dodałem pakowanie na lewo bez marginesu

# Ramka wpisywania słowa i wyszukiwania
entry_frame = tk.Frame(root)
entry_frame.pack(pady=10)

tk.Label(entry_frame, text="Wpisz słowo:").grid(row=0, column=0, padx=5, pady=5)
entry = tk.Entry(entry_frame, width=30)
entry.grid(row=0, column=1, padx=5, pady=5)

search_button = tk.Button(entry_frame, text="Szukaj podobnych", command=search_similar)
search_button.grid(row=1, column=0, columnspan=2, pady=10)

# Ramka wyników
slide_frame = tk.Frame(root)
slide_frame.pack()

# Statystyki przycisk
stats_button = tk.Button(root, text="Pokaż Statystyki", command=lambda: plot_statistics(db.translate_and_compare(entry.get())))
stats_button.pack(pady=10)

root.mainloop()
