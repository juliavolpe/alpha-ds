#Project 2: Sentiment Analysis by Julia Volpe and Edward Birch
#This program calculates word sentiment level, based on the user reviews from the Yelp academic dataset.
#Due March 18th, 2021
#Julia 50%
#Edward 50%

import json
import sys
import nltk
import csv
import time
from collections import Counter
from nltk.corpus import words
from nltk.corpus import stopwords

nltk.download('words')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet') 
YELP_REVIEW_FILE_NAME = 'yelp_academic_dataset_review_small.json'
WORD_SET = set(words.words('en')) 
STOP_WORD_SET = set(stopwords.words('english'))
CSV_FILE_NAME = "lemmas.csv"

def readFile(filename):
    try:
        with open(filename, mode= "r") as f:
            return f.read()
    except:
        print("Sorry, could not open file %s" % f)
        return None

#gets json content
def getJson(data):
    try:
        return json.loads(data)
    except:
        raise RuntimeError("Sorry, could not get json data")

#processes text using lemmas   
def processText(text):
    wordList = nltk.word_tokenize(text.lower())
    lem = nltk.WordNetLemmatizer()
    lemmed = [lem.lemmatize(w) for w in wordList]           
    finalList = [word for word in lemmed if word not in STOP_WORD_SET and word.isalnum() and word in WORD_SET]
    return set(finalList)

#processes review using sum rating by lemmas dict and number of reviews by lemma dict
def processReview(record, sumRating, numReviews):
    starRating = record["stars"]
    text = record["text"]
    wordList = processText(text)
    for word in wordList:
        if word not in sumRating:
            sumRating[word] = starRating
            numReviews[word] = 1
        else:
            sumRating[word] += starRating
            numReviews[word] += 1

#writes CSV file
def writeCSV(sortedAv, dictionary):
    print()
    print("Writing... " + CSV_FILE_NAME)
    try:
        with open(CSV_FILE_NAME, mode='w') as f:
            writer = csv.writer(f, delimiter=',')
        #this did not work for some reason
        # with open(CSV_FILE_NAME, 'w') as csvfile:
        #     writer = csv.writer(csvfile, delimeter = ",", quote = '"', quoting = csv.QUOTE_MINIMAL)
            #headers
            writer.writerow(['Lemma', ' Sentiment Level']) 
            writer.writerow(["-------------------------"])

            for w in sortedAv[-500:]:
                writer.writerow([w, dictionary[w]])
            writer.writerow(["-------------------------"])
            for w in sortedAv[:500]:
                writer.writerow([w, dictionary[w]])       
    except:
        print("Sorry, could not open csv file %s" % f)
        return None

#main method
def main():
    try:
        file = readFile(YELP_REVIEW_FILE_NAME)
        jsonContent = getJson(file)
            
        sumRating = dict()
        numReviews = dict()
        averageRating = dict()
        
        printCount = 0
        for record in jsonContent:
            if (printCount > 5000):
                sys.stdout.write(".")
                sys.stdout.flush()
                printCount=0
            processReview(record, sumRating, numReviews)
            printCount += 1

        keysToRemove=[key for key in numReviews if numReviews[key] < 10]
        for key in keysToRemove:
            del numReviews[key]
            del sumRating[key]

        for key in numReviews.keys():
            averageRating[key] = (sumRating[key] / numReviews[key])

        sortedAv = sorted(averageRating, key = averageRating.get, reverse = True)

        writeCSV(sortedAv, averageRating)

    except Exception as e:
        print("Sorry, error %s", e)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("---Execution duration: %s seconds ---" % (time.time() - start_time))
