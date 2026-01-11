import logging
import os
import sys

from utils.utils import create_connection, folder_check

PATH = "HomeDomain/Library/Notes/notes.sqlite"
# QUERY ZTITLE, ZTEXT from ZNOTE

class Notes:
    def __init__(self, backup_path, log, result, extract_folder):
        self.log = log
        self.result = result
        self.backup_path = backup_path
        self.extract_folder = extract_folder

    def extracts(self):
        """ Notes extraction and save"""
        print("[*] Extracting Notes... [*]")

        conn = create_connection(backup_path=self.backup_path, db_file=PATH)
        if conn is None:
            print("[-] Couldn't fetch Notes [-]")
            sys.exit(1)

        cursor = conn.cursor()
        query = """
        SELECT
            ZTITLE, ZTEXT
        FROM 
            ZNOTE;
        """

        cursor.execute(query)
        notes = cursor.fetchall()

        print("[+] %d Notes found ! ", len(notes))

        # Saving contacts
        folder_check(self.extract_folder)
        dest_file = os.path.join(self.extract_folder, "notes.txt")
        with open(dest_file, "w+") as f:
            for note in notes:
                ztitle, ztext = note
                f.write(f"> {ztitle} : {ztext} \n")

        conn.close()
        print("[+] Notes extracted successfully [+]")
        logging.info("Notes extracted and saved")
