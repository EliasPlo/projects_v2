import nltk
from nltk.tokenize import word_tokenize
from transformers import pipeline

# Lataa tarvittavat NLTK:n komponentit
nltk.download('punkt')

# Luo HuggingFace Transformers -malliin perustuva QA-pipeline
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# Esimerkkitietokanta kysymyksiin ja vastauksiin
faq_context = """ 
FAQ-botille usein kysyttyjä kysymyksiä: 
1. Mikä on palautusoikeus? Asiakkailla on 30 päivän palautusoikeus.
2. Kuinka voin ottaa yhteyttä asiakaspalveluun? Voit lähettää meille sähköpostia osoitteeseen support@yritys.fi.
3. Missä toimistomme sijaitsevat? Toimistomme sijaitsevat Helsingissä ja Tampereella.
"""

# FAQ-botin päätoiminto
def chatbot():
    print("Tervetuloa FAQ-bottiin! Kysy kysymys, niin vastaan parhaani mukaan.")
    print("(Kirjoita 'lopeta' poistuaksesi ohjelmasta.)")
    while True:
        user_input = input("Sinä: ")
        if user_input.lower() == 'lopeta':
            print("FAQ-botti: Kiitos käytöstä! Nähdään taas.")
            break

        # NLTK-tokenisaatio kysymyksen siistimiseen
        tokens = word_tokenize(user_input)
        processed_question = " ".join(tokens)

        # HuggingFace QA-pipeline
        try:
            answer = qa_pipeline(question=processed_question, context=faq_context)
            print(f"FAQ-botti: {answer['answer']}")
        except Exception as e:
            print("FAQ-botti: En valitettavasti osaa vastata tuohon kysymykseen.")

if __name__ == "__main__":
    chatbot()
