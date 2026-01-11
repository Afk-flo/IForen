import logging
import os
import sys

from utils.utils import create_connection, folder_check

PATH = "HomeDomain/Library/Calendar/Calendar.sqlitedb"
# QUERY ZTITLE, ZTEXT from ZNOTE

class Calendar:
    def __init__(self, backup_path, log, result, extract_folder):
        self.log = log
        self.result = result
        self.backup_path = backup_path
        self.extract_folder = extract_folder

    def extracts(self):
        """ Calendar events extraction and save"""
        print("[*] Extracting calendar events... [*]")

        conn = create_connection(backup_path=self.backup_path, db_file=PATH)
        if conn is None:
            print("[-] Couldn't fetch Events [-]")
            sys.exit(1)

        cursor = conn.cursor()
        query = """
        SELECT
            summary, start_date, end_date
        FROM 
            CalendarItem;
        """

        cursor.execute(query)
        calendar = cursor.fetchall()

        print("[+] %d Calendar events found ! ", len(calendar))

        # Saving contacts
        folder_check(self.extract_folder)
        dest_file = os.path.join(self.extract_folder, "calendar.txt")
        with open(dest_file, "w+") as f:
            for event in calendar:
                summary, start_date, end_date = event
                f.write(f"> {summary} : {start_date} - {end_date} \n")

        conn.close()
        print("[+] Calendar events extracted successfully [+]")
        logging.info("Calendar extracted and saved")
