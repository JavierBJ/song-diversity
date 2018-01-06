#!/usr/bin/env python

import numpy as np
import pickle
from sklearn.cluster import KMeans

num_clusters = 20
originality_scores = []
diversity_scores = []

# save embeddings
embeddings = {}
f = open('glove.6B.50d.txt', 'r', encoding='utf-8')
i = 0
for line in f:
    parts = line.split()
    embeddings[parts[0]] = parts[1:]

# cluster word embeddings
alg = KMeans(n_clusters=num_clusters, random_state=0)
arr_embs = np.array(list(embeddings.values()))
arr_embs = arr_embs[0:4000,:]
print(arr_embs.shape)
#print(type(arr_embs[0]))
#import sys
#sys.exit(1)

clusters = alg.fit_predict(arr_embs)
centroids = alg.cluster_centers_
num_centroids = len(centroids)

print(centroids.shape)

f = open('data.pkl', 'rb')
names, years, artists, genres, lyrics = pickle.load(f)
print('Total songs:', len(names))

# Initialize genre-diversity data structures
div_genres = {}
count_genres = {}
for genre in genres:
    if genre not in div_genres:
        div_genres[genre] = 0
        count_genres[genre] = 0

div_years = {}
count_years = {}
for year in years:
    if year not in div_years:
        div_years[year] = 0
        count_years[year] = 0

div_artists = {}
count_artists = {}
for artist in artists:
    if artist not in div_artists:
        div_artists[artist] = 0
        count_artists[artist] = 0

# calculate diversity for each lyrics
for i, (name, year, artist, genre, lyric) in enumerate(zip(names, years, artists, genres, lyrics)):
    if i%100==0:
        print(i)
    #if i>=100000:
    #    break
    if len(lyric)==0:
        continue
    
    clusters_used = []
    for word in lyric:
        if word in embeddings:
            vec = embeddings[word]
            cluster_idx = alg.predict([vec])
            if cluster_idx not in clusters_used:
                clusters_used.append(cluster_idx)
    diversity = len(clusters_used) / num_centroids
    div_genres[genre] += diversity
    count_genres[genre] += 1
    div_years[year] += diversity
    count_years[year] += 1
    div_artists[artist] += diversity
    count_artists[artist] += 1

print('Genre diversity:')
for genre, div in div_genres.items():
    if count_genres[genre]>0:
        print(genre, div / count_genres[genre])
print('\nYear diversity:')
for year, div in sorted(div_years.items()):
    if count_years[year]>0:
        print(year, div/count_years[year], count_years[year])
threshold = sorted(count_artists.values(), reverse=True)[100]-1
print('\nArtist diversity:')
for artist, div in div_artists.items():
    if count_artists[artist]>threshold:
        print(artist, div/count_artists[artist])
