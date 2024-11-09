import sqlite3
import logging
import os


def error_message_handler(message,log=True) -> None :
    """ Basic error function in order to avoid redundancy message management """
    if log:
        logging.critical("[-] Error - %s [-]", message)
    print("[-] Error - %s [-]", message)


def folder_check(extract_folder) -> None:
    """ Check & Create extract folder """
    if not os.path.exists(extract_folder):
        logging.info("[*] Creation of the extract folder [*]")
        os.makedirs(extract_folder)


def create_connection(backup_path, db_file) -> sqlite3.Connection|None:
    """ Try to connect to the database in the provided backup """

    final_path = backup_path + db_file
    try :
        conn = sqlite3.connect(final_path)
        logging.info("[*] Connected to database for %s [*]", final_path)
        return conn
    except :
        error_message_handler("Could not connect to the database %s", final_path)
        return None

