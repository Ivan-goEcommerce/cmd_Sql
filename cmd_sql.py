import os
import pyodbc
import csv
import keyring
from pathlib import Path
from tabulate import tabulate
from sql_file_utils import list_sql_files, prompt_use_saved_query, prompt_save_query
from mandants_utils import get_available_mandants, select_mandant, connect_to_database
from csv_file_editor_utils import get_csv_filename, export_to_csv

SERVICE_NAME = "MSSQL_Connection" # Name des keyrings

def prompt_user_credentials(): #verbindungsdaten eingeben
    print("Gib die Verbindungsdaten für MSSQL ein:")
    server = input("Servername: ")
    user = input("Benutzername: ")
    password = input("Passwort: ")
    return server, user, password


def save_credentials_to_keyring(server, user, password): #verbindungsdaten in keyring speichern
    keyring.set_password(SERVICE_NAME, "server", server)
    keyring.set_password(SERVICE_NAME, "user", user)
    keyring.set_password(SERVICE_NAME, "password", password)


def load_credentials_from_keyring(): #verbindungsdaten aus keyring laden
    try:
        server = keyring.get_password(SERVICE_NAME, "server")
        user = keyring.get_password(SERVICE_NAME, "user")
        password = keyring.get_password(SERVICE_NAME, "password")
        if None in (server, user, password):
            return None, None, None
        print("Zugangsdaten erfolgreich aus dem Keyring geladen.")
        return server, user, password
    except Exception as e:
        print(f"Fehler beim Abrufen der Credentials aus dem Keyring: {e}")
        return None, None, None


def test_connection(server, db_name, user, password): #teste verbindung
    try:
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={db_name};UID={user};PWD={password}'
        with pyodbc.connect(conn_str, timeout=5):
            return True
    except pyodbc.Error as e:
        print(f"Verbindungsfehler: {e}")
        return False

def get_user_query():
    print("Gib deine SQL-Abfrage ein:")
    return input("SQL> ")


def get_output_option():
    print("Wähle das Ausgabeformat:")
    print("1: Ausgabe in der Konsole")
    print("2: In CSV-Datei speichern")
    while True:
        choice = input("Auswahl (1/2): ")
        if choice in ["1", "2"]:
            return int(choice)
        print("Ungültige Eingabe. Bitte 1 oder 2 eingeben.")


def execute_query(cursor, query):
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    results = cursor.fetchall()
    return columns, results


def print_results(columns, results):
    print(tabulate(results, headers=columns, tablefmt="grid"))

def main():
    credentials_valid = False
    server, user, password = load_credentials_from_keyring()

    if server and user and password:
        print("Versuche, Verbindung mit gespeicherten Zugangsdaten herzustellen...")
        credentials_valid = test_connection(server, "master", user, password)

    if not credentials_valid:
        while True:
            server, user, password = prompt_user_credentials()
            if test_connection(server, "master", user, password):
                save_credentials_to_keyring(server, user, password)
                break
            else:
                retry = input("Verbindung fehlgeschlagen. Erneut versuchen? (j/n): ").strip().lower()
                if retry != "j":
                    print("Programm wird beendet.")
                    return

    mandants = get_available_mandants(server, user, password)
    if not mandants:
        print("Keine Mandanten gefunden.")
        return

    db_name = select_mandant(mandants)

    try:
        conn = connect_to_database(server, db_name, user, password)
        cursor = conn.cursor()
        query = prompt_use_saved_query()
        if not query:
            query = get_user_query()
        output_option = get_output_option()
        columns, results = execute_query(cursor, query)
        prompt_save_query(query)

        if output_option == 1:
            print_results(columns, results)
        else:
            filename = get_csv_filename()
            export_to_csv(columns, results, filename)

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
    finally:
        try:
            conn.close()
        except:
            pass


if __name__ == "__main__":
    main()
