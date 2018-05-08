import nltk
import string
import test
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from stop_words import get_stop_words
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import collections

from itertools import repeat
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

paper_tiles = test.run()
document_lookup = {}

doc_id = 0

for paper_id, tiles in paper_tiles.items():
    updated_tiles = []
    for id, tile in enumerate(tiles):

        # Remove new lines and unnecessary spacing
        tile = ' '.join(tile.split())
        document_lookup[doc_id] = tile

        # Remove punctuation
        translator = str.maketrans('', '', string.punctuation)
        tile = tile.translate(translator)

        doc_id += 1

        # Remove stop words
        tile_words = word_tokenize(tile)
        stop_words = list(get_stop_words('en'))
        nltk_words = list(stopwords.words('english'))
        stop_words.extend(nltk_words)
        tile = [w for w in tile_words if not w in stop_words and not w.isdigit()]

        # tile = ''.join([i for i in tile if not i.isdigit()])

        # Perform stemming
        processed_tile = ''

        for word in tile:
            processed_tile += PorterStemmer().stem(word) + ' '
        processed_tile = processed_tile.strip()

        # Update paper tiles
        updated_tiles.append(processed_tile)
    paper_tiles[paper_id] = updated_tiles


raw_documents = []

for paper_id, tiles in paper_tiles.items():
    for id, tile in enumerate(tiles):
        raw_documents.append(tile)


def generate_tfmatrix(journal_documents):
    # getting term by doc matrix utilising TF
    count_vectorizer = CountVectorizer(min_df=1, stop_words='english')

    dtm = count_vectorizer.fit_transform(journal_documents)
    # print(count_vectorizer.get_feature_names())
    document_vectors = pd.DataFrame(dtm.toarray(), columns=count_vectorizer.get_feature_names())

    cluster_centroids[0] = document_vectors.values[0]
    first_cluster = {}
    first_cluster[0] = document_vectors.values[0]

    clusters[0] = [first_cluster]
    # document_vectors = np.delete(document_vectors.values, (0), axis=0)

    return document_vectors.values

def generate_tfidfmatrix(journal_documents):
    # Perform Tf-IDF
    vectorizer = TfidfVectorizer(
        decode_error='ignore', strip_accents='unicode',
        stop_words='english', lowercase=True,
        max_df=0.9, max_features=3000)

    # tfidf similarity
    tfidf = vectorizer.fit_transform(raw_documents)
    tfidf_vectors = pd.DataFrame(tfidf.toarray(), columns=vectorizer.get_feature_names())

    cluster_centroids[0] = tfidf_vectors.values[0]
    first_cluster = {}
    first_cluster[0] = tfidf_vectors.values[0]

    clusters[0] = [first_cluster]

    return tfidf_vectors.values

document_vectors = {}
cluster_centroids = {}
clusters = {}


doc_vectors = generate_tfmatrix(raw_documents)
# doc_vectors = generate_tfidfmatrix(raw_documents)


for vector_id, vector in enumerate(doc_vectors):
    if vector_id > 0:

        # Holds the similarity of the current doc with relation to the existing centroids
        similarity_with_clusters = collections.OrderedDict()
        # document_similar_to_some_cluster = False

        # Check each centroid's similarity with the current document vector
        for centroid_id, centroid in cluster_centroids.items():

            # Calculate similarity and store cluster if necessary
            document_centroid_similarity = cosine_similarity([centroid], [vector])

            if document_centroid_similarity >= 0.5:
                similarity_with_clusters[centroid_id] = document_centroid_similarity[0][0]
                # document_similar_to_some_cluster = True

        # If the current document vector is similar to any of the other centroids,
        # 1.)   place it in that cluster, otherwise
        # 2.)   create new cluster and store

        if len(similarity_with_clusters) > 0:
            most_similar_centroid = list(sorted((value, key) for (key, value) in similarity_with_clusters.items()))[-1][1]
            # Get the document vectors making up the centroid
            centroid_doc_vectors = clusters[most_similar_centroid]

            # Update the new cluster centroid mean
            cluster_documents = []
            for doc in list(centroid_doc_vectors):
                cluster_documents.append(list(doc.values())[0])

            cluster_documents.append(vector)
            new_cluster_mean = np.floor(np.mean(cluster_documents, axis=0))
            cluster_centroids[most_similar_centroid] = new_cluster_mean

            # Update the clusters array holding references to the documents behind the clusters
            new_document_vector = {}
            new_document_vector[vector_id] = vector
            clusters[most_similar_centroid].append(new_document_vector)
        else:
            new_elem = len(cluster_centroids)
            cluster_centroids[new_elem] = vector
            # Creating the new cluster
            next_cluster = {}
            next_cluster[vector_id] = vector
            clusters[new_elem] = [next_cluster]

# move the singleton clusters into an 'Others' cluster
singleton_clusters = []
for id, cluster in list(clusters.items()):
    if len(cluster) == 1:
        singleton_clusters.append(cluster[0])
        del clusters[id]
        del cluster_centroids[id]
clusters['others'] = singleton_clusters

# getting the most representative tile from each of the clusters
# for now, we're only picking THE most similar tile to the cluster centroid
most_representative_documents = {}
for cid, cluster in list(clusters.items()):
    if cid != "others":
        doc_similarities = collections.OrderedDict()
        for doc_id, document_vector in list(enumerate(cluster)):
            document_centroid_similarity = cosine_similarity([cluster_centroids[cid]], [document_vector[list(document_vector.keys())[0]]])
            doc_similarities[list(document_vector.keys())[0]] = document_centroid_similarity

        doc_similarities = collections.OrderedDict(sorted(doc_similarities.items(), key=lambda x: x[1]))
        most_representative_documents[cid] = list(doc_similarities.items())[-1]



for cid, cluster in list(clusters.items()):
    for doc_id, document_vector in list(enumerate(cluster)):
        doc_cluster_id = list(document_vector.keys())[0]
        cluster[doc_id] = document_lookup[doc_cluster_id]
    print(cluster)


print('done')
