import logging
import os
import sys

from utils.utils import create_connection, folder_check

PATH = "HomeDomain/Library/Safari/Bookmarks.db"

class Safari:
    def __init__(self, backup_path, log, extract_folder):
        self.log = log
        self.backup_path = backup_path
        self.extract_folder = extract_folder

    def extract(self):
        """ Safari Bookmarks extraction and save """
        print("[*] Extracting Safari Bookmarks... [*]")

        conn = create_connection(backup_path=self.backup_path, db_file=PATH)
        if conn is None:
            print("[-] Couldn't fetch Safari Bookmarks [-]")
            sys.exit(1)

        cursor = conn.cursor()
        
        query = """
        SELECT title, url
        FROM bookmarks
        WHERE url IS NOT NULL;
        """

        cursor.execute(query)
        bookmarks = cursor.fetchall()

        print("[+] %d Bookmarks found !" % len(bookmarks))

        # Saving bookmarks
        folder_check(self.extract_folder)
        dest_file = os.path.join(self.extract_folder, "safari_bookmarks.txt")
        with open(dest_file, "w+", encoding="utf-8") as f:
            for bm in bookmarks:
                f.write(f"> Title: {bm[0]} - URL: {bm[1]}\n")

        conn.close()
        print("[+] Safari Bookmarks extracted successfully [+]")
        logging.info("Safari Bookmarks extracted and saved")