from src import MailProviderFactory


def login():
    MailProviderFactory.get_mail_provider().connect()


def analyze_mails_by_senders():
    return MailProviderFactory.get_mail_provider().analyze_mails_by_senders()


def logout():
    MailProviderFactory.get_mail_provider().disconnect()


def is_logged_in():
    return MailProviderFactory.get_mail_provider().is_logged_in()


def connect():
    MailProviderFactory.get_mail_provider().connect()


def is_mails_analyzed():
    return MailProviderFactory.get_mail_provider().is_mails_analyzed()


def is_mark_deleted():
    return MailProviderFactory.get_mail_provider().is_mark_deleted()


def get_mails_by_sender():
    return MailProviderFactory.get_mail_provider().get_mails_by_sender()


def get_mails_by_domain():
    return MailProviderFactory.get_mail_provider().get_mails_by_domain()


def mark_senders_for_deletion(senders_to_delete):
    MailProviderFactory.get_mail_provider().mark_senders_for_deletion(senders_to_delete)


def mark_domains_for_deletion(domains_to_delete):
    MailProviderFactory.get_mail_provider().mark_domains_for_deletion(domains_to_delete)


def get_mark_deleted():
    return MailProviderFactory.get_mail_provider().get_mark_deleted()


def get_unsubscribe_links():
    return MailProviderFactory.get_mail_provider().get_unsubscribe_links()


def delete_mails():
    MailProviderFactory.get_mail_provider().delete_mails()