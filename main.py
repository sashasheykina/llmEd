import json
import re
from openai import OpenAI

def elencoUDA(its, grado, indirizzo, contesto, client):


    linee_guida = open("linee_guida", "r").read()
    formato_output = open("formato_output_elencoUda", "r").read()
    role_system = "Agisci da esperto docente di Informatica negli "+its +". \ "+linee_guida+" Il tuo compito è fornire la progettazione didattica per la disciplina Informatica, in linea con le indicazioni nazionali."+formato_output
    contesto_classe = "### ANALISI PROFILO CLASSE \ " +contesto +"### ANNO DI RIFERIMENTO \ "+ grado + " ad indirizzo " + indirizzo +". \ PROGETTAZIONE: \ "
    role_user = "Io ti fornirò l'analisi del profilo della classe e l'anno di riferimento, e tuo restituirai la Progettazione Disciplinare nel formato richiesto JSON. \ "+contesto_classe
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": role_system},
            {"role": "user", "content": role_user}
        ]
    )

    response_text = completion.choices[0].message.content

    # Pulire la risposta per trovare solo il JSON
    json_start = response_text.find('{')
    json_end = response_text.rfind('}') + 1

    if json_start != -1 and json_end != -1:
        json_text = response_text[json_start:json_end]

        try:
            response_data = json.loads(json_text)
            # Salvataggio della risposta in un file JSON
            elenco_path = 'elencoUDA.json'
            with open(elenco_path, 'w', encoding='utf-8') as json_file:
                json.dump(response_data, json_file, ensure_ascii=False, indent=2)

            print(f"La risposta è stata salvata in {elenco_path}")
        except json.JSONDecodeError as e:
            print("Errore nel decodificare il JSON:", e)
            print("Contenuto JSON estratto:", json_text)
    else:
        print("Errore: non è stato possibile individuare un blocco JSON valido nella risposta.")
        print("Contenuto della risposta:", response_text)