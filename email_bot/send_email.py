
import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path

from dotenv import load_dotenv  # pip install python-dotenv

PORT = 587  
EMAIL_SERVER = "smtp.gmail.com"  # Adjust server address, if you are not using @outlook

# Load the environment variables
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

# Read environment variables
sender_email = os.getenv("EMAIL")
password_email = os.getenv("PASSWORD")


def send_email(subject, email_receiver, gym_owner, gym_name,body):
    # Create the base text message.
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("VertexTop", f"{sender_email}"))
    msg["To"] = email_receiver
    msg["BCC"] = sender_email

    msg.set_content(body,subtype = "html")


    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, password_email)
        try:
            server.sendmail(sender_email, email_receiver, msg.as_string())
        except smtplib.SMTPResponseException as e:
            import traceback
            traceback.print_exc()
            print("Errore SMTPResponseException:", e)
        


if __name__ == "__main__":
    send_email(
        subject="Invoice Reminder",
        gym_owner="Antonio D'alessandro",
        email_receiver="personofinmterest@gmail.com",
        gym_name="New Move",
        body= f"""
                Salve {gym_owner}, tutto bene?

                Sarò diretto, ho controllato la vostra palestra su internet e sarebbe bello lavorare con voi: vi sto rubando del tempo per dirvi che vi aiuteremmo ad avere nuovi clienti. 
                (sempre se ne avete davvero bisogno).

                Senza dilungarmi inutilmente, avrete nuova clientela a fine del servizio (circa 3 mesi).
                Acquisiamo i contatti e li tramutiamo in clienti, in maniera automatica.

                La parte più bella è che se non siete soddisfatti del servizio, vi rimborsiamo. Veniamo pagati solo se voi avete nuovi clienti e siete contenti. Alla fine il nostro successo dipende dal vostro.

                Ho un sistema specifico per ottenere questi risultati e sarei davvero contento se avessi l'opportunità di mostrare come funziona, magari in una videochiamata. 
                Vi piacerebbe l’idea di programmare questa chiamata, senza impegno, anche questa settimana? Se avete spazio per nuovi clienti ovviamente!


                Grazie

                Paolo Ligori. 

                Tel 0621701576
                atvertextop@gmail.com



                """
    )
