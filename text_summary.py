import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
text = """ Paragraphs are the building blocks of papers. 
Many students define paragraphs in terms of length: a paragraph is a group of at least five sentences,
a paragraph is half a page long, etc. 
In reality, though, the unity and coherence of ideas among sentences is what constitutes a paragraph.
A paragraph is defined as “a group of sentences or a single sentence that forms a unit” 
(Lunsford and Connors 116). 
Length and appearance do not determine whether a section in a paper is a paragraph.
For instance, in some styles of writing, particularly journalistic styles,
a paragraph can be just one sentence long. Ultimately,
a paragraph is a sentence or group of sentences that support one main idea. In this handout, 
we will refer to this as the “controlling idea,”
because it controls what happens in the rest of the paragraph."""
def summarizer(rawdocs):
    stopwords = list(STOP_WORDS)
    # print(stopwords)
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(rawdocs)
    # print(doc)
    tokens = [token.text for token in doc]
    # print(tokens)
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1
    # print(word_freq)
    max_freq = max(word_freq.values())
    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq
    # print(word_freq)
    sent_tokens = [sent for sent in doc.sents]
    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]
    # print(sent_scores)
    select_len = int(len(sent_tokens)* 0.3) #0.3 means 30 percent of total length
    # print(select_len)
    summary = nlargest(select_len, sent_scores, key= sent_scores.get)
    # print(summary)
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    # print(text)
    # print(summary)
    # print("Length of original text ", len(text.split(' ')))
    # print("Length of summary text ", len(summary.split(' ')))
    return summary, doc , len(rawdocs.split(' ')),len(summary.split(' '))