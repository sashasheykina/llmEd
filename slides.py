import json

from openai import OpenAI

def genSlides(its, grado, indirizzo, contesto, client):

    linee_guida = open("linee_guida", "r").read()
    elencoUda = open("elencoUDA.json", "r").read()
    dettaglioUda = open("dettaglioUDA.json", "r").read()
    formato_output = open("formato_output_slides", "r").read()
    elencoLezioni = open("elencoLezioni.json", "r").read()
    dettaglioLezione = open("lezione.json", "r").read()
    role_system = "Agisci da esperto docente di Informatica negli "+its +". \ "+linee_guida+" Il  tuo compito è fornire il dettaglio della lezione che ti fornirò nell’ambito della progettazione didattica per la disciplina Informatica, in linea con le indicazioni nazionali."+formato_output
    contesto_classe = "### ANALISI PROFILO CLASSE \ " + contesto + "### ANNO DI RIFERIMENTO \ " + grado + " ad indirizzo " + indirizzo + ". \ PROGETTAZIONE: \ "
    role_user = "Io ti fornirò l'analisi del profilo della classe e l'anno di riferimento, l'elenco delle UDA, la UDA di riferimento, dettaglio dell'UDA, l'elenco delle lezioni, il dettaglio della lezione  e tuo restituirai le slide per la Progettazione Disciplinare nel formato richiesto. \ "+contesto_classe+elencoUda+"### UNITA’ DIDATTICA \
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

    slides_path = 'slides.json'
    with open(slides_path, 'w', encoding='utf-8') as json_file:
        json.dump(response_data, json_file, ensure_ascii=False, indent=2)

    print(f"La risposta è stata salvata in {slides_path}")


