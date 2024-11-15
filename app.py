import openai

# Ustaw swój klucz API OpenAI
openai.api_key = 'xxx'

# Sprawdzenie, czy klucz jest prawidłowy
if openai.api_key:
    print("Klucz API załadowany.")
else:
    print("Brak klucza API. Upewnij się, że wprowadziłeś poprawny klucz.")

# Funkcja do odczytania zawartości pliku artykułu
def read_article(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            article_text = file.read()
            print("Plik został pomyślnie załadowany.")
            print("Pierwsze 200 znaków artykułu:", article_text[:200])  # Wyświetl pierwsze 200 znaków artykułu
            return article_text
    except FileNotFoundError:
        print(f"Plik {file_path} nie został znaleziony.")
        return ''
    except Exception as e:
        print(f"Błąd podczas odczytu pliku: {e}")
        return ''

# Funkcja do wysłania żądania do API OpenAI i przetworzenia artykułu
def process_article_with_openai(article_text):
    if not article_text:
        print("Tekst artykułu jest pusty. Nie można przetworzyć.")
        return ''

    print("Wysyłanie artykułu do OpenAI...")
    try:
        prompt = (
            "Przekształć poniższy tekst artykułu do formatu HTML. "
            "Użyj odpowiednich tagów HTML do strukturyzacji treści, "
            "a także wskaż miejsca na obrazy, używając tagu <img> z atrybutem src=\"image_placeholder.jpg\" "
            "oraz alt z opisem obrazu. Dodaj podpisy pod obrazkami. Nie używaj CSS ani JavaScript. "
            "Zwróć tylko zawartość do wstawienia między tagi <body> i </body>.\n\n"
            "Artykuł:\n" + article_text
        )

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Możesz także użyć modelu "gpt-4" jeśli masz dostęp
            messages=[
                {"role": "system", "content": "Przekształc tekst artykułu do HTML."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        print("Odpowiedź z API OpenAI została odebrana.")
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Błąd podczas komunikacji z API OpenAI: {e}")
        return ''

# Funkcja do zapisania wygenerowanego kodu HTML do pliku
def save_html_to_file(html_content, file_path):
    if not html_content:
        print("Brak zawartości HTML do zapisania.")
        return

    print("Zapisywanie kodu HTML do pliku...")
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
        print(f"Plik został zapisany jako {file_path}.")
    except Exception as e:
        print(f"Błąd podczas zapisywania pliku: {e}")

def main():
    print("Rozpoczynanie procesu...")
    # 1. Odczytaj artykuł z pliku
    article_text = read_article('artykul.txt')
    
    # 2. Przetwórz artykuł przy użyciu OpenAI
    html_content = process_article_with_openai(article_text)
    
    # 3. Zapisz wygenerowany kod HTML do pliku
    save_html_to_file(html_content, 'artykul.html')

    print("Proces zakończony.")

# Uruchomienie programu
if __name__ == "__main__":
    main()