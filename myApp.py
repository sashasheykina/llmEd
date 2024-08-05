
import pandas as pd
import streamlit as st


from openai import OpenAI

# data
from main import elencoUDA
from dettaglio_uda import dettaglioUDA
from elenco_lezioni import elencoLezioni
from lezione import dettaglioLezione
from slides import genSlides

# Directly assign the API key
OPENAI_API_KEY = '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'
client = OpenAI(api_key=OPENAI_API_KEY)

items = ['Istituti Tecnici Settore Economico', 'Istituti Tecnici Settore Tecnologico']
grado = ['Primo Anno', 'Secondo Anno', 'Terzo Anno', 'Quarto Anno', 'Quinto Anno']
indirizzo = []

st.title("🎈 Benvenuti nell'esperimento GENERAZIONE DELLA LEZIONE IN INFORMATICA")
st.write(
    "Inserisce la descrizione del contest della tua classe"
)

indirizzi = {'items':  ['Istituti Tecnici Settore Economico', 'Istituti Tecnici Settore Economico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico'],
        'indirizzo': ['Amministrazione, finanza e marketing', 'Turismo', 'Agraria, agroalimentare e agroindustria', 'Chimica, materiali e biotecnologie', 'Meccanica, meccatronica ed energia']}

df = pd.DataFrame(indirizzi)

docente = st.text_input('Docente', key='doc')


# feature_1 filters
items_val = df["items"].unique()
feature_1ed = st.selectbox('Seleziona tipo scuola',  items_val)
# filter out data
df = df[(df["items"] == feature_1ed)]

# feature_2 filters
feature_2_val = df["indirizzo"].unique()
feature_2 = st.selectbox('Seleziona indirizzo',  feature_2_val)
# filter out data
df = df[(df["indirizzo"] == feature_2)]


grado = st.selectbox("Selecziona grado classe", pd.Series(grado), key='gr')
contesto = st.text_input('Contesto classe', key='ctx')


# order register
with st.form(key='cad_form', clear_on_submit=True):

    if st.form_submit_button("Genera lezione :white_check_mark:"):
        #elencoUDA(feature_1ed, grado, feature_2, contesto, client)
        #dettaglioUDA(feature_1ed, grado, feature_2, contesto, client)
        elencoLezioni(feature_1ed, grado, feature_2, contesto, client)
        dettaglioLezione(feature_1ed, grado, feature_2, contesto, client)
        genSlides(feature_1ed, grado, feature_2, contesto, client)



