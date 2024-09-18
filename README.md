
# IForen - IOS Forensic ToolKit

IForen is a digital investigation tool specializing in IOS phones. This tool will provide you with a web interface to carry out investigations of your IOS backups.




[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
![Issue](https://img.shields.io/badge/Issue-0-green)
![Case solve](https://img.shields.io/badge/Case%20solve-300-red)
## Screenshots

![App Screenshot](https://github.com/Afk-flo/IForen/blob/main/image.png)


## Features

In the current version, the application allow you to: 

- Create and manage investigation case
- Get full access to SMS, MMS & IMessage
- Get access to contact list
- Get access to Safari BookMark (and History for encrypted backup)
- Get access to History Call
- Get access to local Medias
- Get access to Notes
- Get access to Calendar
- Get access to Recording
- Be able to list all of the installed applications
- Be able to list and read some logs

We are currently working on : 
- Filter creation in order to get some deleted / Hidden data 
- Creation of disk copy in order to do some file carving investigation
- JailBreak analysis in order to make memory analysis
- Create a "Generate Report" 
- Optimisation for encrypted backup (Safari, Password, etc..)



## Installation

You can start this project by creating a backup with [LibmobileDevice](https://github.com/libimobiledevice/libimobiledevice) or with Itunes if you are on Mac or Windows.

After this first installation, you can create a backup 
```bash
    # Unencrypted backup 
    idevicebackup2 backup --full /path/to/backup

    # Encrypted backup 
    idevicebackup2 encrytpion on 
    idevicebackup2 backup --full /path/to/backup

```


Then, you can launch the application :
```bash
    python3 app.py

```
You'll able to get to the app at ```http://localhost:5000```


## Authors

- [@Afk-Flo](https://www.github.com/afk-flo)

