"""
    Data Acquisition Functions
    @by Afk-Flo 
    @Creation data 15/09/24

    This file is designed to the data acquisition process.
    After, the first backup step, who will able to exploit two types of files :
    - .db/.sqlite files who will give files paths and types
    - folder who will be crawled in order to find somes files

    By exploiting them, who are able to get all the data available.

    [!] Note that those functions can't find hidden data, please refer to hiddenDataAcquisition.py
    [!] Note that, you won't find any media acquisition here, please refer to mediaAcquisition.py

"""

import os
import sqlite3
import plistlib


# Data acquisition for SMS/MMS and IMessage 
# v1 - All the message will be capted
# v2@TODO - Filter will be available in order to filter : from/To, type, deleted, etc..
def smsExtractor(extractFolder='./extract', outputDir="../output"):
    print("[+] SMS/MMS and IMessage extraction..")

    sms_db_path = os.path.join(outputDir, "HomeDomain/Library/SMS/sms.db")
    if not os.path.exists(sms_db_path):
        print("[+] Unable to find the SMS database")
        return False
     
    conn = sqlite3.connect(sms_db_path)
    cursor = conn.cursor()

    query = """
    SELECT 
        datetime(message.date/100000000 + strftime('%s','1970-01-01'), 'unixepoch', 'localtime') as message_date,
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
    dest_file = os.path.join(extractFolder, "messages.txt")
    with open(dest_file, "w+") as f:
        for message in messages:
            date,sender,text = message
            f.write(f"> Date: {date}, From/To: {sender}, Message : {text} \n")


    conn.close()
    print(f"[+] You can find them in {dest_file}")
    return True


# Contact Acquisition 
# v1 = Get contact file 
# V2@TODO = Mix contact with Message in order to recreate conversation
def contactAcquisition(extractFolder='./extract', outputDir="../output"):
    print("[+] Contact acquisition ..")

    # Path lookup
    contact_db_path = os.path.join(outputDir, "HomeDomain/Library/AddressBook/AddressBook.sqlitedb")
    if not os.path.exists(contact_db_path):
        print("[!] Unable to find the contact database")
        return 
    
    # SQL request + Acquisition
    conn = sqlite3.connect(contact_db_path)
    cursor = conn.cursor()

    # @TODO => Query optimsiation
    query = """
    SELECT First, Last, Organization 
    FROM ABPerson
    """
    cursor.execute(query)
    contacts = cursor.fetchall()

    print(f"[+] {len(contacts)} contacts found ")

    # Save contact in file
    if not os.path.exists(extractFolder):
        os.makedirs(extractFolder)

    dest_file = os.path.join(extractFolder, "contacts.txt")
    with open(dest_file,'w+', encoding='utf-8') as f:
        for contact in contacts:
            f.write(f"{contact}\n")

    conn.close()
    print(f"[+] Acquisition finished - You can find the file here : {dest_file} ")
    return True

# Call History Acquisition
# v1 = Get all call 
# v2@TODO = Mix contact with call history in order to recreate it properly
def callHistoryAcquisition(extractFolder='./extract', outputDir="../output"):
    print("[+] Call history acquisition ..")

    # Path lookup
    history_db_path = os.path.join(outputDir, "HomeDomain/Library/CallHistoryDB/CallHistory.storedata")
    if not os.path.exists(history_db_path):
        print("[!] Unable to find the call history database")
        return 
    
    # SQL
    conn = sqlite3.connect(history_db_path)
    cursor = conn.cursor()

    query = """
    SELECT ZADDRESS, ZDATE, ZDURATION
    FROM ZCALLRECORD
    """

    cursor.execute(query)
    calls = cursor.fetchall()

    print(f"[+] {len(calls)} phone call found")

    # Check for extract 
    if not os.path.exists(extractFolder):
        os.makedirs(extractFolder)

    dest_file = os.path.join(extractFolder, 'call_history.txt')
    with open(dest_file, 'w+', encoding='utf-8') as f:
        for call in calls:
            f.write(f'{call}\n')


    conn.close()
    print(f"[+] Call history acquired - You can find it here {dest_file}")
    return True

# User notes acquisition
# v1 = Find the notes of the user 
# v2@TODO = Try to find deleted notes from the user
def notesAcquisition(extractFolder='./extract', outputDir="../output"):
    print("[+] User notes aquisition ..")

    notes_db = os.path.join(outputDir, 'HomeDomain/Library/Notes/notes.sqlite')
    if not os.path.exists(notes_db):
        print("[!] Unable to find the notes Database")
        return
    
    # Data acquisiton
    # @TODO => Review SQL for timestamp data
    conn = sqlite3.connect(notes_db)
    cursor = conn.cursor()

    query = """
    SELECT ZTITLE, ZTEXT
    FROM ZNOTE
    """

    cursor.execute(query)
    notes = cursor.fetchall()

    print(f"[+] {len(notes)} notes found ")

    # Export in file
    if not os.path.exists(extractFolder):
        os.makedirs(extractFolder)

    dest_file = os.path.join(extractFolder, 'notes.txt')
    with open(dest_file, 'w+', encoding='utf-8') as f:
        for note in notes :
            f.write(f'>{note}\n')

    conn.close()
    print(f"[+] Notes acquired - Please, find the file here {dest_file}")
    return True


# Applications acquisition - Find which application are installed on the user device
# v1 = List user application
# v2@TODO = find more informations and potential data (messages, files,etc..)
def applicationAcquisition(extractFolder='./extract', backupDir="./backup"):
    print("[+] Application aquisiton ..")

    # We'll find the application in the Manifest.db directly, npo need for other db
    manifest_db = os.path.join(backupDir, 'Manifest.db')
    if not os.path.exists(manifest_db):
        print("[!] Unable to find the manifest.db")
        return
    
    conn = sqlite3.connect(manifest_db)
    cursor = conn.cursor()

    # @TODO => Better SQL, currently, only bundle_id 
    query = """
    SELECT DINSTICT bundle_id
    FROM Apps
    """

    cursor.execute(query)
    applications = cursor.fetchall()

    print(f"[+] {len(applications)} applications found")

    # Acqui
    if not os.path.exists(extractFolder):
        os.makedirs(extractFolder)

    dest_file = os.path.join(extractFolder, 'applications.txt')
    with open(dest_file, 'w+', encoding='utf-8') as f:
        for app in applications:
            f.write(f'{app[0]}\n') # check for app[XX]

    conn.close()
    print(f"[+] Applciation acquisition over - find them here {dest_file}")
    return True


# Calendar acquisition 
# v1 = Find and list element acquired
# v2@TODO = Try to get more info and deleted informations
def calendarAcquisition(extractFolder='./extract', outputDir="../output"):
    print("[+] Calendar aquisition .. ")

    calendar_db = os.path.join(outputDir, 'HomeDomain/Library/Calendar/Calendar.sqlitedb')
    if not os.path.exists(calendar_db):
        print("[!] Unable to find calendar database")
        return
    
    # SQL acqui
    conn = sqlite3.connect(calendar_db)
    cursor = conn.cursor()

    query = """
    SELECT summary, start_date, end_date
    FROM CalendarItem
    """

    cursor.execute(query)
    datas = cursor.fetchall()

    print(f"[+] {len(datas)} calendar evenment found ")

    # extraction
    if not os.path.exists(extractFolder):
        os.makedirs(extractFolder)

    dest_file = os.path.join(extractFolder, 'calendar.txt')
    with open(dest_file, 'w+', encoding='utf-8') as f :
        for data in datas:
            f.write(f'Event : {data}\n')
        
    conn.close()
    print(f"[+] Event acquired - You find them here {dest_file}")    
    return True


# Mail aquisition
# v1 = Find information about mail account/Usage
# v2@TODO = Try to find more informations about account usage and mails datas
def mailAcquisition(extractFolder='./extract', outputDir="../output"):
    # Need more investigation in order to find the right path (change for IOS Versionning)
    # Manifest.dn => sql query for LIKE 'HOMEDOmain/LIbary/Mail/%' in order to adapt
    
    pass


# Wireless Acquisition
# @TODO - FILE MANAGEMENT
# v1 = Find wireless information (connexion, SSID, timestamp)
# v2@TODO = Find more information with precise timestamp
def wirelessAcquition(extractFolder='./extract', outputDir="../output"):
    print("[+] Wireless Data Acquisition ..")

    wireless_db = os.path.join(outputDir, 'SystemPreferencesDOmain/SystemConfiguration/com.apple.wifi.plist')
    if not os.join.exists(wireless_db):
        print("[!] Unable to find the wireless database")
        return
    
    if not os.path.exists(extractFolder):
        os.makedirs(extractFolder)
    
    # file extraction here
    with open(wireless_db, 'rb') as f:
        plist_data = plistlib.load(f)

    # data cquisiton 
    networks = plist_data.get('List of known networks', [])

    dest_file = os.path.join(extractFolder, 'networks.txt')
    cnt = 0
    with open(dest_file, 'w+', encoding='utf-8') as f:
        for network in networks:
            cnt += 1
            # try to exploit the SSID - or Unknow
            ssid = network.get('SSID_STR', 'Unknow SSID')
            f.write(f'SSID : {ssid}\n')

    print(f"[+] {cnt} networks found ")
    print(f"[+] You can find them here {dest_file}")

    return True


# Safari Bookmark and History collect 
# [!] Note that History acquisition is only available for Encrypted backup
def safariAcquisiton(extractFolder='./extract', outputDir="../output"):
    pass

# GPS datas
# [!] Caefull with this one
def localisationAcquisition(extractFolder='./extract', outputDir="../output"):
    pass

# Recording for User
#
def recordingAcquisition(extractFolder='./extract', outputDir="../output"):
    pass

