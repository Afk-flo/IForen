import os
import subprocess
import platform
import shutil
import sqlite3

# Check the configuration of the 0S
# Also check for various tools (currently, libdevicemobile)
def checkConfig():
    print("[...] Configuration check ..")
    print(" ")
    if platform.platform()[0] in ['Ubuntu','Debian']:
        print("[+] Platform accepted.")
    else :
        print("[!] Error - Ubuntu or Debian is required to run this tool.")
    
    try:
        subprocess.check_output(['dpkg', '-s', 'libmobiledevice'])
        print("[+] Libomobiledevice is installed")
    except:
        print("[!] Error - LibmobileDevice need to be installed")
        print("[!] Please - Exec : apt-get install libmobiledevice") 

# Detect the mobile access => for further step
def mobileIdentification():
    try:
        result = subprocess.run(['ideviceinfo'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print("[+] Appareil IOS détecté : ")
            print(result.stdout)
            return 0
        else :
            print("[!] Aucun appareil IOS détecté - EXIT")
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
def manageManifest( backupFolder='./backup', outputDir="../output"):
    # Check if the file is here
    manifest_db = os.path.join(backupFolder, "Manifest.db")
    if not os.path.exists(manifest_db):
        print("[!] Manifest.db can't be foud - Please create an other backup or check your IOS version")
        return

    # DB connexion
    conn = sqlite3.connect(manifest_db)
    cursor = conn.cursor()

    # Get the files 
    cursor.execute("SELECT fileID, domain, relativePath, FROM Files")
    files = cursor.fetchall()

    print(f"[+] SQLITE find found : {len(files)}")

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
    
    


if __name__ == "__main__" :
    # clear 
    print("""
          -------------------------------
          |                              |
          |     IForen - IOS Analyzer    |
          |                              |
          -------------------------------
          by Afk-Flo
          """)
    
    # Var
    backupFolder = "./backup"
    outputDir = "./output"
    
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
        manifest = manageManifest(backupFolder,outputDir)
        

