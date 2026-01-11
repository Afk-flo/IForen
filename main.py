import argparse
import sys
from datetime import datetime
import os

# Extract
from extract.sms import SMS
from extract.call_history import CallHistory
from extract.calendar import Calendar
from extract.notes import Notes
from extract.contacts import Contacts

banner = """
 ________  ______   ______   ______    ______   ___   __      
/_______/\/_____/\ /_____/\ /_____/\  /_____/\ /__/\ /__/\    
\__.::._\/\::::_\/_\:::_ \ \\:::_ \ \ \::::_\/_\::\_\\  \ \   
   \::\ \  \:\/___/\\:\ \ \ \\:(_) ) )_\:\/___/\\:. `-\  \ \  
   _\::\ \__\:::._\/ \:\ \ \ \\: __ `\ \\::___\/_\:. _    \ \ 
  /__\::\__/\\:\ \    \:\_\ \ \\ \ `\ \ \\:\____/\\. \`-\  \ \
  \________\/ \_\/     \_____\/ \_\/ \_\/ \_____\/ \__\/ \__\/
                                                   iOS Analyzer
                                                   by @Afk-Flo
                                                    
                                                              """


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
        output = "./output"
        os.makedirs(os.path.dirname(output), exist_ok=True)
        print(f"[INFO] No output folder provided, using the default {output}")
    else :
        output = args.output
        print(f"[INFO] Output folder {output}")

    if not args.extract_folder:
        extract_folder = "./extract"
        os.makedirs(extract_folder, exist_ok=True)
        print(f"[INFO] No extract folder provided, using the default {extract_folder}")
    else:
        extract_folder = args.extract_folder
        print(f"[INFO] Extract folder {extract_folder}")


    # Starting the investigation
    start_time = datetime.now()
    start_time_str = start_time.strftime("%d-%m-%Y %H:%M:%S")
    print(f"[INFO] Starting the investigation at {start_time_str} - Good luck")

    # Primo extraction - On fait simple 
    # SMS
    smsExt = SMS()
    smsExt.extract()

    Contacts.extracts()
    CallHistory.extract()
    Notes.extracts()
    Calendar.extracts()


    #@TODO
    # Check for backup folder - is it empty ?
    # Display a menu for the request
    # Change the txt format for CSV

    # Checkconfig
    # mobileIdentification


    # Encrypted backup management
