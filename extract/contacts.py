import sqlite3
import logging
import os
import sys

from utils.utils import create_connection, folder_check

PATH = "HomeDomain/Library/AddressBook/AddressBook.sqlitedb"

class Contacts:
    def __init__(self, backup_path, log, extract_folder):
        self.log = log
        self.backup_path = backup_path
        self.extract_folder = extract_folder

    def extracts(self):
        """ Contacts extraction and save"""
        print("[*] Extracting contacts... [*]")

        conn = create_connection(backup_path=self.backup_path, db_file=PATH)
        if conn is None:
            print("[-] Couldn't fetch contacts [-]")
            sys.exit(1)

        cursor = conn.cursor()
        query = """
        SELECT first, middle, last, organization FROM  ABPerson ORDER BY ROWID ASC;
        """

        #@TODO -> Check for ADMMultiValue
        # Missing number lol

        cursor.execute(query)
        contacts = cursor.fetchall()

        print(f"[+] {len(contacts)} contacts found ! ")

        # Saving contacts
        folder_check(self.extract_folder)
        dest_file = os.path.join(self.extract_folder, "contacts.txt")
        with open(dest_file, "w+") as f:
            for contact in contacts:
                first,middle,last,organization = contact
                f.write(f"> {first} {middle} {last} - {organization}\n")

        conn.close()
        print("[+] Contacts content have been saved in ./tmp/output/contacts.txt [+]")
        logging.info("Contacts extracted and saved")
