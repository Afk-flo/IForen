"""
    Log Acquisition Functions
    @by Afk-Flo 
    @Creation data 15/09/24

    This file is designed in order to collect and classified as many as log as possible.
    Thoose logs will be found in database and other storage.
    Thoose logs will help us understand the evidence
    
    [!] Note that, with a backup analysis, it's difficult to get the log
"""
import sqlite3
import os
import shutil
import plistlib


# Crash report analytics
# Helpus to have a better understanding of the apps in the device
# v2@TODO => Better extraction with more information and connexion with current apps
def crashReporter(outputdire="./output", backupdir="./backup", extractdir="./extract"):

    print("[+] Crash log analytics ..")

    manifest_db = os.path.join(backupdir, "manifest.db")
    if not os.path.exists(manifest_db):
        print("[!] Unable to find the manifest.db file")

    # First step - sqlite for file from manifest
    conn = sqlite3.connect(manifest_db)
    cursor = conn.cursor()

    # @TODO query to update for version
    query = """
    SELECT fileID, relativePath
    FROM Files
    WHERE domain = 'HomeDomain' AND relativePath LIKE 'Library/Logs/CrashReporter/%'
    """

    cursor.execute(query)
    crash_logs = cursor.fetchall()

    if not os.path.exists(extractdir):
        os.makedirs(extractdir)

    for fileID, relativePath in crash_logs:
        backup_path = os.path.join(backupdir, fileID[:2], fileID)
        dest_file = os.path.join(extractdir, os.path.basename(relativePath))

        try :
            shutil.copy2(backup_path, dest_file)
            print(f"[+] Crash repport obtained and stored here {dest_file}")
        except Exception as e:
            print(f"[!] Error while copying {backup_path} : {e}")


    # step 2 - Analytics 
    # The crash report will be in the plistlib format
    dest_crash_file = os.path.join(extractdir, 'crashReport.txt')

    with open(dest_file, 'rb') as f:
        crash_datas = plistlib.load(f)

    app_name = crash_datas.get('CFBunbleIdentifier','Unknow idenfier')
    crash_date = crash_datas.get('Date','Unknow crash date')

    print(f"Crash found - {app_name}, Date : {crash_date}")

    return True














    