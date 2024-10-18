from datetime import datetime
import json
import streamlit as st



def aggiorna_elencoUDA():
    # Carica i dati dal file JSON
    with open('elencoUDA.json', 'r') as f:
        data = json.load(f)

    # Estrai le "UDA" in una lista
    elencoUda = [unita["UDA"] for unita in data["Unita Didattiche"]]
    # Aggiorna la lista di UDA nello stato della sessione
    st.session_state.uda_options = elencoUda  # Questo aggiornerà il selectbox automaticamente
    # Forza Streamlit a ricaricare l'interfaccia con i nuovi dati

def aggiorna_elencoContenuti():
    # Carica i dati dal file JSON
    with open('elencoContenuti.json', 'r') as f:
        data = json.load(f)

        # Estrai le "UDA" in una lista
    elencoContenuti = [unita["Tipologia"] for unita in data["tipologie_delle_lezioni"]]

    # Aggiorna la lista di UDA nello stato della sessione
    st.session_state.struttura = elencoContenuti  # Questo aggiornerà il selectbox automaticamente

def aggiorna_elencoAttivita():

    # Apri e carica il file JSON
    with open('struttura_lezione.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    elencoAttivita = []
    # Itera sui materiali didattici e strumenti
    for item in data["Materiale didattico e strumenti utilizzati durante la lezione"]:
        elencoAttivita.append(f'{item["materiale_didattico"]} ({item["strumento"]})')

    # Aggiorna la lista di UDA nello stato della sessione
    st.session_state.contenuto = elencoAttivita

def aggiorna_elencoLezioni():
    # Carica i dati dal file JSON
    with open('elencoLezioni.json', 'r') as f:
        data = json.load(f)

    # Estrai le "UDA" in una lista
    elencoLezioni = [unita["Lezione"] for unita in data["Lezioni"]]

    # Aggiorna la lista di UDA nello stato della sessione
    st.session_state.lezione_options = elencoLezioni

def lineeGuida(art, disciplina):
    linee_guida = open("LINEE GUIDA/afm_rim_informatica", "r").read()
    if art == 'Relazioni internazionali per il Marketing':
        if disciplina == 'Tecnologie della comunicazione':
            linee_guida = open("LINEE GUIDA/afm_rim_tdc", "r").read()
    if art == 'Grafica e Comunicazione':
        if disciplina == 'Progettazione multimediale':
            linee_guida = open("LINEE GUIDA/gec_pm", "r").read()
    if art == 'Sistemi informativi aziendali':
        if disciplina == 'Informatica':
            linee_guida = open("LINEE GUIDA/afm_sia_informatica", "r").read()
    if art == 'Informatica':
        if disciplina == 'Sistemi e reti':
            linee_guida = open("LINEE GUIDA/iet_i_ser", "r").read()
        elif disciplina == 'Tecnologie e progettazione di sistemi informatici e di telecomunicazioni':
            linee_guida = open("LINEE GUIDA/iet_i_tpsit", "r").read()
        elif disciplina == 'Gestione progetto, organizzazione di inpresa':
            linee_guida = open("LINEE GUIDA/iet_i_gpoi", "r").read()
        elif disciplina == 'Informatica':
            linee_guida = open("LINEE GUIDA/iet_i_inf", "r").read()
        elif disciplina == 'Telecomunicazioni':
            linee_guida = open("LINEE GUIDA/iet_i_tel", "r").read()
    if art == 'Telecomunicazioni':
        if disciplina == 'Sistemi e reti':
            linee_guida = open("LINEE GUIDA/iet_t_ser", "r").read()
        elif disciplina == 'Tecnologie e progettazione di sistemi informatici e di telecomunicazioni':
            linee_guida = open("LINEE GUIDA/iet_t_tpsit", "r").read()
        elif disciplina == 'Gestione progetto, organizzazione di inpresa':
            linee_guida = open("LINEE GUIDA/iet_t_gpoi", "r").read()
        elif disciplina == 'Informatica':
            linee_guida = open("LINEE GUIDA/iet_t_inf", "r").read()
        elif disciplina == 'Telecomunicazioni':
            linee_guida = open("LINEE GUIDA/iet_t_tel", "r").read()
    return linee_guida

def periodoUda(uda_name):
    data = open("elencoUDA.json", "r").read()
    # Carica il JSON
    miaUda = json.loads(data)
    for uda in miaUda['Unita Didattiche']:
        if uda['UDA'] == uda_name:
            return uda['Periodo']
    return "UDA non trovata."

def elencoLezioni(its, grado, indirizzo, disciplina, uda, periodo, ore_anno, ore_sett, contesto, client):
    elencoUda = open("elencoUDA.json", "r").read()
    dettaglioUda = open("dettaglioUDA.json", "r").read()
    formato_output = open("formato_output_elenco_lezioni", "r").read()
    griglia = open("griglia_valutazione.json", "r").read()
    livello = open("livello_competenze.json", "r").read()
    valutazioni = open("valutazioni", "r").read()
    role_system = (
        f"Agisci da esperto docente di Informatica negli {its}. Il tuo compito è fornire l’elenco delle lezioni da attivare per una specifica Unità didattica di Apprendimento che ti fornirò nell’ambito della progettazione didattica. "
        f"per la disciplina {disciplina}. Dovrai fornire la progettazione tramite un JSON strutturato come segue: {formato_output}."
    )
    contesto_classe = (
        f"### ANALISI PROFILO CLASSE {contesto}. ### GRADO CLASSE  {grado}. ad indirizzo {indirizzo}."
    )
    role_user = (
        f"Io ti fornirò il file json che contiene uda, l'analisi del profilo della classe, l'anno di riferimento, l'elenco delle UDA, la UDA di riferimento, il dettaglio unità didattica, priodo di svolgimento, ore setiimanali, monte ore annuo, livello competenze, griglia di valutazione, la lista di possibili valutazioni da adottare e tuo restituirai l’elenco "
        f"delle lezioni per la Progettazione Disciplinare nel formato richiesto. ### CONTESTO CLASSE {contesto_classe}. ### ELENCO UNITA’ DIDATTICA: {elencoUda}. ### UNITA’ DIDATTICA {uda} ### DETTAGLIO UNITA’ DIDATTICA {dettaglioUda}. "
        f"### PERIODO {periodo}. ### NUMERO DI ORE SETTIMANALI {str(ore_sett)}. ### TOTALE ORE ANNO SCOLASTICO {str(ore_anno)}. ### LIVELLO COMPETENZE {livello}. ### GRIGLIA DI VALUTAZIONE {griglia}. ###VALUTAZIONI {valutazioni}"
        f"ELENCO LEZIONI: "
    )

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": role_system},
            {"role": "user", "content": role_user}
        ]
    )

    # Estrarre la risposta testuale dall'oggetto completion
    response_text = completion.choices[0].message.content

    # Pulire la risposta per trovare solo il JSON
    json_start = response_text.find('{')
    json_end = response_text.rfind('}') + 1

    if json_start != -1 and json_end != -1:
        json_text = response_text[json_start:json_end]

        try:
            response_data = json.loads(json_text)
            # Salvataggio della risposta in un file JSON
            elenco_path = 'elencoLezioni.json'
            with open(elenco_path, 'w', encoding='utf-8') as json_file:
                json.dump(response_data, json_file, ensure_ascii=False, indent=2)

            print(f"La risposta è stata salvata in {elenco_path}")
        except json.JSONDecodeError as e:
            print("Errore nel decodificare il JSON:", e)
            print("Contenuto JSON estratto:", json_text)
    else:
        print("Errore: non è stato possibile individuare un blocco JSON valido nella risposta.")
        print("Contenuto della risposta:", response_text)

def dettaglioUDA(its, grado, indirizzo, linee_guida, disciplina, uda, contesto, docente, ore_sett, ore_anno, client):

    elencoUda = open("elencoUDA.json", "r").read()
    formato_output = open("formato_output_dettaglioUda", "r").read()
    metodologie = open("metodologie_didattiche", "r").read()
    valutazioni = open("valutazioni", "r").read()
    strumenti = open("sussidi_didattici.json", "r").read()
    esperienze = open("esperienze_attivate", "r").read()
    os = str(ore_sett)
    oa = str(ore_anno)
    response_data = None
    elenco_path = 'dettaglioUDA.json'
    role_system = (
            f"Agisci da esperto docente di Informatica negli {its}. {linee_guida} "
            f"Il tuo compito è fornire il dettaglio dell’Unità didattica di Apprendimento che ti fornirò nell’ambito della progettazione didattica per la disciplina {disciplina}, "
            f"in linea con le indicazioni nazionali. Dovrai fornire la Progettazione Disciplinare tramite un JSON strutturato come segue: {formato_output}"
    )
    contesto_classe = (
        f"### ANALISI PROFILO CLASSE \ {contesto}. ### GRADO CLASSE \ {grado} ad indirizzo {indirizzo}. "
    )
    role_user = (
            f"Io ti fornirò l'analisi del profilo della classe e l'anno di riferimento, numero ore settimanali, monte ore annuo, nome docente, l'elenco delle UDA, la UDA di riferimento, metodologie da applicare, "
            f"il materiale didattico da utilizzare per la metodologia applicata, esperienze attivate, tipi di valutazioni e tuo restituirai il dettaglio dell’unità didattica di apprendimento "
            f"per la Progettazione Disciplinare nel formato richiesto. \ ### CONTESTO CLASSE {contesto_classe} \ ### NUMERO ORE SETTIMANALI {os} "
            f"### TOTALE ORE ANNO {oa}. \ ### DOCENTE: {docente}. \ ### ELENCO UDA: {elencoUda} \ ### UDA: {uda}. \ ### METODOLOGIE {metodologie} "
            f"### MATERIALE DIDATTICO {strumenti}. ### ESPERIENZE ATTIVATE {esperienze}. ### TIPI DI VALUTAZIONE: {valutazioni}. " 
            f"DETTAGLIO UDA: "
    )

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": role_system},
            {"role": "user", "content": role_user}
        ]
    )

    # Estrarre la risposta testuale dall'oggetto completion
    response_text = completion.choices[0].message.content

    # Stampa di debug per visualizzare la risposta originale
    #print("Risposta originale:", response_text)

    # Se necessario, pulisci il contenuto per estrarre solo il JSON valido
    json_start = response_text.find('{')
    json_end = response_text.rfind('}') + 1

    if json_start != -1 and json_end != -1:
        cleaned_json_text = response_text[json_start:json_end]
        #print(cleaned_json_text)

        try:
            response_data = json.loads(cleaned_json_text)
            # Salvataggio della risposta in un file JSON
            with open(elenco_path, 'w', encoding='utf-8') as json_file:
                json.dump(response_data, json_file, ensure_ascii=False, indent=2)

            print(f"La risposta è stata salvata in {elenco_path}")
        except json.JSONDecodeError as e:
            print("Errore nel decodificare il JSON:", e)
            print("Contenuto JSON estratto:", cleaned_json_text)
    else:
        print("Errore: non è stato possibile individuare un blocco JSON valido nella risposta.")
        print("Contenuto della risposta:", response_text)
    return response_data

'''
    response_data = None  # Inizializza response_data
    # Convertire in un oggetto Python
    try:
        response_data = json.loads(cleaned_json_text)

    except json.JSONDecodeError as e:
        # Stampa l'errore e la posizione
        print(f"Errore nella decodifica JSON: {e}")
        print("JSON problematica:", cleaned_json_text)

        # Aggiungi ulteriori controlli per trovare il problema
        for i, line in enumerate(cleaned_json_text.splitlines()):
            print(f"Riga {i + 1}: {line}")'''

def elencoUDA(its, grado, indirizzo, linee_guida, disciplina, contesto, client):

    formato_output = open("formato_output_elencoUda", "r").read()
    role_system = (
            f"Agisci da esperto docente di Informatica negli {its}. {linee_guida} "
            f"Il tuo compito è fornire la progettazione didattica per la disciplina {disciplina}, "
            f"in linea con le indicazioni nazionali. Dovrai fornire la progettazione tramite un JSON strutturato come segue: {formato_output}"
    )
    contesto_classe = (
            f"### ANALISI PROFILO CLASSE \ {contesto}. ### GRADO CLASSE DI RIFERIMENTO \ {grado} ad indirizzo {indirizzo}. PROGETTAZIONE: \ "
         )
    role_user = (
            f"Io ti fornirò l'analisi del profilo della classe e il grado classe di riferimento, "
            f"e tu restituirai la Progettazione Disciplinare nel formato richiesto JSON. {contesto_classe} "
            f"ELENCO UDA: "
    )

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": role_system},
            {"role": "user", "content": role_user}
        ],
    )

    response_text = completion.choices[0].message.content

    # Pulire la risposta per trovare solo il JSON
    json_start = response_text.find('{')
    json_end = response_text.rfind('}') + 1

    if json_start != -1 and json_end != -1:
        json_text = response_text[json_start:json_end]
        #print(json_text)

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

def genera_PDC(its, grado, indirizzo, articolazione, linee_guida, disciplina, contesto, docente, ore_sett, ore_anno, client):


    # Carica l'elenco delle UDA dal file JSON
    with open("elencoUDA.json", "r", encoding="utf-8") as f:
        elenco_uda = json.load(f)
        # Recupera il valore associato alla chiave "BES"
        valore_bes = elenco_uda.get("BES/DSA", None)  # Restituisce None se "BES" non esiste

    current_year = datetime.now().year
    anno = str(current_year)+"/"+str(current_year+1)
    dettagli_path = 'progettazione_didattica.json'
    try:
        with open(dettagli_path, 'w', encoding='utf-8') as json_file:
            dati = {
                "ordinamento scuola": "Scuola secondaria di II grado",
                "tipo scuola": its,
                "grado": grado,
                "indirizzo": indirizzo,
                "articolazione": articolazione,
                "disciplina": disciplina,
                "contesto": contesto,
                "docente": docente,
                "anno_scolastico": anno,
                "ore_settimanali": ore_sett,
                "ore_annue": ore_anno,
                "BES": valore_bes,
                "Unita Didattiche": []
            }
            json.dump(dati, json_file, ensure_ascii=False, indent=4)
        print(f"Dati scritti con successo nel file '{dettagli_path}'.")
    except Exception as e:
        print(f"Si è verificato un errore durante la scrittura nel file: {e}")

    # Itera su ciascuna UDA e genera il dettaglio
    for uda in elenco_uda["Unita Didattiche"]:
        dettaglio = None
        print("#################################################")
        dettaglio = dettaglioUDA(its, grado, indirizzo,  linee_guida, disciplina, uda, contesto, docente, ore_sett, ore_anno, client)
        print("QUESTO é IL DETTAGLIO GENERATO:"+str(dettaglio))
        print("#################################################")
        update_file_progettazione_didattica(dettaglio)

def update_file_progettazione_didattica(response_text):

    nome_file = 'progettazione_didattica.json'
    # Leggi il file JSON esistente
    try:
        with open(nome_file, 'r', encoding='utf-8') as file_json:
            dati = json.load(file_json)

            # Controlla che "Unita Didattiche" sia una lista
            if "Unita Didattiche" in dati and isinstance(dati["Unita Didattiche"], list):
                # Aggiungi il nuovo dato alla lista "Unita Didattiche"
                dati["Unita Didattiche"].append(response_text)
            else:
                print("Errore: 'Unita Didattiche' non è una lista o non esiste.")
                return
    except FileNotFoundError:
        print(f"Errore: il file '{nome_file}' non è stato trovato.")
        return
    except json.JSONDecodeError:
        print("Errore nella decodifica del file JSON.")
        return

    # Scrivi il file JSON aggiornato
    with open(nome_file, 'w', encoding='utf-8') as file_json:
        json.dump(dati, file_json, ensure_ascii=False, indent=4)

    print(f"File JSON '{nome_file}' aggiornato con successo.")

def elencoContenuti(its, grado, indirizzo, disciplina, lezione, client):

    contenuti = open("tipologie_lezioni", "r").read()
    elencoUda = open("elencoUDA.json", "r").read()
    dettaglioUda = open("dettaglioUDA.json", "r").read()
    elencoLezioni = open("elencoLezioni.json", "r").read()
    formato_output = open("formato_output_elenco_contenuti", "r").read()

    role_system = (
        f"Agisci da esperto docente di Informatica negli {its}."
        f"Il tuo compito è fornire la progettazione didattica per la disciplina {disciplina}. Dovrai fornire la progettazione tramite un JSON strutturato come segue: {formato_output}"
    )
    contesto_classe = (
        f"### ANALISI PROFILO CLASSE ### GRADO CLASSE DI RIFERIMENTO \ {grado} ad indirizzo {indirizzo}. PROGETTAZIONE: \ "
    )
    role_user = (
        f"Io ti fornirò elenco unità didattiche, dettaglio unita didattica di riferimento, elenco lezioni, la lezione, tipologie delle lezioni, l'analisi del profilo della classe, "
        f"e tu restituirai elenco dei possibili tipi di lezioni da adottare per la lezione specifica nella Progettazione Disciplinare nel formato richiesto JSON. ### ELENCO UDA: {elencoUda}. "
        f"### DETTAGLIO UDA: {dettaglioUda}. ### ELENCO LEZIONI: {elencoLezioni}. ### LEZIONIE: {lezione}. ### POSSIBILI TIPOLOGIE DI LEZIONE {contenuti}. ### CONTESTO CLASSE {contesto_classe}. "
        f"ELENCO TIPOLOGIE LEZIONI: "
    )

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": role_system},
            {"role": "user", "content": role_user}
        ],
    )

    response_text = completion.choices[0].message.content

    # Pulire la risposta per trovare solo il JSON
    json_start = response_text.find('{')
    json_end = response_text.rfind('}') + 1

    if json_start != -1 and json_end != -1:
        json_text = response_text[json_start:json_end]
        # print(json_text)

        try:
            response_data = json.loads(json_text)
            # Salvataggio della risposta in un file JSON
            elenco_path = 'elencoContenuti.json'
            with open(elenco_path, 'w', encoding='utf-8') as json_file:
                json.dump(response_data, json_file, ensure_ascii=False, indent=2)

            print(f"La risposta è stata salvata in {elenco_path}")
        except json.JSONDecodeError as e:
            print("Errore nel decodificare il JSON:", e)
            print("Contenuto JSON estratto:", json_text)
    else:
        print("Errore: non è stato possibile individuare un blocco JSON valido nella risposta.")
        print("Contenuto della risposta:", response_text)

def getMaterialeDidattico(uda, lezione, struttura, client):

    current_dateTime = datetime.now()
    materiale = open("sussidi_didattici.json", "r").read()
    elencoLezioni = open("elencoLezioni.json", "r").read()
    griglia = open("griglia_valutazione.json", "r").read()
    livello = open("livello_competenze.json", "r").read()
    valutazioni = open("valutazioni", "r").read()
    date = str(current_dateTime.day) + "/" + str(current_dateTime.month) + "/" + str(current_dateTime.year)
    # Cerca l'unità didattica specifica
    dettaglioUda = None

    try:
        # Apertura sicura del file JSON
        with open("progettazione_didattica.json", 'r', encoding='utf-8') as f:
            dati = json.load(f)

        for unita in dati.get("Unita Didattiche", []):
            if unita.get("UNITA’ DI APPRENDIMENTO") == uda:
                dettaglioUda = unita
                break  # Una volta trovata l'UDA, esci dal ciclo

        if dettaglioUda:
            print(f"Dettaglio dell'UDA '{uda}'")
        else:
            print(f"L'UDA '{uda}' non è stata trovata.")
    except FileNotFoundError:
        print("Errore: Il file 'progettazione_didattica.json' non è stato trovato.")
    except json.JSONDecodeError:
        print("Errore: Il file non è un JSON valido.")
    except Exception as e:
        print(f"Si è verificato un errore: {e}")

    docente = dati.get("docente")
    tipo_scuola = dati.get("tipo scuola")
    indirizzo = dati.get("indirizzo")
    grado = dati.get("grado")
    contesto = dati.get("contesto")
    disciplina = dati.get("disciplina")
    periodo = dati.get("anno_scolastico")
    ore_anno = dati.get("ore_annue")
    ore_sett = dati.get("ore_settimanali")
    formato_output = None
    elenco_path = 'struttura_lezione.json'

    if struttura == 'Discussione guidata':
        formato_output = open("formato_output_DiscussioneGuidata", "r").read()
    elif struttura == "Lezione frontale":
        formato_output = open("formato_output_LezioneFrontale", "r").read()
    elif struttura == "Case Study":
        formato_output = open("formato_output_CaseStudy", "r").read()
    elif struttura == "Laboratorio pratico":
        formato_output = open("formato_output_LaboratorioPratico", "r").read()
    elif struttura == "Lavoro di gruppo":
        formato_output = open("formato_output_LavoroDiGruppo", "r").read()
    elif struttura == "Verifica scritta":
        formato_output = open("formato_output_VerificaScritta", "r").read()
    elif struttura == "Presentazione progetto":
        formato_output = open("formato_output_PresentazioneProgetto", "r").read()
    elif struttura == "Flipped classroom":
        formato_output = open("formato_output_FlippedClassroom", "r").read()
    else:
        st.warning('Non è previsto il materiale diadattico per questa tipologia di lezione', icon="⚠️")
        return

    role_system = (
        f"Agisci da esperto docente di Informatica negli {tipo_scuola}. "
        f"Il tuo compito è fornire la struttura della lezione che ti darò nell’ambito della progettazione didattica per la disciplina {disciplina}. "
        f"Dovrai fornire la progettazione tramite un JSON strutturato come segue: {formato_output}"
    )
    contesto_classe = (
        f"### ANALISI PROFILO CLASSE {contesto} ### ANNO DI RIFERIMENTO {grado} ad indirizzo {indirizzo} ### PROGETTAZIONE: "
    )
    role_user = (
        f"Io ti fornirò l'analisi del profilo della classe, la data di oggi, la UDA di riferimento, deattaglio UDA, elenco lezioni, periodo,"
        f"totale ore settimanali, monte ore annuo, lezione di riferimento, nome docente, il materiale didattico da utilizzare per la metodologia applicata e tuo restituirai la lezione per la Progettazione Disciplinare nel formato richiesto. "
        f"### CONTESTO CLASSE: {contesto_classe}. ### DATA DI OGGI: {date}. ### UNITA’ DIDATTICA {uda}. ### DETTAGLIO UNITA’ DIDATTICA {dettaglioUda}. ### ELENCO LEZIONI {elencoLezioni}. ### ANNO SCOLASTICO {periodo}. ### NUMERO DI ORE SETTIMANALI {str(ore_sett)}"
        f"### TOTALE ORE ANNO SCOLASTICO {str(ore_anno)}. ### LEZIONE {lezione} ### NOME DOCENTE {docente}. ### MATERIALE DIDATTICO {materiale} "
        f"LEZIONE:"
    )

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": role_system},
            {"role": "user", "content": role_user}
        ]
    )

    response_text = completion.choices[0].message.content
    print(response_text)
    # Pulire la risposta per trovare solo il JSON
    json_start = response_text.find('{')
    json_end = response_text.rfind('}') + 1

    if json_start != -1 and json_end != -1:
        json_text = response_text[json_start:json_end]

        try:
            response_data = json.loads(json_text)
            # Salvataggio della risposta in un file JSON
            with open(elenco_path, 'w', encoding='utf-8') as json_file:
                json.dump(response_data, json_file, ensure_ascii=False, indent=2)

            print(f"La risposta è stata salvata in {elenco_path}")
        except json.JSONDecodeError as e:
            print("Errore nel decodificare il JSON:", e)
            print("Contenuto JSON estratto:", json_text)
    else:
        print("Errore: non è stato possibile individuare un blocco JSON valido nella risposta.")
        print("Contenuto della risposta:", response_text)

def creaContenuto(tipo_scuola, disciplina, lezione, contenuto, client):


    formato_output = None

    if "Presentazioni" in contenuto:
        formato_output = open("formato_output_DiscussioneGuidata", "r").read()
        print(contenuto)
    elif "Mappe Concettuali" in contenuto:
        formato_output = open("formato_output_mconcettuale", "r").read()
        print(contenuto)
    elif "Quiz" in contenuto:
        formato_output = open("formato_output_verifica", "r").read()
        print(contenuto)
    elif "Sondaggi" in contenuto:
        print(contenuto)
    elif "Bacheche digitali" in contenuto:
        print(contenuto)
    elif "Schede di lavoro" in contenuto:
        print(contenuto)
    elif "Test semi-strutturato" or "Test strutturato" or "Test non strutturato" or "Domande flash" or "Prova scritta" or "Sondaggi" or "Quiz" or "Esercizi a risposta multipla" in contenuto:
        formato_output = open("formato_output_verifica", "r").read()
        print(contenuto)
    elif "Test Valutazione" in contenuto:
        print(contenuto)
    elif "Mappe mentali condivise" in contenuto:
        print(contenuto)
    elif "Lavoro di gruppo" in contenuto:
        print(contenuto)
    elif "rainstorming" in contenuto:
        print(contenuto)


    role_system = (
        f"Agisci da esperto docente di Informatica negli {tipo_scuola}."
        f"Il tuo compito è fornire il contenuto della lezione che ti fornirò nell’ambito della progettazione didattica per la disciplina {disciplina}."
        f"Dovrai fornire la progettazione tramite un JSON."
    )

    role_user = (
        f"Io ti fornirò l'argomento di riferimento, struttura della lezione, materiale didattico, e tuo restituirai il contenuto della lezione per la Progettazione Disciplinare nel formato richiesto. {formato_output}. "
        f"### ARGOMENT {lezione}. ### MATERIALE DIDATTICO {contenuto}"
        f"CONTENUTO LEZIONE:"
    )

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
            elenco_path = 'contenuto_lezione.json'
            with open(elenco_path, 'w', encoding='utf-8') as json_file:
                json.dump(response_data, json_file, ensure_ascii=False, indent=2)

            print(f"La risposta è stata salvata in {elenco_path}")
        except json.JSONDecodeError as e:
            print("Errore nel decodificare il JSON:", e)
            print("Contenuto JSON estratto:", json_text)
    else:
        print("Errore: non è stato possibile individuare un blocco JSON valido nella risposta.")
        print("Contenuto della risposta:", response_text)

