
import pandas as pd
import streamlit as st
from openai import OpenAI
from streamlit_option_menu import option_menu
from streamlit_extras.stylable_container import stylable_container
from pd_class import ProgettazioneDidattica
from tools import aggiorna_elencoUDA, aggiorna_elencoLezioni, lineeGuida, periodoUda, elencoLezioni, elencoUDA, \
    dettaglioUDA, genera_PDC, elencoContenuti, aggiorna_elencoContenuti, getMaterialeDidattico, \
    aggiorna_elencoAttivita, creaContenuto

# Directly assign the API key
OPENAI_API_KEY = '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'
client = OpenAI(api_key=OPENAI_API_KEY)

st.set_page_config(page_title="", layout='wide')
st.title("Benvenuto nell'esperimento")

selected = option_menu(None, ["Home", "Materiale didattico", 'Download'],
    icons=['house', "file-earmark-slides", 'cloud-download'],
    styles={
        "container": {"margin": "0px !important", "padding": "0!important", "align-items": "stretch", "background-color": "#fafafa"},
        "icon": {"font-size": "15px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": { "font-size": "16px", "font-weight": "normal"}
    },
    menu_icon="cast", default_index=0, orientation="horizontal")



lezione_info = {'tipo_scuola':  ['Istituti Tecnici Settore Economico', 'Istituti Tecnici Settore Economico', 'Istituti Tecnici Settore Economico', 'Istituti Tecnici Settore Economico', 'Istituti Tecnici Settore Economico', 'Istituti Tecnici Settore Economico', 'Istituti Tecnici Settore Economico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico',  'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico','Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico'],
        'indirizzo': ['Amministrazione, finanza e marketing', 'Amministrazione, finanza e marketing', 'Amministrazione, finanza e marketing', 'Amministrazione, finanza e marketing', 'Amministrazione, finanza e marketing', 'Amministrazione, finanza e marketing', 'Amministrazione, finanza e marketing', 'Grafica e comunicazione', 'Grafica e comunicazione', 'Grafica e comunicazione', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni','Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni'],
        'articol': ['Relazioni internazionali per il Marketing', 'Relazioni internazionali per il Marketing', 'Relazioni internazionali per il Marketing', 'Relazioni internazionali per il Marketing', 'Sistemi informativi aziendali', 'Sistemi informativi aziendali', 'Sistemi informativi aziendali', 'Grafica e comunicazione', 'Grafica e comunicazione', 'Grafica e comunicazione',  'Informatica', 'Informatica', 'Informatica', 'Informatica', 'Informatica', 'Informatica', 'Informatica', 'Informatica', 'Informatica', 'Informatica', 'Informatica', 'Informatica', 'Telecomunicazioni', 'Telecomunicazioni', 'Telecomunicazioni', 'Telecomunicazioni', 'Telecomunicazioni','Telecomunicazioni', 'Telecomunicazioni', 'Telecomunicazioni', 'Telecomunicazioni', 'Telecomunicazioni', 'Telecomunicazioni', 'Telecomunicazioni'],
        'materia': ['Informatica', 'Informatica', 'Tecnologie della comunicazione', 'Tecnologie della comunicazione', 'Informatica', 'Informatica', 'Informatica', 'Progettazione multimediale', 'Progettazione multimediale', 'Progettazione multimediale', 'Sistemi e reti', 'Sistemi e reti', 'Sistemi e reti', 'Tecnologie e progettazione di sistemi informatici e di telecomunicazioni', 'Tecnologie e progettazione di sistemi informatici e di telecomunicazioni', 'Tecnologie e progettazione di sistemi informatici e di telecomunicazioni', 'Gestione progetto, organizzazione di inpresa',
                   'Informatica', 'Informatica', 'Informatica', 'Telecomunicazioni', 'Telecomunicazioni', 'Sistemi e reti', 'Sistemi e reti', 'Sistemi e reti', 'Tecnologie e progettazione di sistemi informatici e di telecomunicazioni', 'Tecnologie e progettazione di sistemi informatici e di telecomunicazioni', 'Tecnologie e progettazione di sistemi informatici e di telecomunicazioni', 'Gestione progetto, organizzazione di inpresa',
                   'Informatica', 'Informatica', 'Telecomunicazioni', 'Telecomunicazioni', 'Telecomunicazioni'],
        'grado' : ['III', 'IV', 'III', 'IV', 'III', 'IV', 'V', 'III', 'IV', 'V', 'III', 'IV', 'V', 'III', 'IV', 'V', 'V', 'III', 'IV', 'V', 'III', 'IV', 'III', 'IV', 'V', 'III', 'IV', 'V', 'V', 'III', 'IV', 'III', 'IV', 'V']}
df = pd.DataFrame(lezione_info)

if "doc" not in st.session_state:
    st.session_state["doc"] = ""

if "ctx" not in st.session_state:
    st.session_state["ctx"] = ""

if "ore_anno" not in st.session_state:
    st.session_state["ore_anno"] = 0

if "oreSett" not in st.session_state:
    st.session_state["oreSett"] = 0


periodo = ""
# Initialize disabled for form_submit_button to False
if "disabled" not in st.session_state:
    st.session_state.disabled = False

if "disabledD" not in st.session_state:
    st.session_state.disabledD = False

if "disabledUDA" not in st.session_state:
    st.session_state.disabledUDA = True

if "disabledPDC" not in st.session_state:
    st.session_state.disabledPDC = True

if "disabledLs" not in st.session_state:
    st.session_state.disabledLs = True

if "disabledL" not in st.session_state:
    st.session_state.disabledL = True

if "disabledC" not in st.session_state:
    st.session_state.disabledC = True

if "disabledS" not in st.session_state:
    st.session_state.disabledS = True

if "disabledTemp" not in st.session_state:
    st.session_state.disabledTemp = True

if "ppt_bytes" not in st.session_state:
    ppt_bytes = 'output_presentation.pptx'
    st.session_state.ppt_bytes = ppt_bytes

def unable():
    del st.session_state["doc"]
    st.session_state["tipoS"] = None
    st.session_state["adr"] = None
    del st.session_state["ctx"]
    del st.session_state["ore_anno"]
    del st.session_state["oreSett"]
    st.session_state.uda_options = []
    st.session_state.lezione_options = []
    st.session_state.disabled = False
    st.session_state.disabledPDC = True
    st.session_state.disabledL = True
    st.session_state.disabledLs = True
    st.session_state.disabledUDA = True


# Disable the submit button after it is clicked
def salva_dati(tipo_scuola, indirizzo, linee_guida, grado, contesto, docente, disciplina, articolazione, ore_set, ore_anno, warn, succ):
        if tipo_scuola == None or indirizzo == None or grado == None or contesto == None or contesto =="" or docente == None or docente == ""\
                or ore_set == 0 or ore_anno ==0 or disciplina == None or articolazione == None:
            warn.warning('Compila tutti i campi!', icon="⚠️")
        else:
            st.session_state.disabledUDA = False
            st.session_state.disabled = True
            succ.success('I tuoi dati sono stati salvati con successo!', icon="✅")




#def unablePDC():
 #   st.session_state.disabledPDC = False

with st.sidebar:

    docente = st.text_input('Nome Docente', key='doc', placeholder="Nome docente...",
                            label_visibility="collapsed", disabled=st.session_state.disabled)
    # feature_1 filters
    items_val = df["tipo_scuola"].unique()
    tipo_scuola = st.selectbox('Seleziona tipo scuola',  items_val, key="tipoS", index=None, placeholder="Seleziona tipo istituto...",
                            label_visibility="collapsed", disabled=st.session_state.disabled)
    # filter out data
    df = df[(df["tipo_scuola"] == tipo_scuola)]


    # feature_2 filters
    feature_2_val = df["indirizzo"].unique()
    address = st.selectbox('Seleziona indirizzo', feature_2_val, key = "adr", index=None, placeholder="Seleziona indirizzo...",
                            label_visibility="collapsed", disabled=st.session_state.disabled)
    # filter out data
    df = df[(df["indirizzo"] == address)]
    # feature_3 filters
    art = df["articol"].unique()
    articolazione = st.selectbox('Seleziona articolazione',  art, index=None, placeholder="Seleziona articolazione...",
                            label_visibility="collapsed", disabled=st.session_state.disabled)
    # filter out data
    df = df[(df["articol"] == articolazione)]

    # feature_4 filters
    matt = df["materia"].unique()
    disciplina = st.selectbox('Seleziona disciplina',  matt, index=None, placeholder="Seleziona disciplina...",
                            label_visibility="collapsed", disabled=st.session_state.disabled)
    # filter out data
    df = df[(df["materia"] == disciplina)]
    grade = df["grado"].unique()
    grado = st.selectbox('Seleziona grado classe', grade, disabled=st.session_state.disabled)
    df = df[(df["grado"] == grado)]

    contesto = st.text_area('Contesto classe', key='ctx', label_visibility="collapsed", placeholder="Inserisci contesto classe...", disabled=st.session_state.disabled, height=250, max_chars=2000)
    linee_guida = lineeGuida(articolazione, disciplina)
    ore_anno = st.number_input('Inserisce monte ore annuale', min_value=0, max_value=500, step=1, key="ore_anno",
                               disabled=st.session_state.disabled, label_visibility="visible")
    ore_sett = st.number_input('Inserisce monte ore settimanale', min_value=0, max_value=32, step=1, key="oreSett",
                               disabled=st.session_state.disabled, label_visibility="visible")

    col1, col2 = st.columns(
        [1, 1])
    warn = st.container()
    succ = st.container()

    with col1:
        st.button("Salva", use_container_width=True, disabled=st.session_state.disabled, on_click=salva_dati(tipo_scuola, address, linee_guida, grado, contesto, docente, disciplina, articolazione, ore_sett, ore_anno, warn, succ))

    with col2:
        st.button(
            "Resetta",
            kwargs=None,
            on_click=unable,
            use_container_width=True,
        )

    with warn:
        alert = warn.warning('Compila tutti i campi!', icon="⚠️")
        alert.empty()

    with succ:
        alert = succ.success('I tuoi dati sono stati salvati con successo!', icon="✅")
        alert.empty()


# Inizializza lo stato se non è già stato fatto
if "uda_options" not in st.session_state:
    st.session_state.uda_options = []  # Inizialmente vuoto

if "lezione_options" not in st.session_state:
    st.session_state.lezione_options = []  # Inizialmente vuoto

# Inizializza lo stato se non è già stato fatto
if "contenuto" not in st.session_state:
    st.session_state.contenuto = []  # Inizialmente vuoto

# Inizializza lo stato se non è già stato fatto
if "struttura" not in st.session_state:
    st.session_state.struttura = []  # Inizialmente vuoto

progm_didat = ProgettazioneDidattica(
        tipo_scuola=tipo_scuola,
        indirizzo=address,
        linee_guida=linee_guida,
        grado=grado,
        contesto=contesto,
        docente=docente,
        disciplina=disciplina,
        articolazione=articolazione,
        ore_anno=ore_anno,
        ore_sett=ore_sett
    )
selected
if selected == "Home":
    st.title("GENERAZIONE DELLA LEZIONE")
    st.markdown("Gentile Docente, \n\nL'obiettivo di questo esperimento è valutare l'efficacia di uno strumento innovativo progettato per supportarvi nella creazione del materiale didattico per le vostre lezioni. Lo strumento è stato sviluppato per semplificare e velocizzare la produzione dei seguenti materiali: \n\nProgettazione Disciplinare per Competenze: Un documento che include l'analisi della classe, le unità di apprendimento, le competenze da sviluppare e le metodologie didattiche. \n\nSlides della Singola Lezione: Materiale visivo per la presentazione dei contenuti in classe. \n\nSuggerimenti per il Docente: Linee guida per lo svolgimento della lezione, comprensive di strumenti tecnologici per quiz, brainstorming e attività interattive. \n\nIl vostro contributo è fondamentale per valutare la qualità e l'utilità dei materiali generati dallo strumento rispetto ai metodi tradizionali. Durante l'esperimento, vi sarà chiesto di creare i materiali per una specifica lezione utilizzando sia lo strumento automatico che il metodo manuale. Successivamente, analizzeremo insieme vari aspetti qualitativi come la chiarezza, la comprensibilità e la completezza dei materiali generati, oltre alla velocità di produzione. \n\nLa partecipazione all'esperimento ci aiuterà a comprendere se e in che modo questo strumento possa facilitare il vostro lavoro e migliorare la qualità dei materiali didattici.")


if selected == "Materiale didattico":
    with stylable_container(
            key="container1",
            css_styles="""
                {
                    border: 1px solid #E9E9FA;
                    border-radius: 0.5rem;
                    background-color: #FAFAFD;
                    padding: calc(1em - 1px)
                }
                """,
    ):
        st.subheader("Programmazione disciplinare per competenze")
        # Bottone per generare le UDA
        submit_button1 = st.button("Genera Elenco UDA", disabled=st.session_state.disabledUDA)

        if submit_button1:
            #elencoUDA(progm_didat.tipo_scuola, progm_didat.grado, progm_didat.indirizzo, progm_didat.linee_guida, progm_didat.disciplina, progm_didat.contesto, client)
            aggiorna_elencoUDA()
            st.session_state.disabledPDC = False
            st.session_state.disabledLs = False
            col7, col8 = st.columns([1000, 1])
            with col7:
                st.success('Elenco UDA generati con successo!', icon="✅")
            with col8:
                pass

        submit_button2 = st.button("Crea PDC", disabled=st.session_state.disabledPDC)
        if submit_button2:
            #genera_PDC(progm_didat.tipo_scuola, progm_didat.grado, progm_didat.indirizzo, progm_didat.articolazione, progm_didat.linee_guida, progm_didat.disciplina, progm_didat.contesto, progm_didat.docente, ore_sett, ore_anno, client)
            col7, col8 = st.columns([1000, 1])
            with col7:
                st.success('Programmazione Disciplinare per Competenze generata con successo!', icon="✅")
            with col8:
                pass


    with stylable_container(
            key="container2",
            css_styles="""
                    {
                        border: 1px solid #E9E9FA;
                        border-radius: 0.5rem;
                        background-color: #FAFAFD;
                        padding: calc(1em - 1px)
                    }
                    """,
    ):
        st.subheader("Pianifica la tua lezione")
        col3, col4 = st.columns([1000, 1])
        with col3:
            # Crea il selectbox prima del form, collegato a `st.session_state["uda_options"]`
            uda = st.selectbox('Seleziona Unità Didattiche',  st.session_state.uda_options, key="uda")
            submit_button3 = st.button("Genera Lezioni", disabled=st.session_state.disabledLs)

            lezione = st.selectbox('Seleziona Lezione', st.session_state.lezione_options, key="less")
        with col4:
            pass

        periodo = periodoUda(uda)

        if submit_button3:
            #dettaglioUDA(progm_didat.tipo_scuola, progm_didat.grado, progm_didat.indirizzo, progm_didat.linee_guida, progm_didat.disciplina, uda, progm_didat.contesto, progm_didat.docente, progm_didat.ore_sett, progm_didat.ore_anno, client)
            #elencoLezioni(progm_didat.tipo_scuola, progm_didat.grado, progm_didat.indirizzo, disciplina, uda, periodo, progm_didat.ore_anno, progm_didat.ore_sett, progm_didat.contesto, client)
            st.session_state.disabledL = False
            aggiorna_elencoLezioni()


        submit_button4 = st.button("Genera Contenuti", disabled=st.session_state.disabledL)
        if submit_button4:
            #elencoContenuti(progm_didat.tipo_scuola, progm_didat.grado, progm_didat.indirizzo, progm_didat.disciplina, lezione, client)
            st.session_state.disabledS = False
            aggiorna_elencoContenuti()


    with stylable_container(
            key="container",
            css_styles="""
                            {
                                border: 1px solid #E9E9FA;
                                border-radius: 0.5rem;
                                background-color: #FAFAFD;
                                padding: calc(1em - 1px)
                            }
                            """,
    ):
        st.subheader("Struttura lezione specifica")
        col5, col6 = st.columns([1000, 1])
        with col5:
            struttura = st.selectbox('Seleziona tipologia lezione', st.session_state.struttura)
        with col6:
            pass
        submit_button6 = st.button("Genera sussidi didattici", disabled=st.session_state.disabledS)
        if submit_button6:
            getMaterialeDidattico(uda, lezione, struttura, client)
            st.session_state.disabledC = False
            aggiorna_elencoAttivita()


    with stylable_container(
            key="container",
            css_styles="""
                            {
                                border: 1px solid #E9E9FA;
                                border-radius: 0.5rem;
                                background-color: #FAFAFD;
                                padding: calc(1em - 1px)
                            }
                            """,
        ):
        st.subheader("Contenuti attività specifica")
        col11, col12 = st.columns([1000, 1])
        with col11:
            contenuto = st.selectbox('Seleziona contenuto', st.session_state.contenuto)
        with col12:
            pass
        submit_button7 = st.button("Crea Contenuto", disabled=st.session_state.disabledC)
        if submit_button7:
            #creaContenuto(progm_didat.tipo_scuola, progm_didat.disciplina, lezione, contenuto, client)
            pass

        col9, col10 = st.columns([1000, 1])
        with col9:
            uploaded_files = st.file_uploader(
                "Carica il tuo template", accept_multiple_files=True, disabled=st.session_state.disabledTemp
            )
            for uploaded_file in uploaded_files:
                bytes_data = uploaded_file.read()
                st.write("filename:", uploaded_file.name)
                st.write(bytes_data)
        with col10:
            pass

        submit_button5 = st.button("Crea PPT della Lezione",
                                   disabled=True)


if selected == "Download":
    with stylable_container(
            key="container4",
            css_styles="""
                        {
                            border: 1px solid #E9E9FA;
                            border-radius: 0.5rem;
                            background-color: #FAFAFD;
                            padding: calc(1em - 1px)
                        }
                        """,
    ):
        st.subheader("Scarica qui il tuo materiale")
        # Mostra il pulsante di download solo se il form è stato inviato con successo
        if 'ppt_bytes' in st.session_state:
            st.download_button(
                label="Download PDC",
                data=st.session_state.ppt_bytes,
                file_name="pdc.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
        # Mostra il pulsante di download solo se il form è stato inviato con successo
        if 'ppt_bytes' in st.session_state:
            st.download_button(
            label="Download Lezione Frontale",
            data=st.session_state.ppt_bytes,
            file_name="output_presentation.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
        # Mostra il pulsante di download solo se il form è stato inviato con successo
        if 'ppt_bytes' in st.session_state:
            st.download_button(
                label="Download Contenuti Lezione",
                data=st.session_state.ppt_bytes,
                file_name="output_presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )




