#!/usr/bin/env python
# coding: utf-8

# import libraries
import os
import pandas as pd
import nltk
from nltk.corpus import stopwords
import copy
import textdistance

# Change working directory
os.chdir(r'raw data/')

# Import raw data
dat1 = pd.read_pickle('./whiskeyconsensus-reviews-raw-July-2021.pkl')


# Step 1: Text cleaning -- normalize text
# Lower case
dat2 = dat1[['Color','Nose','Palate','Finish']].apply(lambda x: x.str.lower(), axis=0)

# Remove punctuation
dat3 = dat2[['Color','Nose','Palate','Finish']].apply(lambda x: x.str.replace('[^\w\s]', '', regex = True), axis=0)

# Remove extra white space
dat4 = dat3.join(dat1[['Name', 'reviewUrl']])

dat5 = dat4.replace('s+',' ', regex = True)

# Replace html ampersand escapes
dat6 = dat5.replace('&amp;', '&', regex = True)


# Step 2: Remove stop words
stopWords = stopwords.words('english')
for i in ['nose', 'palate', 'finish']:
    stopWords.append(i)

def removeStopWords(sentence):
    'The function splits each string in a cell apart and rejoins the sentence after removing any stop words'
    wordList=sentence.split()
    cleanSentence = ' '.join([w for w in wordList if w.lower() not in stopWords])
    return(cleanSentence)

dat6['Nose'] = dat6['Nose'].apply(removeStopWords)
dat6['Palate'] = dat6['Palate'].apply(removeStopWords)
dat6['Finish'] = dat6['Finish'].apply(removeStopWords)


# Step 3: Stemming
def stemming(sentence):
    wordList=sentence.split()
    stemmedSentence = [nltk.PorterStemmer().stem(word) for word in wordList]
    return(stemmedSentence)

dat6['Nose'] = dat6['Nose'].apply(stemming)
dat6['Palate'] = dat6['Palate'].apply(stemming)
dat6['Finish'] = dat6['Finish'].apply(stemming)


# Step 4: Calculate Jaccard similarity
def similarityScore(chosenWhiskey, dataset):
    '''
    The function takes splits the dataset between the chosen whiskey and the other whiskeys and computes the Jaccard similarity
    for each category (Nose, Palate, and Finish) before summing each of the scores together and returning the top 5 results
    '''
    chosenRow = dataset[dataset['Name'] == chosenWhiskey]
    comparisonRows = dataset[dataset['Name'] != chosenWhiskey]
    score = []
    name = []
    for i in range(0, len(comparisonRows)):
        noseScore = textdistance.jaccard(chosenRow.iloc[0, 1], comparisonRows.iloc[i, 1])
        palateScore = textdistance.jaccard(chosenRow.iloc[0, 2], comparisonRows.iloc[i, 2])
        finishScore = textdistance.jaccard(chosenRow.iloc[0, 3], comparisonRows.iloc[i, 3])
        tempScore = noseScore + palateScore + finishScore
        score.append(tempScore)
        name.append(comparisonRows.iloc[i, 4])
    finalDat = pd.DataFrame()
    finalDat['Name'] = name
    finalDat['Score'] = score
    returnDat = finalDat.sort_values(['Score'], ascending=False).iloc[0:5, 0:2]
    return(returnDat)    
    
# Test
# similarityScore('William Larue Weller (2020)', dat6)

# Export dataset
os.chdir(r'clean data/')
dat6.to_pickle("./whiskeyconsensus-dataset-July-2021.pkl")

