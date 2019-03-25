from collections import OrderedDict

import pandas

from src import Captain


def print_df(df):
    print(df.to_string(index=False, justify="left"))
    print("{:50s} = {:10d}".format("Total", sum(df["Mail Count"])))


def mark_sender(df: pandas.DataFrame):
    field = "Sender"
    senders_to_delete = mark(df, field)
    Captain.mark_senders_for_deletion(senders_to_delete)
    print(str(len(senders_to_delete)) + " senders marked for deletion")


def mark_domains(df: pandas.DataFrame):
    field = "Domain"
    senders_to_delete = mark(df, field)
    Captain.mark_domains_for_deletion(senders_to_delete)
    print(str(len(senders_to_delete)) + " domains marked for deletion")


def mark(df, field):
    print("We will display all entries with their count. Please press y to mark for deletion or n to skip. Press x to "
          "stop. To change anything you can refer the json stored in ./cache")
    senders_to_delete = []
    for index, row in df.iterrows():
        sender = row[field]
        print("{:100s} | {:10d} (y or n)".format(sender, row["Mail Count"]))
        op = input()
        if op == "y":
            senders_to_delete.append(sender)
            print("Added")
        elif op == "x":
            print("Stop")
            break
        else:
            print("Skipped")
            continue
    return senders_to_delete


def show_mark_deleted(d):
    print("##############################################")
    for k, v in d.items():
        if v:
            print("Mails from following " + k + " will be deleted:")
            for entry in v:
                print("\t" + entry)
            print("##############################################")
    print("To change anything you can refer the json stored in ./cache")


def show_unsubscribe_links(links):
    if not links:
        print("No links found")
        return
    print("We suggest you should unsubscribe from the following urls")
    for l in links:
        print("\t" + l)


def analyze_mails_by_senders():
    print("This process takes time. Approx 7 min for 5000 mails. Continue ? (y or n)")
    op = input()
    if op == 'y':
        return Captain.analyze_mails_by_senders()
    else:
        return 0


def delete_mails():
    print("We suggest you should unsubscribe to junk mails before continuing. Unsubscribe ? (y or n)")
    op = input()
    if op == 'y':
        links = Captain.get_unsubscribe_links()
        show_unsubscribe_links(links)
    mark_deleted = Captain.get_mark_deleted()
    show_mark_deleted(mark_deleted)
    print("Continue ? (y or n)")
    op = input()
    if op == 'y':
        Captain.delete_mails()


if __name__ == "__main__":
    pandas.set_option('display.max_columns', None)  # or 1000
    pandas.set_option('display.max_rows', None)  # or 1000
    pandas.set_option('display.max_colwidth', -1)  # or 199

    is_logged_in = Captain.is_logged_in()
    if is_logged_in:
        Captain.connect()
    while True:
        is_logged_in = Captain.is_logged_in()
        is_mails_analyzed = Captain.is_mails_analyzed()
        is_mark_deleted = Captain.is_mark_deleted()
        options = OrderedDict()
        if not is_logged_in:
            options["Login"] = (Captain.login, lambda _: print("Login Successful"))
        if is_logged_in:
            options["Analyze Mails by Senders"] = (analyze_mails_by_senders, lambda t: print("Analysis Done. "
                                                                                             "Time taken : "
                                                                                             + str(t) + " sec"))
        if is_logged_in and is_mails_analyzed:
            options["Show Mails Count by Sender"] = (Captain.get_mails_by_sender, lambda df: print_df(df))
        if is_logged_in and is_mails_analyzed:
            options["Show Mails Count by Domain"] = (Captain.get_mails_by_domain, lambda df: print_df(df))
        if is_logged_in and is_mails_analyzed:
            options["Mark mails for deletion by Sender"] = (Captain.get_mails_by_sender, lambda df: mark_sender(df))
        if is_logged_in and is_mails_analyzed:
            options["Mark mails for deletion by Domain"] = (Captain.get_mails_by_domain, lambda df: mark_domains(df))
        if is_logged_in and is_mails_analyzed and is_mark_deleted:
            options["Show mark deleted items"] = (Captain.get_mark_deleted, lambda d: show_mark_deleted(d))
        if is_logged_in and is_mails_analyzed and is_mark_deleted:
            options["Unsubscribe to junk mails"] = (Captain.get_unsubscribe_links, lambda d: show_unsubscribe_links(d))
        if is_logged_in and is_mails_analyzed and is_mark_deleted:
            options["Delete mails"] = (delete_mails, lambda _: print("Mails deleted successfully!!"))

        if is_logged_in:
            options["Logout"] = (Captain.logout, lambda _: print("Logout Successful"))

        index = 1
        print("Select a option or 99 to exit")
        for key, value in options.items():
            print(str(index) + ". " + key)
            index += 1

        op = int(input()) - 1
        if op == 98:
            break
        selected_option = list(options.items())[op][1]
        output = selected_option[0]()
        selected_option[1](output)
        print("---------------------------------------------------------------------------------------------")
