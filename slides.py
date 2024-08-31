import json

from openai import OpenAI

def genSlides(its, grado, indirizzo, contesto, docente, client):

    linee_guida = open("linee_guida", "r").read()
    elencoUda = open("elencoUDA.json", "r").read()
    dettaglioUda = open("dettaglioUDA.json", "r").read()
    formato_output = open("formato_output_slides", "r").read()
    elencoLezioni = open("elencoLezioni.json", "r").read()
    dettaglioLezione = open("lezione.json", "r").read()
    role_system = "Agisci da esperto docente di Informatica negli "+its +". \ "+linee_guida+" Il  tuo compito è fornire il dettaglio della lezione che ti fornirò nell’ambito della progettazione didattica per la disciplina Informatica, in linea con le indicazioni nazionali."+formato_output
    contesto_classe = "### ANALISI PROFILO CLASSE \ " + contesto + "### ANNO DI RIFERIMENTO \ " + grado + " ad indirizzo " + indirizzo + "Nome docente: "+ docente+". \ PROGETTAZIONE: \ "
    role_user = "Io ti fornirò l'analisi del profilo della classe e l'anno di riferimento, l'elenco delle UDA, la UDA di riferimento, dettaglio dell'UDA, l'elenco delle lezioni, il dettaglio della lezione  e tuo restituirai 25 slide per una presentazione Power Point per la Progettazione Disciplinare nel formato richiesto. \ "+contesto_classe+elencoUda+"### UNITA’ DIDATTICA \
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
            elenco_path = 'slides.json'
            with open(elenco_path, 'w', encoding='utf-8') as json_file:
                json.dump(response_data, json_file, ensure_ascii=False, indent=2)

            print(f"La risposta è stata salvata in {elenco_path}")
        except json.JSONDecodeError as e:
            print("Errore nel decodificare il JSON:", e)
            print("Contenuto JSON estratto:", json_text)
    else:
        print("Errore: non è stato possibile individuare un blocco JSON valido nella risposta.")
        print("Contenuto della risposta:", response_text)