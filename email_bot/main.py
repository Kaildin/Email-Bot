from datetime import datetime, date, timedelta
import pandas as pd 
from send_email import send_email

import time
from deta import Deta
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def root():
    return "HomePage EmailBot Eskeree"


#public google sheet url - not secure!
SHEET_ID = "1McHi8LonS6ZAzaXfWvLM6cZEQiOE7lv-CbYPjKu8834"
SHEET_NAME = "Foglio1"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

def load_df(url):
    df = pd.read_csv(url, parse_dates=["DATA_PRIMA_MAIL"],dayfirst=True)
    # print(type(df))
    return df    

df = load_df(URL)
   

def query_data_and_send_emails(df):
    present = date.today()
    email_counter = 0
    for _, row in df.iterrows():
        first_mail_date = datetime.strptime(datetime.strftime((row["DATA_PRIMA_MAIL"]).date(), "%d,%m,%y"), "%d,%m,%y").date()        #prima mail
        if (present == first_mail_date):
            send_email(
                
                email_receiver = row["EMAIL"],
                gym_name=row["NOME"],
                gym_owner=row["NOME"],
                subject = 'Domanda al volo',

                body= f"""\
                <html>
                <body>
                    <p>Salve {row["NOME"]}, tutto bene?</p>
                    <p>Sarò diretto, ho controllato la vostra palestra su internet e sarebbe bello lavorare con voi: vi sto rubando del tempo per dirvi che vi aiuteremmo ad avere nuovi clienti. (sempre se ne avete davvero bisogno).</p>
                    <p></p>
                    <p>Senza dilungarmi inutilmente, avrete nuova clientela a fine del servizio (circa 3 mesi).</p>
                    <p>Acquisiamo i contatti e li tramutiamo in clienti, in maniera automatica.</p>
                    <p></p>
                    <p>La parte più bella è che se non siete soddisfatti del servizio, vi rimborsiamo. Veniamo pagati solo se voi avete nuovi clienti e siete contenti. Alla fine il nostro successo dipende dal vostro.</p>
                    <p></p>
                    <p>Ho un sistema specifico per ottenere questi risultati e sarei davvero contento se avessi l'opportunità di mostrare come funziona, magari in una videochiamata. 
                    <p>Vi piacerebbe l’idea di programmare questa chiamata, senza impegno, anche questa settimana? Se avete spazio per nuovi clienti ovviamente!</p>
                    <p><strong>Paolo Ligori</strong></p>
                    <p><strong>Tel 0621701576</strong></p>
                    <p><strong>atvertextop@gmail.com</strong></p>
                </body>
                </html>
                """
            )
            email_counter+=1

        #1 follow up email
        elif (present == (first_mail_date + timedelta(1))) and (row["REPLIED"] == "NO"):
            send_email(
                email_receiver = row["EMAIL"],
                gym_name=row["NOME"],
                gym_owner=row["NOME"],
                subject = 'Eccoci', 

                body_html = f"""\
                <html>
                  <body>
                    <p>Ciao {row["NOME"]}, come va?</p>
                    <p>I hope you are well.</p>
                    <p>Credo che non ha ancora controllato la prima mail che avevo mandato, spero che possa esservi utile, aspetto risposta!</p>
                    <p></p>
                    <p></p>
                    <p><strong>Paolo Ligori</strong></p>
                    <p><strong>Tel 0621701576</strong></p>
                    <p><strong>atvertextop@gmail.com</strong></p>
                  </body>
                </html>
                """
            )
            email_counter+=1
        #2 follow up email
        elif (present == (first_mail_date + timedelta(3))) and (row["REPLIED"] == "NO"):
            send_email(
                email_receiver = row["EMAIL"],
                gym_name=row["NOME"],
                gym_owner=row["NOME"],
                subject = 'informazione per '+ row["NOME"],

                body = f"""\
                <html>
                  <body>
                    <p>Ciao {row["NOME"]}, tutto bene?</p>
                    <p></p>
                    <p>Oltre al caldo torrido mi ci metto anch'io a infastidirla (sperando di no)!</p>
                    <p>Resto qui a sua disposizione!</p>
                    <p></p>
                    <p><strong>Paolo Ligori</strong></p>
                    <p><strong>Tel 0621701576</strong></p>
                    <p><strong>atvertextop@gmail.com</strong></p>
                  </body>
                </html>
                """
            )
            email_counter+=1
        #3 follow up email
        elif (present == (first_mail_date + timedelta(5))) and (row["REPLIED"] == "NO"):
            send_email(
                email_receiver = row["EMAIL"],
                gym_name=row["NOME"],
                gym_owner=row["NOME"],
                subject = 'Sfruttiamo la situazione a nostro vantaggio!',

                body = f"""\
                <html>
                  <body>
                    <p>Ciao {row["NOME"]},</p>
                    <p></p>
                    <p>sono ancora convinto che potremmo lavorare molto bene insieme, perciò voglio insistere chiedendole gentilmente se è interessato a leggere la prima mail che abbiamo inviato</p>
                    <p>Resto qui a sua disposizione!</p>
                    <p>Grazie</p>
                    <p><strong>Paolo Ligori</strong></p>
                    <p><strong>Tel 0621701576</strong></p>
                    <p><strong>atvertextop@gmail.com</strong></p>
                  </body>
                </html>
                """
            )
            email_counter+=1
        #4 follow up email
        elif (present == (first_mail_date + timedelta(7))) and (row["REPLIED"] == "NO"):
            send_email(
                email_receiver = row["EMAIL"],
                gym_name=row["NOME"],
                gym_owner=row["NOME"],
                subject = 'ma...',

                body = f"""\
                <html>
                  <body>
                    <p>Ciao {row["NOME"]},</p>
                    <p>è passato un pò di tempo, spero che abbia avuto modo di dare un’ occhiata alla mail.</p>
                    <p>Voglio solo assicurarmi che da ambo le parti non perdiamo un'ottima occasione per migliorare le nostre attività.</p>
                    <p></p>
                    <p>Grazie</p>
                    <p><strong>Paolo Ligori</strong></p>
                    <p><strong>Tel 0621701576</strong></p>
                    <p><strong>atvertextop@gmail.com</strong></p>
                  </body>
                </html>
                """
            )
            email_counter+=1

    return f"Total emails sent: {email_counter}"


@app.post('/__space/v0/actions')
async def actions(request: Request):
    data = await request.json()
    event = data.get('event')
    if not event or not isinstance(event, dict) or not isinstance(event.get('id'), str):
        return {"error": "Invalid data format in 'event' field."}

    if event['id'] == 'check_send':
        df = load_df(URL)
        result = query_data_and_send_emails(df)
        print(result)
        return result
    

    return {"message": "Action not recognized."}


df = load_df(URL)
result = query_data_and_send_emails(df)
print(result)
    
