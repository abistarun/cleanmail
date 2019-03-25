# Introduction

This is a tool to delete mails by senders or domains. We first analyze your mailbox (This process takes time). Once done, we show you the count of mails per sender.
You can then mark and select the senders whose mails you want to delete. We also show you a list of links from which you should unsubscribe, to avoid junk mails  

### Note:
- Please take care while marking mails for deletion, mails once deleted cannot be restored. We also recommend you should take a backup of your mails.
- We initially ask for read permissions only, delete permissions will be asked as and when required. 
- Using this tool, I reduced the size of my mailbox from 37000+ to 4000 mails

# Installation
1. Get Gmail token
   1. Option 1: Get sample token
       1. Goto https://developers.google.com/gmail/api/quickstart/python
       1. Click on "ENABLE THE GMAIL API"
       1. Click "Download client configration"
   2. Option 2: Create a gmail token
       1. Goto https://console.developers.google.com
       1. Create a new project 
       1. Select the project and click on "ENABLE APIS AND SERVICES"
       1. Search for "Gmail API" and click "Enable"
       1. Click on "Create Credentails"
       1. Select "Gmail API", UI Type : "Other UI" and Access : "User Data"
       1. Click next
       1. If prompted, click "Create Consent Screen"
       1. Type Application Name and keep scope public.
       1. Go to previous tab, type any client id
       1. Click on done and download the key
 
2. Copy the token in ./tokens as credentails.json. Delete the existing file.
3. Install the following 
   1. pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
4. Run the script: python CLI.py
  
## Contact
 - I'll be glad to help, for any doubts please write to abistarun@gmail.com