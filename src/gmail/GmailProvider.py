import base64
import email
import json
import os
import pickle
import random
import re
import shutil
import time

import pandas as pandas
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from src.MailProvider import MailProvider


class GmailProvider(MailProvider):
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    DELETE_SCOPES = ['https://mail.google.com/']

    def __init__(self):
        self.service = None

    def connect(self):
        creds = None
        if not os.path.exists('./cache/'):
            os.mkdir("./cache/")
        if os.path.exists('./cache/token.pickle'):
            with open('./cache/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    './tokens/credentials.json', self.SCOPES)
                creds = flow.run_local_server()
            with open('./cache/token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)

    def disconnect(self):
        if os.path.exists('./cache/'):
            shutil.rmtree("./cache/")

    def is_logged_in(self):
        return os.path.exists('./cache/token.pickle')

    def is_mails_analyzed(self):
        return os.path.exists('./cache/mails_by_sender.json')

    def is_mark_deleted(self):
        return os.path.exists('./cache/senders_to_delete.json') or os.path.exists('./cache/domains_to_delete.json')

    def mark_senders_for_deletion(self, senders_to_delete):
        with open('./cache/senders_to_delete.json', 'w') as f:
            json.dump(senders_to_delete, f)

    def mark_domains_for_deletion(self, domains_to_delete):
        with open('./cache/domains_to_delete.json', 'w') as f:
            json.dump(domains_to_delete, f)

    def get_mark_deleted(self):
        senders = None
        domains = None
        if os.path.exists('./cache/senders_to_delete.json'):
            with open('./cache/senders_to_delete.json', 'rb') as token:
                senders = json.load(token)
        if os.path.exists('./cache/domains_to_delete.json'):
            with open('./cache/domains_to_delete.json', 'rb') as token:
                domains = json.load(token)
        return {
            "Sender": senders,
            "Domains": domains
        }

    def get_mails_by_sender(self):
        with open('./cache/mails_by_sender.json', 'rb') as token:
            mails_by_sender = json.load(token)
        df = pandas.DataFrame(columns=["Sender", "Mail Count"])
        for i, entry in enumerate(mails_by_sender.items()):
            df.loc[i] = [entry[0], len(entry[1])]
        df.sort_values("Mail Count", ascending=False, inplace=True)
        return df

    def get_unsubscribe_links(self):
        mails_to_delete = self.get_mails_to_delete()
        result = []
        for _, mails in mails_to_delete.items():
            for i in range(0, 1):
                try:
                    m = random.choice(mails)
                    content = self._get_message_body(m)

                    search = re.findall('<a[^>]*href[^>]*>[^<]*</a>', content)
                    for link in search:
                        if "unsubscribe" in link.lower():
                            link = re.findall("href=[^'\"]*['\"][^'\"]*['\"]", link)[0]
                            link = re.findall("http[^\"']*", link)[0]
                            if link not in result:
                                result.append(link)
                except Exception as e:
                    pass
        return result

    def delete_mails(self):
        flow = InstalledAppFlow.from_client_secrets_file('./tokens/credentials.json', self.DELETE_SCOPES)
        creds = flow.run_local_server()
        del_service = build('gmail', 'v1', credentials=creds)

        user_id = self.service.users().getProfile(userId='me').execute()['emailAddress']
        del_user_id = del_service.users().getProfile(userId='me').execute()['emailAddress']
        if user_id != del_user_id:
            print("Please sign in using the same user.")
            return

        mails_to_delete = self.get_mails_to_delete()
        del_id = []
        for _, mails in mails_to_delete.items():
            del_id += mails
        self._fire_delete(del_id, del_service)

    def _fire_delete(self, msgs, del_service):
        chunkSize = 999
        for i in range(0, len(msgs), chunkSize):
            chunk = msgs[i:i + chunkSize]
            del_service.users().messages().batchDelete(userId='me', body={
                'ids': chunk
            }).execute()
        print("Deleted Count : " + str(len(msgs)))

    def _get_message_body(self, msg_id):
        message = self.service.users().messages().get(userId='me', id=msg_id, format='raw').execute()
        msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
        mime_msg = email.message_from_bytes(msg_str)
        messageMainType = mime_msg.get_content_maintype()
        if messageMainType == 'multipart':
            for part in mime_msg.get_payload():
                if part.get_content_maintype() == 'text':
                    return part.get_payload().replace("=\r\n", "")
            return ""
        elif messageMainType == 'text':
            return mime_msg.get_payload()

    def get_mails_to_delete(self):
        mark_deleted = self.get_mark_deleted()
        senders = mark_deleted["Sender"]
        domains = mark_deleted["Domains"]
        with open('./cache/mails_by_sender.json', 'rb') as token:
            mails_by_sender = json.load(token)
        mails_to_delete = {}
        for sender, mail_list in mails_by_sender.items():
            domain = re.search("@[\w.]+", sender).group()
            if (senders and sender in senders) or (domains and domain in domains):
                mails_to_delete[sender] = mail_list
        return mails_to_delete

    def get_mails_by_domain(self):
        with open('./cache/mails_by_sender.json', 'rb') as token:
            mails_by_sender = json.load(token)
        mails_by_domain = {}
        for sender, msg_list in mails_by_sender.items():
            domain = re.search("@[\w.]+", sender).group()
            if domain not in mails_by_domain:
                mails_by_domain[domain] = 0
            mails_by_domain[domain] += len(msg_list)
        df = pandas.DataFrame(columns=["Domain", "Mail Count"])
        for i, entry in enumerate(mails_by_domain.items()):
            df.loc[i] = [entry[0], entry[1]]
        df.sort_values("Mail Count", ascending=False, inplace=True)
        return df

    def analyze_mails_by_senders(self):
        start = time.time()
        mails_by_sender = {}
        analyzed_mails = []
        response = self._execute_list_messages()
        self._populate_mails_by_sender(mails_by_sender, response, analyzed_mails)

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = self._execute_list_messages(page_token=page_token)
            self._populate_mails_by_sender(mails_by_sender, response, analyzed_mails)
        with open('./cache/mails_by_sender.json', 'w') as f:
            json.dump(mails_by_sender, f)
        return time.time() - start

    def _populate_mails_by_sender(self, mails_by_sender, response, analyzed_mails):
        if 'messages' in response:
            for msg in response['messages']:
                if msg['id'] not in analyzed_mails:
                    sender = self._get_sender(msg['id'])
                    if not sender:
                        continue
                    if sender not in mails_by_sender:
                        mails_by_sender[sender] = []
                    mail_ids = self._get_mails_by_sender(sender)
                    analyzed_mails += mail_ids
                    mails_by_sender[sender] += mail_ids
                    t_1 = sum(len(item) for _, item in mails_by_sender.items())
                    print("Analysing sender : {:100s} | Mails analyzed count = {:5d}".format(sender, t_1))

    def _get_sender(self, msg_id):
        messages_details = self.service.users().messages().get(userId='me', id=msg_id).execute()
        for curr in messages_details['payload']['headers']:
            if curr['name'] == 'From':
                match = re.search(r'[\w\.-]+@[\w\.-]+', curr['value'])
                if match:
                    return match.group(0)
                else:
                    return curr['value']

    def _get_mails_by_sender(self, sender):
        if sender is None:
            return []
        query = 'from:' + sender
        response = self.service.users().messages().list(userId='me', q=query).execute()
        messages = []
        if 'messages' in response:
            for msg in response['messages']:
                messages.append(msg['id'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = self.service.users().messages().list(userId='me',
                                                            q=query,
                                                            pageToken=page_token).execute()
            if 'messages' in response:
                for msg in response['messages']:
                    messages.append(msg['id'])
        return messages

    def _get_count(self, q=None):
        response = self._execute_list_messages()
        count = 0
        if 'messages' in response:
            count += response['resultSizeEstimate']

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = self._execute_list_messages(page_token=page_token, q=q)
            count += response['resultSizeEstimate']

        return count

    def _execute_list_messages(self, page_token=None, q=None):
        return self.service.users().messages().list(userId='me', pageToken=page_token, q=q,
                                                    maxResults=10000).execute()
