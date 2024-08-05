import json

from openai import OpenAI


def elencoLezioni(its, grado, indirizzo, contesto, client):

    linee_guida = open("linee_guida", "r").read()
    elencoUda = open("elencoUDA.json", "r").read()
    dettaglioUda = open("dettaglioUDA.json", "r").read()
    formato_output = open("formato_output_elenco_lezioni", "r").read()
    role_system = "Agisci da esperto docente di Informatica negli "+its +". \ "+linee_guida+" Il tuo compito è fornire il dettaglio dell’Unità didattica di Apprendimento che ti fornirò nell’ambito della progettazione didattica per la disciplina Informatica, in linea con le indicazioni nazionali."+formato_output
    contesto_classe = "### ANALISI PROFILO CLASSE \ " + contesto + "### ANNO DI RIFERIMENTO \ " + grado + " ad indirizzo " + indirizzo + ". \ PROGETTAZIONE: \ "
    role_user = "Io ti fornirò l'analisi del profilo della classe e l'anno di riferimento, l'elenco delle UDA, la UDA di riferimento, e tuo restituirai il dettaglio dell’unità didattica di apprendimento per la Progettazione Disciplinare nel formato richiesto. \ "+contesto_classe+elencoUda+"### UNITA’ DIDATTICA \
    Introduzione ai Sistemi Informativi Aziendali \ "+dettaglioUda+"### PERIODO \
    Settembre-Ottobre \
    ### NUMERO DI ORE SETTIMANALI \
    4 \
    ### TOTALE ORE ANNO SCOLASTICO \
    132 \
    ELENCO LEZIONI: \
    "

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

    lezioni_path = 'elencoLezioni.json'
    with open(lezioni_path, 'w', encoding='utf-8') as json_file:
        json.dump(response_data, json_file, ensure_ascii=False, indent=2)

    print(f"La risposta è stata salvata in {lezioni_path}")


