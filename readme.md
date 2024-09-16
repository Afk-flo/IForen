# IOS Forensic toolkit 
_____________


A simple python script to help investigate IOS Mobile Phone.

## Description
### Features 
Based on the [libimobiledevice](https://github.com/libimobiledevice/libimobiledevice) framework, we aim to build an usefull app, who will allow to lead an forensic investigation.

The mobile don't need to be Jailbreaked (only somes features requires it)

=> Optimised for IOS 17

We implemented features to : 
- Mobile identification and soft data aquisition
- Create an uncrypted/crypted backup 
- Access Filesystem of a device
- Access to SMS/MMS/Imessage
- Access to Media modules
- Access to Safari history (Encrypted backup only)
- Access to Contacts
- Access to Call History
- Access to All Applications 
- Access to Localisation data
- Access to Notes 

### TODO 
We're currently working on : 
- Enable Memory analytics (Device need to be JailBreak, Root access is mandatory)
- Create an HTML report / Web app management 
- Optimise the aquisition process 
- Create a security test (hash management for compromission verification)

## How to use 
### Environment and tools
First, you need to be on a Debian/Ubutu environment.
You need to install libimobiledevice : 
```
sudo apt-get install libimobiledevice-utils
```

Then play the requirements.txt 
```
pip install requirements.txt
```

Now, you can plug the mobile device and you're free to start :) 