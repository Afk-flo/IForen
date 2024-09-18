import os

# func


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

        