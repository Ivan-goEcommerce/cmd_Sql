import os

def list_sql_files():
    
    return [f for f in os.listdir() if f.endswith(".sql")]

def prompt_use_saved_query():
    
    files = list_sql_files()
    if not files:
        print("Keine gespeicherten Abfragen gefunden.")
        return None

    print("Gespeicherte Abfragen gefunden:")
    for idx, fname in enumerate(files, start=1):
        print(f"{idx}: {fname}")

    while True:
        choice = input("Möchtest du eine gespeicherte Abfrage verwenden? (j/n): ").strip().lower()
        if choice == "j":
            try:
                num = int(input("Nummer der Abfrage wählen: "))
                if 1 <= num <= len(files):
                    with open(files[num - 1], "r", encoding="utf-8") as f:
                        query = f.read()
                    print(f"Abfrage aus '{files[num - 1]}' geladen:")
                    print(query)
                    return query
                else:
                    print("Ungültige Nummer.")
            except ValueError:
                print("Bitte eine Zahl eingeben.")
        elif choice == "n":
            return None
        else:
            print("Bitte 'j' oder 'n' eingeben.")

def prompt_save_query(query):
    
    choice = input("Möchtest du diese Abfrage speichern? (j/n): ").strip().lower()
    if choice == "j":
        while True:
            filename = input("Dateiname für die Abfrage (ohne .sql): ").strip()
            if filename:
                full_name = f"{filename}.sql"
                if os.path.exists(full_name):
                    overwrite = input(f"Datei '{full_name}' existiert bereits. Überschreiben? (j/n): ").strip().lower()
                    if overwrite != "j":
                        continue
                with open(full_name, "w", encoding="utf-8") as f:
                    f.write(query)
                print(f"Abfrage in '{full_name}' gespeichert.")
                break
            else:
                print("Ungültiger Dateiname.") 