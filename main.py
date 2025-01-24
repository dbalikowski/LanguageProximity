import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from database import Database
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pygame
import threading


canvas = None  # Dodaj tę linię, aby canvas była dostępna globalnie


# Inicjalizacja bazy danych
db = Database()

# Inicjalizacja Pygame i załadowanie dźwięku
pygame.mixer.init()
click_sound = pygame.mixer.Sound("assets/sound.mp3")

# Funkcja do odtwarzania dźwięku
def play_click_sound():
    click_sound.play()

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
    window.resizable(True, True)  # Zablokuj rozmiar okna aplikacji

def save_plot_to_png():
    if canvas is None:
        messagebox.showerror("Błąd", "Brak wykresu do zapisania.")
        return
    fig = canvas.figure
    try:
        fig.savefig("wykres.png", format="png")
        messagebox.showinfo("Sukces", "Wykres został zapisany jako wykres.png.")
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się zapisać wykresu: {str(e)}")


# Funkcja do ekranu ładowania
def show_loading_screen():
    root.withdraw()  # Ukryj główne okno na czas ładowania

    loading_screen = tk.Toplevel(root)
    loading_screen.overrideredirect(True)  # Usuń ramkę okna
    loading_screen.configure(bg="white")
    
    # Wyśrodkowanie ekranu ładowania
    loading_width, loading_height = 800, 600
    center_window(loading_screen, loading_width, loading_height)

    # Wczytaj obrazek intro
    intro_image = Image.open("assets/intro.jpg")
    intro_image = intro_image.resize((loading_width, loading_height), Image.LANCZOS)
    intro_photo = ImageTk.PhotoImage(intro_image)

    # Wyświetl obrazek
    intro_label = tk.Label(loading_screen, image=intro_photo, bg="white")
    intro_label.image = intro_photo
    intro_label.pack(expand=True, fill="both")

    # Efekt zanikania
    alpha = 1.0

    def fade_out():
        nonlocal alpha
        alpha -= 0.05
        if alpha <= 0:
            loading_screen.destroy()  # Zamknij ekran ładowania
            show_main_view()  # Otwórz główną aplikację
        else:
            loading_screen.attributes("-alpha", alpha)
            loading_screen.after(50, fade_out)

    loading_screen.after(1000, fade_out)  # Zacznij zanikanie po 1 sekundzie

# Słowniki tłumaczeń
translations = {
    "PL": {
        "language": "Język",
        "pl": "Polski",
        "en": "Angielski",
        "header": "Language Proximity",
        "word_prompt": "Wpisz słowo",
        "search_button": "Szukaj podobnych",
        "stats_button": "Pokaż Statystyki",
        "footer": "Autorzy: Artur Czarnecki, Dawid Balikowski, Piotr Graczyk, Sebastian Maciak, Patryk Muszyński",
        "similarity_results": "Wyniki podobieństwa",
        "similarity_results_header": "Wyniki podobieństwa",        
        "translation": "Tłumaczenie",
        "similarity": "Podobieństwo",
        "no_results": "Brak wyników dla podanego słowa.",
        "loading": "Szukam..."
    },
    "EN": {
        "language": "Language",
        "pl": "Polish",
        "en": "English",
        "header": "Language Proximity",
        "word_prompt": "Enter word",
        "search_button": "Search Similar",
        "stats_button": "Show Statistics",
        "footer": "Authors: Artur Czarnecki, Dawid Balikowski, Piotr Graczyk, Sebastian Maciak, Patryk Muszyński",
        "similarity_results": "Similarity Results",
        "similarity_results_header": "Similarity Results",        
        "translation": "Translation",
        "similarity": "Similarity",
        "no_results": "No results found for the entered word.",
        "loading": "Searching..."
    }
}

# Globalna zmienna do trzymania aktualnego języka
current_language = "EN"

# Funkcja do zmiany języka
def change_language(lang):
    global current_language
    current_language = lang
    update_texts()

# Funkcja do aktualizacji tekstów w zależności od wybranego języka
def update_texts():
    # Aktualizacja tekstów w GUI
    header_label.config(text=translations[current_language]["header"])
    search_button.config(text=translations[current_language]["search_button"])
    footer_label.config(text=translations[current_language]["footer"])
    
    # Etykieta paska narzędzi
    language_menu.entryconfig(0, label=translations[current_language]["pl"])
    language_menu.entryconfig(1, label=translations[current_language]["en"])
    
    # Etykieta "Wpisz słowo"
    word_prompt_label.config(text=translations[current_language]["word_prompt"])



# Funkcja do wyświetlania głównego widoku aplikacji
def show_main_view():
    root.deiconify()  # Pokaż główne okno
    center_window(root, 800, 950)  # Wyśrodkowanie głównego okna
    global canvas

    # Ramka nagłówka
    header_frame = tk.Frame(root)
    header_frame.pack(pady=10)

    # Dodanie logo
    logo_image = Image.open("assets/logo.png")
    logo_image = logo_image.resize((200, 200), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(header_frame, image=logo_photo)
    logo_label.image = logo_photo
    logo_label.pack(side="left", padx=(0, 10))

    # Nagłówek
    global header_label
    header_label = tk.Label(header_frame, text=translations[current_language]["header"], font=("Arial", 20))
    header_label.pack(side="left")

    # Ramka paska narzędzi
    toolbar_frame = tk.Frame(root)
    toolbar_frame.pack(fill="x", padx=10)

    # Menu w pasku narzędzi
    menu_bar = tk.Menu(root)
    global language_menu
    language_menu = tk.Menu(menu_bar, tearoff=0)
    language_menu.add_command(label=translations[current_language]["pl"], command=lambda: change_language("PL"))
    language_menu.add_command(label=translations[current_language]["en"], command=lambda: change_language("EN"))
    menu_bar.add_cascade(label=translations[current_language]["language"], menu=language_menu)

    root.config(menu=menu_bar)

    # Ramka wpisywania słowa i wyszukiwania
    entry_frame = tk.Frame(root)
    entry_frame.pack(pady=10)
    global word_prompt_label
    word_prompt_label = tk.Label(entry_frame, text=translations[current_language]["word_prompt"])
    word_prompt_label.grid(row=0, column=0, padx=5, pady=5)
    entry = tk.Entry(entry_frame, width=30)
    entry.grid(row=0, column=1, padx=5, pady=5)

    # Przyciski
    global search_button
    search_button = ttk.Button(entry_frame, text=translations[current_language]["search_button"], command=lambda: search_similar(entry, search_button))
    search_button.grid(row=1, column=0, columnspan=2, pady=10)

    # Ramka wyników
    global slide_frame
    slide_frame = tk.Frame(root)
    slide_frame.pack()

    # Dodanie podpisu autorów w lewym dolnym rogu
    footer_frame = tk.Frame(root)
    footer_frame.pack(side="bottom", fill="x", pady=(20, 10))
    global footer_label
    footer_label = tk.Label(footer_frame, text=translations[current_language]["footer"], font=("Arial", 10), anchor="w")
    footer_label.pack(side="left", padx=10)

        # Ramka paska narzędzi
    toolbar_frame = tk.Frame(root)
    toolbar_frame.pack(fill="x", padx=10)

    # Menu w pasku narzędzi
    menu_bar = tk.Menu(root)
    language_menu = tk.Menu(menu_bar, tearoff=0)
    language_menu.add_command(label=translations[current_language]["pl"], command=lambda: change_language("PL"))
    language_menu.add_command(label=translations[current_language]["en"], command=lambda: change_language("EN"))
    menu_bar.add_cascade(label=translations[current_language]["language"], menu=language_menu)

    root.config(menu=menu_bar)

    # Dodaj przycisk do zapisania wykresu
    save_button = ttk.Button(toolbar_frame, text="Zapisz wykres", command=save_plot_to_png)
    save_button.pack(side="right", padx=10)

def display_results(results):
    # Usuwamy poprzednie wyniki
    slide_frame.pack_forget()
    for widget in slide_frame.winfo_children():
        widget.destroy()

    # Wyświetlanie nagłówka wyników po wyszukaniu
    slide_label = tk.Label(slide_frame, text=translations[current_language]["similarity_results"], font=("Arial", 16))
    slide_label.pack(pady=10)

    # Wyświetlanie wyników podobieństwa
    high_similarity_results = [(translated_word, (score, lang)) for translated_word, (score, lang) in results if score >= 50]

    if high_similarity_results:
        for translated_word, (score, lang) in high_similarity_results:
            result_label = tk.Label(slide_frame, text=f"{translations[current_language]['translation']}: {translated_word} ({translations[current_language]['language']}: {lang}), {translations[current_language]['similarity']}: {score:.2f}%")
            result_label.pack()
    elif len(results) > 2:
        closest_results = results[:2]
        for translated_word, (score, lang) in closest_results:
            result_label = tk.Label(slide_frame, text=f"{translations[current_language]['translation']}: {translated_word} ({translations[current_language]['language']}: {lang}), {translations[current_language]['similarity']}: {score:.2f}%")
            result_label.pack()
    else:
        no_result_label = tk.Label(slide_frame, text=translations[current_language]["no_results"])
        no_result_label.pack()

    slide_frame.pack()  # Pokazujemy ramkę z wynikami

    # Generowanie wykresu po uzyskaniu wyników
    plot_statistics(results)



def search_similar(entry, button):
    word = entry.get()
    if not word:
        messagebox.showerror("Błąd", "Wpisz słowo do porównania.")
        return

    def run_search():
        # Usuwamy poprzednie wykresy, jeśli istnieją
        if canvas is not None:
            canvas.get_tk_widget().pack_forget()

        # Animacja ładowania
        button.config(text=translations[current_language]["search_button"] + "...")
        play_click_sound()
        results = db.translate_and_compare(word)
        display_results(results)
        button.config(text=translations[current_language]["search_button"])  # Przywrócenie napisu na przycisku

    threading.Thread(target=run_search).start()  # Uruchom w tle, by GUI się nie zawieszało


# Funkcja do wykreślenia statystyk na wykresie
def plot_statistics(results):
    play_click_sound()
    global canvas

    if not results:
        messagebox.showinfo("Brak wyników", "Nie ma wyników do wyświetlenia na wykresie.")
        return

    if canvas is not None:
        canvas.get_tk_widget().pack_forget()

    translated_words, similarities = zip(*[(tw, (s[0], s[1])) for tw, s in results])
    similarities = [s[0] for s in similarities]
    colors = [(1 - sim / 100, sim / 100, 0) for sim in similarities]

    sorted_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=False)
    sorted_translated_words = [translated_words[i] for i in sorted_indices]
    sorted_similarities = [similarities[i] for i in sorted_indices]
    sorted_colors = [colors[i] for i in sorted_indices]

    fig, ax = plt.subplots(figsize=(10, len(sorted_translated_words) * 0.5))
    ax.barh(sorted_translated_words, sorted_similarities, color=sorted_colors)
    ax.set_xlabel(translations[current_language]["similarity"] + " (%)")
    ax.set_title(translations[current_language]["similarity"] + " Comparison")

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both')


# Inicjalizacja głównego okna
root = tk.Tk()
root.title(translations[current_language]["header"])
root.iconbitmap("assets/logo.ico")

# Wyśrodkowanie okna na ekranie
center_window(root, 800, 600)

# Pokaż ekran ładowania na początku
show_loading_screen()

root.mainloop()
