import email
import imaplib
import quopri
import webbrowser
import tkinter as tk
import tkinter
from tkinter import ttk, messagebox
import pyperclip



def link_authorization():
    global link, imap_server
    print("\n TRYING TO GET VERIFICATION LINK...")
    try:
        imap_server = imaplib.IMAP4_SSL('imap.rambler.ru')
        imap_server.login(email_entry.get(), password_entry.get())
        imap_server.select('Inbox')

        # Search for emails with the subject 'Verify Email Address for Discord'
        status, messages = imap_server.search(None, 'SUBJECT "Verify Discord Login from New Location"')

        # Get the IDs of the emails that match the search criteria
        msg_ids = messages[0].split()

        if msg_ids != []:
            for msg_id in msg_ids:
                # Fetch the contents of the email with the matching subject
                status, message = imap_server.fetch(msg_id, '(RFC822)')
                for response in message:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        for msg in msg.get_payload():
                            body = msg.get_payload()

                            decoded_body = quopri.decodestring(body).decode()

                            # Remove = from the body
                            decoded_body = decoded_body.replace("=\n", '')

                            import re
                            # Extract the desired words or sentences using regular expression
                            extracted_text = re.findall(r'(https?://[^\s]+)', decoded_body)
                            link = extracted_text[1]
                            print("\n GOT VERIFICATION LINK ✅")

                            # Mark the email for deletion
                            imap_server.store(msg_id, '+FLAGS', '\\Deleted')

                            # Permanently delete the marked email
                            imap_server.expunge()

                            imap_server.close()
                            imap_server.logout()

                            return link

    except Exception as link_authorization_mail:
        print("\n error in link authorization -", link_authorization_mail)
        messagebox.showerror("Error", "Something went wrong! contact owner")

    else:
        print("\n No email with the specified subject found.")
        messagebox.showinfo("Error", "No email found. pls retry !")


    # Close the mailbox and log out of the email account

def show_popup(link):
    popup_window = tk.Toplevel(window)
    popup_window.title("Login Link")
    popup_window.configure(bg='#333333')
    popup_window.geometry("300x150")
    popup_window.resizable(False, False)

    login_label = tk.Label(popup_window, text="Login Link:" ,bg='#333333', fg="#FF3399")
    login_label.pack()

    login_text = tk.Text(popup_window, width=30, height=3)
    login_text.insert(tk.END, link)
    login_text.configure(state='disabled')
    login_text.pack(pady=10)

    def copy_link():
        pyperclip.copy(link)
        messagebox.showinfo("Link Copied", "The link has been copied to the clipboard.")

    copy_button = tk.Button(popup_window, text="Copy Link", bg="#FF3399", fg="#FFFFFF", font=("Arial", 10),
                            command=copy_link)
    copy_button.pack()

def get_link():
    link = link_authorization()

    if link:
        show_popup(link)

def contact():
    webbrowser.open("https://api.whatsapp.com/send/?phone=917060143862&text=Hi+%21+%0AI+need+Support+discord+login&type=phone_number&app_absent=0")

window = tkinter.Tk()
window.title("Discord login link @rambler : V1")
window.geometry('500x500')
window.configure(bg='#333333')
window.resizable(False, False)
frame = tkinter.Frame(bg='#333333')

# Creating widgets
login_label = tkinter.Label(
    frame, text="Discord Login", bg='#333333', fg="#FF3399", font=("Arial", 30))
username_label = tkinter.Label(
    frame, text="Email", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
email_entry = tkinter.Entry(frame, font=("Arial", 16))
password_entry = tkinter.Entry(frame, font=("Arial", 16))
password_label = tkinter.Label(
    frame, text="Password  ", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
login_button = tkinter.Button(
    frame, text="  Get link  ", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=get_link)

contact_button = tkinter.Button(
    frame, text="☎contact", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=contact)

# Placing widgets on the screen
login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
username_label.grid(row=1, column=0)
email_entry.grid(row=1, column=1, pady=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20)
login_button.grid(row=3, column=0, columnspan=2, pady=30,padx=50)
contact_button.grid(row=9, column=0, columnspan=2, pady=30,padx=50,)

frame.pack()

window.mainloop()
