import logging
import os
import sys

from utils.utils import create_connection, folder_check

PATH = "Manifest.db"

class Applications:
    def __init__(self, backup_path, log, extract_folder):
        self.log = log
        self.backup_path = backup_path
        self.extract_folder = extract_folder

    def extract(self):
        """ Applications extraction and save """
        print("[*] Extracting installed applications... [*]")

        conn = create_connection(backup_path=self.backup_path, db_file=PATH)
        if conn is None:
            print("[-] Couldn't fetch Applications [-]")
            sys.exit(1)

        cursor = conn.cursor()
        
        query = """
        SELECT DISTINCT bundle_id
        FROM Apps;
        """

        cursor.execute(query)
        apps = cursor.fetchall()

        print("[+] %d Applications found !" % len(apps))

        # Saving applications
        folder_check(self.extract_folder)
        dest_file = os.path.join(self.extract_folder, "applications.txt")
        with open(dest_file, "w+") as f:
            for app in apps:
                f.write(f"> {app[0]}\n")

        conn.close()
        print("[+] Applications extracted successfully [+]")
        logging.info("Applications extracted and saved")