print('Loading Modules...')

import praw
import pdb
import re
import os
from time import sleep

from random import randint
from datetime import datetime
from nltk.sentiment import SentimentIntensityAnalyzer as sia
from nltk.tokenize import sent_tokenize as senTok
from nltk import download
from numpy import mean

file = open('id.redID', 'r')
RedID = file.read()
file.close()

class Watcher():

    def __init__(self):

        # Get key
        self.reddit = praw.Reddit(RedID, user_agent=RedID)
        
        # id Target
        while True:
            try:
                
                self.ask = input('Where Should I Look: r/')
                self.subreddit = self.reddit.subreddit(self.ask)
                break
                
            except:
                pass


        # How deep should I look
        self.depth = None
        # Set up list for data storage
        
        self.data = []

        # load language processor
        self.langVal = sia()
        download('vader_lexicon')
        print('Loading Successful. Now Obtaining Approximate Sentiment Info...')
        sleep(3)

        
    def start(self):

        countS = 0
        countC = 0

        print('\nReading Posts and Comments: ')
        #print('Cycles: \n')
        for submission in self.subreddit.new(limit=self.depth):

            # 1. Get the submission's score
            if submission.selftext != '':
                print(submission.selftext)
                content = submission.selftext
                contentL = senTok(content)
                
                if len(contentL) > 0:
                
                    scores = [self.langVal.polarity_scores(sen)['compound'] for sen in contentL]
                    result = mean(scores)
                
                    self.data.append(float(result))
                    
                    

            # 2. Look at the comments under it
            for comment in submission.comments.list():
        
                try:
                    print(comment.body)
                    
                    comCont = comment.body
                    comContL = senTok(comCont)
                    
                    
                    
                    if len(comContL) > 0:
                        scores = [self.langVal.polarity_scores(sen)['compound'] for sen in comContL]
                        self.data.append(mean(scores))
                        
                        
                    
                except:
                   pass
                #print('\n', end='')
                countC += 1

            #print('\n', end='')
            countS += 1


        print('\n\n', end='')
        print('==================================\n' * 2)
        print('Processing Data\n')
        print('==================================\n' * 2)
        #sleep(2)


        print('')
        for x in range(9):
              print('.')
              sleep(0.5)
        
        print('')
        print(str(len(self.data)) + ' Posts/Comments Recieved\n')
        print('Mean Compound Sentiment Score (1 = Max Positive, -1 = Max Negative): %.4f' % mean(self.data))
        
        


# Start Main =========================

main = Watcher()
main.start()
input('\nPress Enter to End ...')
