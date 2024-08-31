import json

from openai import OpenAI
# Directly assign the API key
OPENAI_API_KEY = 'sk-proj-bnV3OzNQN8aN9lT5btYqT3BlbkFJo6uSRw6mM4jKYGOO2D7w'
client = OpenAI(api_key=OPENAI_API_KEY)

school_type = "Istituti Tecnici Settore Economico. \ "
linee_guida = open("linee_guida", "r").read()
elencoUda = open("elencoUDA.json", "r").read()
dettaglioUda = open("dettaglioUDA.json", "r").read()
formato_output = open("formato_output_slides", "r").read()
elencoLezioni = open("elencoLezioni.json", "r").read()
dettaglioLezione = open("lezione.json", "r").read()
role_system = "Agisci da esperto docente di Informatica negli Istituti Tecnici Settore Economico. \ "+school_type+linee_guida+"Il tuo compito è fornire il dettaglio della lezione che ti fornirò nell’ambito della progettazione didattica per la disciplina Informatica, in linea con le indicazioni nazionali."
contesto_classe=open("contesto_classe", "r").read()
elenco_UDA = open("elencoUDA.json", "r").read()
role_user = "Io ti fornirò l'analisi del profilo della classe e l'anno di riferimento, l'elenco delle UDA, la UDA di riferimento, dettaglio dell'UDA, l'elenco delle lezioni, il dettaglio della lezione  e tuo restituirai le slide per la Progettazione Disciplinare. \ "+contesto_classe+elencoUda+"### UNITA’ DIDATTICA \
Introduzione ai Sistemi Informativi Aziendali \ "+dettaglioUda+"### PERIODO \
Settembre-Ottobre \
### NUMERO DI ORE SETTIMANALI \
4 \
### TOTALE ORE ANNO SCOLASTICO \
132 \
"+ elencoLezioni+"### LEZIONE \
Introduzione ai Sistemi Informativi Aziendali \
DETTAGLIO LEZIONE: \ " + dettaglioLezione + "SLIDES: \ "


completion = client.chat.completions.create(
  model="gpt-4.0",
  messages=[
    {"role": "system", "content": role_system

        },
    {"role": "user", "content": role_user
        }
  ]
)


# Estrarre la risposta testuale dall'oggetto completion
response_text = completion.choices[0].message.content

# Salvataggio della risposta in un file JSON

slides_path = 'slides_without_json'
f = open(slides_path, 'w')
f.write(response_text)
f.close()

print(f"La risposta è stata salvata in {slides_path}")


