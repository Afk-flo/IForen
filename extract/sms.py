import logging
import sys
import os

from func.utils.utils import create_connection, folder_check

PATH = "HomeDomain/Library/SMS/sms.db"

class SMS:
    def __init__(self, backup_path, log, result, extract_folder):
        self.log = log
        self.result = result
        self.backup_path = backup_path
        self.extract_folder = extract_folder

    def extract(self):
        """ SMS Database extraction for iOS device """
        conn = create_connection(backup_path=self.backup_path, db_file=PATH)
        if conn is None:
            print("[-] Couldn't fetch SMS [-]")
            sys.exit(1)

        print("[*] SMS-MMS and iMessage acquisition ... [*]")
        cursor = conn.cursor()

        query = """
        SELECT 
            message.date as message_date,
            handle.is as sender,
            message.text as text
        FROM message
        LEFT JOIN handle ON message.handle = handle.id
        ORDER BY message_date ASC;
        """

        """
        Second query : 
        SELECT
            message.*
            handle.id as "number"
        FROM message, handle
        WHERE handle.rowid = message.handle_id
        """

        cursor.execute(query)
        # Messages aquisition
        messages = cursor.fetchall()

        # Print count
        print("[+] %d SMS-MMS and iMessages founded ! [+]" % len(messages))

        # Add and save
        folder_check(self.extract_folder)
        dest_file = os.path.join(self.extract_folder, "sms.txt")
        with open(dest_file, "w+") as f:
            for message in messages:
                date,sender,text = message
                f.write(f"> Date : {date}, From/To: {sender}, Content: {text}\n")

        conn.close()
        logging.info("SMS-MMS and iMessages aquired and save to %s" % dest_file)
        print("[+] SMS-MMS and iMessage content have been saved in %s [+]" % dest_file)



#@TODO:
#    - Type of message
#    - Is Read ?
#    - Connect with contacts
#    - Tranform datatime to something understandable