from src.MailProvider import MailProvider
from src.gmail.GmailProvider import GmailProvider

provider = None


def get_mail_provider() -> MailProvider:
    global provider
    if not provider:
        provider = GmailProvider()
    return provider
