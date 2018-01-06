import csv
import pickle

punct = ['.', ',', '\n', '?', '!', '(', ')']

def tokenize(text):
    for ch in punct:
        text = text.replace(ch, ' ')
    return text.split()

with open('lyrics.csv', newline='', encoding='utf-8') as csvfile:
    names = []
    years = []
    artists = []
    genres = []
    lyrics = []
    
    reader = csv.reader(csvfile, delimiter=',')
    reader.__next__()  
    for row in reader:
        names.append(row[1])
        years.append(row[2])
        artists.append(row[3])
        genres.append(row[4])
        lyrics.append(tokenize(row[5]))
        
    fwrite = open('data.pkl', 'wb')
    pickle.dump((names, years, artists, genres, lyrics), fwrite)
