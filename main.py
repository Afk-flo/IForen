import argparse
import sys
from datetime import datetime
import os
import logging
import hashlib

# Extract
from extract.sms import SMS
from extract.call_history import CallHistory
from extract.calendar import Calendar
from extract.notes import Notes
from extract.contacts import Contacts
from extract.applications import Applications
from extract.safari import Safari

# Utils/Func
from func.backupManager import manageManifest

banner = """
██ ███████  ██████  ██████  ███████ ███    ██ 
██ ██      ██    ██ ██   ██ ██      ████   ██ 
██ █████   ██    ██ ██████  █████   ██ ██  ██ 
██ ██      ██    ██ ██   ██ ██      ██  ██ ██ 
██ ██       ██████  ██   ██ ███████ ██   ████ 
                                              
                                              
                                                   iOS Analyzer
                                                   by @Afk-Flo
                                                    
                                                              """

def get_sha256_hash(file_path):
    """Calculate SHA256 hashy."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except IOError:
        return None


if __name__ == '__main__':
    # Welcome aboard
    print(banner)

    parser = argparse.ArgumentParser(
        description="iForen - iOS investigation tool kit"
    )

    parser.add_argument("-b", "--backup", required=True, help="Backup folder for the investigation")
    parser.add_argument("-o", "--output", required=False, help="Output folder for the backup process")
    parser.add_argument("-e", "--extract-folder", required=False, help="Extract folder for the result of the investigation")

    args = parser.parse_args()

    if not args.backup:
        print("[ERROR] Backup folder is required in order to proceed to the investigation [ERROR]")
        sys.exit(1)

    backup = args.backup
    print(f"[INFO] Backup target : {args.backup}")

    if not args.output:
        output = "./tmp/output"
        os.makedirs(os.path.dirname(output), exist_ok=True)
        print(f"[INFO] No output folder provided, using the default {output}")
    else :
        output = args.output
        print(f"[INFO] Output folder {output}")

    if not args.extract_folder:
        extract_folder = "./tmp/extract"
        os.makedirs(extract_folder, exist_ok=True)
        print(f"[INFO] No extract folder provided, using the default {extract_folder}")
    else:
        extract_folder = args.extract_folder
        print(f"[INFO] Extract folder {extract_folder}")


    # Starting the investigation
    print("[INFO] Calculating hash of the backup...")
    backup_hash = "N/A"
    if os.path.isfile(backup):
        backup_hash = get_sha256_hash(backup)
    elif os.path.isdir(backup):
        # If it's a directory, hash the Manifest.db as a fingerprint
        manifest_path = os.path.join(backup, "Manifest.db")
        if os.path.exists(manifest_path):
            backup_hash = f"{get_sha256_hash(manifest_path)} (Manifest.db)"
        else:
            backup_hash = "Directory (Manifest.db not found)"
    print(f"[INFO] Hash of the backup is {backup_hash}")


    start_time = datetime.now()
    start_time_str = start_time.strftime("%d-%m-%Y %H:%M:%S")
    print(f"[INFO] Starting the investigation at {start_time_str}")


    logging.basicConfig(
    filename='IOS_data_acquisition.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
    
    ### Extract pré-D => Old functions
    if not manageManifest(backup,extract_folder): # ManifestDB
        print("[-] Extraction failed or aborted.")
        sys.exit(1)

    # Primo extraction post-d - On fait simple 
    # SMS
    smsExt = SMS(extract_folder,logging,output)
    smsExt.extract()

    # Contact
    contactExt = Contacts(extract_folder,logging,output, )
    contactExt.extracts()
 
    # Call History
    callHistoryExt = CallHistory(extract_folder,logging,output, )
    callHistoryExt.extract()

    # Notes
    notesExt = Notes(extract_folder,logging,output, )
    notesExt.extracts()

    # Calendar activites
    calExt = Calendar(extract_folder,logging,output, )
    calExt.extracts()

    # Applications
    appExt = Applications(backup,logging,output)
    appExt.extract()

    # Safari
    safariExt = Safari(extract_folder,logging,output)
    safariExt.extract()


    #@TODO
    # Check for backup folder - is it empty ?
    # Display a menu for the request
    # Change the txt format for CSV

    # Checkconfig
    # mobileIdentification


    # Encrypted backup management
