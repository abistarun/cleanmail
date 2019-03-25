class MailProvider(object):

    def connect(self):
        pass

    def analyze_mails_by_senders(self):
        pass

    def disconnect(self):
        pass

    def is_logged_in(self):
        pass

    def is_mails_analyzed(self):
        pass

    def is_mark_deleted(self):
        pass

    def get_mails_by_sender(self):
        pass

    def get_mails_by_domain(self):
        pass

    def mark_senders_for_deletion(self, senders_to_delete):
        pass

    def mark_domains_for_deletion(self, domains_to_delete):
        pass

    def get_mark_deleted(self):
        pass

    def get_unsubscribe_links(self):
        pass

    def delete_mails(self):
        pass
