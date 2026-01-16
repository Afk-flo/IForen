import sqlite3
import logging
import os


def error_message_handler(message,log=True) -> None :
    """ Basic error function in order to avoid redundancy message management """
    if log:
        logging.critical("[-] Error - %s [-]", message)
    print(f"[-] Error - {message} [-]")


def folder_check(extract_folder) -> None:
    """ Check & Create extract folder """
    if not os.path.exists(extract_folder):
        logging.info("[*] Creation of the extract folder [*]")
        os.makedirs(extract_folder)


def create_connection(backup_path, db_file) -> sqlite3.Connection|None:
    """ Try to connect to the database in the provided backup """

    final_path = os.path.join(backup_path, db_file)
    try :
        if not os.path.exists(final_path):
            raise FileNotFoundError("File not found")
        
        #    conn = sqlite3.connect(final_path)
        if os.path.getsize(final_path) == 0:
            raise ValueError("Database file is empty")
            
        conn = sqlite3.connect(f"file:{final_path}?mode=ro", uri=True)
        logging.info("[*] Connected to database for %s [*]", final_path)
        return conn
    except Exception as e:
        error_message_handler(f"Could not connect to the database {final_path} : {e}")
        return None
