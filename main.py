import os
import subprocess
import platform
import shutil
import sqlite3
import glob

# Check the configuration of the 0S
# Also check for various tools (currently, libdevicemobile)
def checkConfig():
    print("[...] Configuration check ..")
    print(" ")
    if platform.platform()[0] in ['Ubuntu','Debian','Fedora']:
        print("[+] Platform accepted.")
    else :
        print("[!] Error - Ubuntu, Debian or Fedora is required to run this tool.")
    
    try:
        subprocess.check_output(['dpkg', '-s', 'libmobiledevice'])
        print("[+] Libomobiledevice is installed")
    except:
        print("[!] Error - LibmobileDevice need to be installed")

# Detect the mobile access => for further step
def mobileIdentification():
    try:
        result = subprocess.run(['ideviceinfo'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print("[+] Appareil IOS détecté : ")
            #print(result.stdout)
            return 0
        else :
            print("[!] Aucun appareil IOS détecté - No mobile analysis")
    except Exception as e:
        print(f"Error while collecting data :  {e}")


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
            result = subprocess.run(['idevicebackup2', 'backup', backupFolder], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) 

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
    print(f"[+] Files extracted - Available here {dest_dir}")
    
# Data extraction for SMS/MMS and IMessage 
def smsExtractor(extractFolder='./extract', outputDir="../output"):
    print("[+] SMS/MMS and IMessage extraction..")

    sms_db_path = os.path.join(outputDir, "HomeDomain/Library/SMS/sms.db")
    if not os.path.exists(sms_db_path):
        print("[+] Unable to find the SMS database")
        return 
     
    conn = sqlite3.connect(sms_db_path)
    cursor = conn.cursor()

    query = """
    SELECT 
        datetime(message.date/100000000 + strftime('%s','2001-01-01'), 'unixepoch', 'localtime') as message_date,
        handle.id as sender,
        message.text
    FROM message
    LEFT JOIN handle ON message.handle_id = handle.rowid
    ORDER BY message_date ASC
    """

    cursor.execute(query)
    messages = cursor.fetchall()

    # print count 
    print(f"[+] {len(messages)} SMS/MSS and IMessages found !")

    if not os.path.exists(extractFolder):
        os.makedirs(extractFolder)

    # Add in files 
    dest_file = os.path.join(extractFolder, "SMS_MMS")
    with open(dest_file, "w+") as f:
        for message in messages:
            date,sender,text = message
            f.write(f"> Date: {date}, From/To: {sender}, Message : {text} \n")


    conn.close()
    print(f"[+] You can find them in {dest_file}")
    return


# Media extraction
# For now - All media | @TODO => Find deleted and hidden one
# Multi type of data to acquire :
# - Data from DCIM
# - Data from SMS/MMS Attachement
# - Data from external sources (tiers app)

# FILTER 
# Need to add Filter to the SQL request in order to 
# - Get hidden files => Flag : WHERE ZHIDDENSTATE = 1;
# - Get trashed files => Flag : WHERE ZTRASHEDSTATE = 1;

# CURRENT STATE
# Only local media are available, Apple policiy will only keep thumbnails and some medias here.
# Full size medias will be uploaded in their Icloud
def extractMedia(extractFolder='./extract', outputDir="../output"):
    print(" ")
    print("[+] Media extraction (Images,Vidéo,Sound) ..")

    # Extraction from Photos.db - DCIM Focus
    media_db_path = os.path.join(outputDir, "CameraRollDomain/Media/PhotoData/Photos.sqlite")
    if not os.path.exists(media_db_path):
        print("[+] Unable to find the Media database")
        return 
    
    # Folder management
    if not os.path.exists(extractFolder):
        os.makedirs(extractFolder)

    dest_medias = os.path.join(extractFolder, "MEDIAS")
    if not os.path.exists(dest_medias):
        os.makedirs(dest_medias)
    
    conn = sqlite3.connect(media_db_path)
    cursor = conn.cursor()

    # Get all (no distinction for Cloud, deleted, hidden..)
    query = """
    SELECT ZDIRECTORY, ZFILENAME
    FROM ZASSET;
    """

    cursor.execute(query)
    medias = cursor.fetchall()

    cnt = 0
    
    # Sent to it
    for media in medias:
        ZDIRECTORY, ZFILENAME = media
        if ZDIRECTORY and ZFILENAME:
            # Local path
            relative_path = os.path.join(ZDIRECTORY, ZFILENAME)
            file_path_output = os.path.join(outputDir, "CameraRollDomain/Media", relative_path)

            # Dest -> dest_medias
            dest = os.path.join(dest_medias)
            
            try : 
                if os.path.exists(file_path_output):
                    shutil.copy(file_path_output, dest)
                    print(f"[+] File {relative_path} copied")
                    cnt +=1
                else :
                    pass
                    #print(f"[!] File {file_path_output} not found in backup")
            except Exception as e :
                print(f">>>> Exception : {e} <<<<< ")

    conn.close()

    print(f"[!] Media extraction over - You'll find them here : {dest_medias}")
    print(f"[+] {len(medias)} medias found, {cnt} media copied")

    return


if __name__ == "__main__" :
    # clear 
    print("""
          -------------------------------
          |                              |
          |     IForen - IOS Analyzer    |
          |                              |
          --------------------extractFolder-----------
          by Afk-Flo
          """)
    
    # Var
    backupFolder = "./backup"
    outputDir = "./output"
    extractFolder = "./extract"
    
    # Check if backup exist, if not create it
    checkConfig()
    resultat = mobileIdentification()

    if resultat == 0:

        # Create backup is not already here
        if not os.path.exists(backupFolder):  
            print("[--] Do you want to encrypt the backup ? (Enter password for Y/ enter for N)")
            password = input(">")
            backupFolder = createBackup(password=password)

        # If backup is here, analyse
        print("[+] Backup déjà présente .. Analyse")
        manifest = manageManifest(backupFolder,outputDir)
        smsExtractor(backupFolder, outputDir)
        extractMedia(extractFolder, outputDir)

        
    else : 
        # If backup is here and no phone
        print("[+] Backup found & no mobile analysis")
        #manifest = manageManifest(backupFolder,outputDir) - testing purpose

        print(" ")
        print("[...] Data extraction .. ")
        smsExtractor(extractFolder, outputDir)
        extractMedia(extractFolder, outputDir)

        
