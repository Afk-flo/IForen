import logging
import os
import sys

from utils.utils import create_connection, folder_check

PATH = "HomeDomain/Library/AddressBook/AddressBook.sqlitedb"

# Encrypted backup only

class CallHistory:
    def __init__(self, backup_path, extract_folder):
        self.backup_path = backup_path
        self.extract_folder = extract_folder

    def extract(self):
        """ Call History Acquisition """
        conn = create_connection(backup_path=self.backup_path, db_file=PATH)
        if conn is None:
            print("[-] Couldn't fecth history call - Is the backup encrypted ? [-]")
            sys.exit(1)


        print("[*] History call aquisition.. [*]")
        cursor = conn.cursor()

        query = """
        SELECT
            ZADDRESS, ZDATE, ZDURATION, ZLOCATION, ZSERVICE_PROVIDER
        FROM
            ZCALLRECORD
        """

        cursor.execute(query)
        calls = cursor.fetchall()

        # print out
        print("[+] %d Calls have been founded ! [+]" % len(calls))

        # Add and save
        folder_check(self.extract_folder)
        dest_file = os.path.join(self.extract_folder, "call_history.txt")
        with open(dest_file, "w+") as f:
            for call in calls:
                #@TODO Get information about the query response
                f.write('- %s' % call)

        conn.close()
        logging.info("Call history acquired and saved to %s" % dest_file)
        print("[+] Call history content have been saved successfully to %s |+]" % dest_file)
