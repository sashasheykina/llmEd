import json

from openai import OpenAI
# Directly assign the API key
OPENAI_API_KEY = 'sk-proj-bnV3OzNQN8aN9lT5btYqT3BlbkFJo6uSRw6mM4jKYGOO2D7w'
client = OpenAI(api_key=OPENAI_API_KEY)

school_type = "Istituti Tecnici Settore Economico. \ "
linee_guida = open("linee_guida", "r").read()
elencoUda = open("elencoUDA.json", "r").read()
formato_output = open("formato_output_dettaglioUda", "r").read()
role_system = "Agisci da esperto docente di Informatica negli Istituti Tecnici Settore Economico. \ "+school_type+linee_guida+"Il tuo compito è fornire il dettaglio dell’Unità didattica di Apprendimento che ti fornirò nell’ambito della progettazione didattica per la disciplina Informatica, in linea con le indicazioni nazionali."+formato_output
contesto_classe=open("contesto_classe", "r").read()
role_user = "Io ti fornirò l'analisi del profilo della classe e l'anno di riferimento, l'elenco delle UDA, la UDA di riferimento, e tuo restituirai il dettaglio dell’unità didattica di apprendimento per la Progettazione Disciplinare nel formato richiesto. \ "+contesto_classe+elencoUda+"### UDA \
Introduzione ai Sistemi Informativi Aziendali \
DETTAGLIO UDA: \
"
elenco_UDA = open("elencoUDA.json", "r").read()
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": role_system

        },
    {"role": "user", "content": role_user
        }
  ]
)


# Estrarre la risposta testuale dall'oggetto completion
response_text = completion.choices[0].message.content

# Convertire il testo JSON in un oggetto Python
response_data = json.loads(response_text)

# Salvataggio della risposta in un file JSON

dettaglio_path = 'dettaglioUDA.json'
with open(dettaglio_path, 'w', encoding='utf-8') as json_file:
    json.dump(response_data, json_file, ensure_ascii=False, indent=2)

print(f"La risposta è stata salvata in {dettaglio_path}")


