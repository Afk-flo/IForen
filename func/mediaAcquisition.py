"""
    Media Acquisition Functions
    @by Afk-Flo 
    @Creation data 15/09/24

    This file is designed in order to make the Media Acquisition process easier.
    Media aquisition is kind of complicated in IOS environment. Files can be found in various folder in a lot of differents places.
    Forthermore, the aquisition process can be complicated, even if the file are in the database, most of them will be stored in the Icloud.
    In the V1, we will try to catch as many local media as possible.
    
"""

import sqlite3
import os
import shutil
import logging

logging.basicConfig(
    filename='IOS_data_acquisition.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

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
    # METADATA FIRST
    for media in medias:
        ZDIRECTORY, ZFILENAME = media
        if ZDIRECTORY and ZFILENAME:
            # Local path
            relative_path = os.path.join(ZDIRECTORY, ZFILENAME)
            file_path_output = os.path.join(outputDir, "CameraRollDomain/Media/PhotoData/Metadata", relative_path)

            # Dest -> dest_medias
            dest = os.path.join(dest_medias)
            
            try : 
                if os.path.exists(file_path_output):
                    shutil.copy(file_path_output, dest)
                    #print(f"[+] File {relative_path} copied")
                    cnt +=1
                else :
                    pass
                    #print(f"[!] File {file_path_output} not found in backup")
            except Exception as e :
                print(f">>>> Exception : {e} <<<<< ")


    print(f"[!] First check (Metadata) - Media extraction over - You'll find them here : {dest_medias}")
    print(f"[+] {len(medias)} medias found, {cnt} media copied")
    print(f"[!] Some files are currenlty stocked in the ICloud - Can't be accessed locally")


    # OUI,C'EST MOCHE, MAIS ON VA CORRIGER TKT
    # Media access now
    max = cnt
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
                    #print(f"[+] File {relative_path} copied")
                    cnt +=1
                else :
                    pass
                    #print(f"[!] File {file_path_output} not found in backup")
            except Exception as e :
                print(f">>>> Exception : {e} <<<<< ")

    conn.close()

    print(f"[!] Second check (DB Access) - Media extraction over - You'll find them here : {dest_medias}")
    print(f"[+] {len(medias)} medias found, {cnt} media copied")
    print(f"[!] Some files are currenlty stocked in the ICloud - Can't be accessed locally")

    print(" ")
    print(f"[--] Total file acquired : {max + cnt}")
    return
