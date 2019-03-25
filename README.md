# Introduction

Sometime ago, I opened my mailbox to find approximately 37000+ mails in there. I was determined to clean the same. 
I went on to try a number of tools and even manually deleteing mails. But nothing worked well.

At last, after analyzing, I found out that most of mails are from similar Senders or Domains (eg. job sites, social networking sites, etc.)

Hence, I wrote the following script to delete mails from unknown senders, domains, etc. And also to unsusbcribe to them.

# Installation
1. get sample gmail token
   1. Goto https://developers.google.com/gmail/api/quickstart/python
   1. Click on "ENABLE THE GMAIL API"
   1. Click "Download client configration"
2. Or create a gmail token
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
  