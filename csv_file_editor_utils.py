import os
import csv

def get_csv_filename():
    """Lässt den Benutzer einen Dateinamen für die CSV-Datei eingeben"""
    while True:
        filename = input("Gib den Dateinamen für die CSV-Datei ein (ohne .csv): ").strip()
        if filename:
            if filename.endswith('.csv'):
                filename = filename[:-4]
            full_filename = f"{filename}.csv"
            if os.path.exists(full_filename):
                print(f"Die Datei '{full_filename}' existiert bereits.")
                while True:
                    choice = input("Möchtest du sie überschreiben? (ja/nein/abbrechen): ").strip().lower()
                    if choice == "ja":
                        return full_filename
                    elif choice == "nein":
                        break
                    elif choice == "abbrechen":
                        print("Programm wird beendet.")
                        exit()
                    else:
                        print("Bitte gib 'ja', 'nein' oder 'abbrechen' ein.")
            else:
                return full_filename
        print("Bitte gib einen gültigen Dateinamen ein.")

def export_to_csv(columns, results, filename="test.csv"):
    """Exportiert die Abfrageergebnisse in eine CSV-Datei"""
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(results)
    print(f"Ergebnisse erfolgreich in '{filename}' gespeichert.") 