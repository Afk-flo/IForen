"""
    Backup Acquisition Functions
    @by Afk-Flo 
    @Creation data 15/09/24

    This file is only designed for the backup process.
    Here, we will decide and create the appropriate backup (encrypted or not)
    And manage it.
    
"""
import os
import subprocess
import sqlite3
import shutil

# Create a backup - using idevicebackup
# User will be able to send a password or not if he want to encrypt it
def createBackup(password=None, backupFolder='./backup'):
    # Create the folder if not here
    if not os.path.exists(backupFolder):
        os.makedirs(backupFolder)

    try :
        # Current - Idevicebackup2
        if password is None:
            result = subprocess.run(['idevicebackup2', 'backup', backupFolder], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)        
        else:    
            # Need to add the right command
            # result = subprocess.run(['idevicebackup2', 'backup', backupFolder], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) 
            subprocess.run(['idevicebackup2','encryption','on',password])
            result = subprocess.run(['idevicebackup2','backup', backupFolder])
            # Wehn completed, restore the data
            subprocess.run(['idevicebackup2', 'encryption','off'])
            subprocess.run(['idevicebackup2', 'restore', backupFolder, '--password', password])
            # done

        if result.returncode == 0:
            print(f"[+] Backup fully captured, find it here : {backupFolder}")
        else :
            print("[!] Error while Backuping - Restart")
            print(result.stderr)

    except Exception as e:
        print(f"Error while backup - {e}")
    return backupFolder


# Manifest.db will help us find the other sqlite files
def manageManifest(backupFolder='./backup', outputDir="../output"):
    # Check if the file is here
    manifest_db = os.path.join(backupFolder, "Manifest.db")
    if not os.path.exists(manifest_db):
        print("[!] Manifest.db can't be foud - Please create an other backup or check your IOS version")
        return

    # DB connexion
    conn = sqlite3.connect(manifest_db)
    cursor = conn.cursor()

    #### Encrypted check
    """
    import plistlib
    manifest_plist = os.path.join(backupFolder, "Manifest.plist")
    with open(manifest_plist, "rb") as f:
        pl = plistlib.load(f)

    if pl.get("IsEncrypted"):
        print(f"[ERROR] Manifest.db is encrypted (IsEncrypted={pl.get('IsEncrypted')}) - Exit")
        return False
        # exit(1)
        
    """

    # Get the files  
    cursor.execute("SELECT fileID, domain, relativePath FROM Files")
    files = cursor.fetchall()

    print(f"[+] SQLITE filesl found : {len(files)}")

    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    for file in files:
        fileID, domain, relativePath = file
        # Hashed files 
        src = os.path.join(backupFolder, fileID[:2], fileID)
        if not os.path.exists(src):
            continue

        # Then, rebuild with the original filepath 
        dest_path = os.path.join(outputDir, domain, relativePath)
        dest_dir = os.path.dirname(dest_path)

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir, exist_ok=True)

        # Then copy each file
        try:
            shutil.copy2(src, dest_path)
        except Exception as e :
            print(f"Error while copying the Sqlite {src} : {e}")

    conn.close()
    print(f"[+] Files extracted - Available here {outputDir}")
    return True
