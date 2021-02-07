from googleapiclient.discovery import build
from youTube import getVideoMetaData
from textblob import TextBlob
import os

def getPolarityScore(comments):
    polList = []
    score = 0
    positives = 0
    negatives = 0

    if(comments):
        for c in comments :

            print(f" \n {c}")
        
            blob = TextBlob(c)
            res = blob.sentiment
            pol = res.polarity
            sub = res.subjectivity

            if(pol > 0 and pol <= 1):
                # +ve
                positives += 1
                pol += 0.5
                pol = pol if pol<1 else 1
                score += pol
            elif(pol>=-1 and pol<0):
                # -ve
                negatives += 1
                pol -= 0.20
                pol = pol if pol>-1 else -1
                score += pol
     
            polList.append((pol,sub))

    print(f' \n {polList}')

    score = (score/positives) if positives > negatives else (score/negatives)

    return score


if __name__ == "__main__":
   vid = 'SkcddD0LGlM'
   print(getPolarityScore(vid))