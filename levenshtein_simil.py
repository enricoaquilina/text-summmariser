from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import collections
from stop_words import get_stop_words
from nltk.corpus import stopwords
from Levenshtein import distance
import numpy as np
import string

class Levenshtein_Simil:
    def __init__(self, raw_documents):
        self.raw_documents = raw_documents
        self.stop_words = list(get_stop_words('en'))
        self.nltk_words = list(stopwords.words('english'))
        self.stop_words.extend(self.nltk_words)

    def clean_text(self, doc_sents):
        # Remove new lines and unnecessary spacing
        doc_sents = [' '.join(sent.split()) for sent in doc_sents]

        # Remove punctuation
        translator = str.maketrans('', '', string.punctuation)
        doc_sents = [sent.translate(translator) for sent in doc_sents]

        # Remove stop words
        text_words = [word_tokenize(sent) for sent in doc_sents]
        processed_sents = []
        for sentence_words in text_words:
            sent = '';
            for word in sentence_words:
                if word not in self.stop_words and not word.isdigit():
                    sent += ' '+word
            processed_sents.append(sent.strip())
        return processed_sents


    def compute_similarities(self):
        doc_similarity = []
        for i, doc1 in self.raw_documents.items():
            doc1_sents = self.clean_text(sent_tokenize(doc1))
            most_similar_document = collections.OrderedDict()
            for j, doc2 in self.raw_documents.items():
                if i < j:
                    doc2_sents = self.clean_text(sent_tokenize(doc2))

                    # sent_similarity will average out each sentence in doc1 to doc2
                    # doc_similarity values will hold the mean sentence similarity of doc1 in respect to doc2
                    sent_similarity = 0
                    doc_similarity_values = np.zeros(len(doc1_sents))

                    for sid, sent1 in enumerate(doc1_sents):
                        for sent2 in doc2_sents:
                            # normalizing the distance between the 2 documents
                            if len(sent1) > 0 or len(sent2) > 0:
                                dist_norm = distance(sent1, sent2) / max(len(sent1), len(sent2))
                                sent_similarity += dist_norm
                        sent_similarity /= len(doc2_sents)
                        doc_similarity_values[sid] = sent_similarity
                        sent_similarity = 0


                    most_similar_document[i, j] = doc_similarity_values.mean()
            doc_similarity.append(collections.OrderedDict(sorted(most_similar_document.items(), key=lambda x: x[1], reverse=True)))

        return doc_similarity




