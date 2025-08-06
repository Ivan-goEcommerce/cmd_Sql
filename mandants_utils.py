import pyodbc

def get_available_mandants(server, user, password):
    """Lädt alle verfügbaren Mandanten aus der master-Datenbank"""
    mandants = [] 
    try:
        conn = connect_to_database(server, "master", user, password)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sys.databases")
        for (name,) in cursor.fetchall():
            if name == "EasyBusiness" or name.startswith("Mandant_"):
                mandants.append(name)
        conn.close()
    except Exception as e:
        print(f"Fehler beim Laden der Mandanten: {e}")
    return mandants

def select_mandant(mandants):
    """Lässt den Benutzer einen Mandanten aus der Liste auswählen"""
    print("Verfügbare Mandanten:")
    for idx, name in enumerate(mandants, start=1):
        print(f"{idx}: {name}")
    while True:
        try:
            choice = int(input("Bitte wähle einen Mandanten: "))
            if 1 <= choice <= len(mandants): #controlle ob die eingaben richtig sind
                return mandants[choice - 1]
            else:
                print("Ungültige Auswahl.")
        except ValueError:
            print("Bitte eine Zahl eingeben.")

def connect_to_database(server, db_name, user, password):
    """Erstellt eine Verbindung zur angegebenen Datenbank"""
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={db_name};UID={user};PWD={password}'
    return pyodbc.connect(conn_str) 