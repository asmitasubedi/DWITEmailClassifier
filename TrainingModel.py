import pandas as pd
import re
import numpy as np
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.stem.porter import PorterStemmer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import csv

# downloading required stop words from nltk and importing the stopwords from nltk corpus
nltk.download('stopwords')
from nltk.corpus import stopwords

# using flask for front end hence importing the render_template for rendering the html files
#from flask import render_template

# df is the dataframe which is training set panda object
df = pd.DataFrame()
# tf is the dataframe which is testing set panda object
tf = pd.DataFrame()

# creating objects
df = pd.read_csv('./trainedemailset.csv')
tf = pd.read_csv('./testemailset.csv')


# preprocessing training set text by removing non-words from training set text
def preprocessor(text):
    text = re.sub('[\W]+', ' ', text)
    return text


df['emails'] = df['emails'].apply(preprocessor)
print(df['emails'])

# removing stop words from training set text
stop = stopwords.words('english')


def remove_stop_words(text):
    return [w for w in text.split() if w not in stop]


porter = PorterStemmer()
df['emails'] = df['emails'].apply(remove_stop_words)
print("df['emails']----->>>", df['emails'])

val = 0
for x in df['emails']:
    df['emails'][val] = [porter.stem(word) for word in x]
    text = ""
    for word in df['emails'][val]:
        text = text + word + " "
    df['emails'][val] = text
    val += 1
print(df['emails'])

# testing usage of CountVextorizer and Tfidfransformer which computes tfidf
count = CountVectorizer()
bag = count.fit_transform(df['emails'])
print("frequency of words--->>", count.vocabulary_)

print("Data in numeric form-->>\n" ,bag.toarray())

tfidf = TfidfTransformer()
np.set_printoptions(precision=2)
print("TFIDF Vector ---->>\n", tfidf.fit_transform(count.fit_transform(df['emails'])).toarray())

# Applying logistic regression classifier
text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', LogisticRegression()), ])

_ = text_clf.fit(df['emails'], df['category'])

# get predicted values
predicted = text_clf.predict(tf['emails'])
print("Predicted labels-->" ,predicted)

# filling categories in club/event emails, classroom emails, admin emails and miscellaneous emails lists
clubEmails = []
classEmails = []
adminEmails = []
msc =[]
ind = 0

home = np.mean(predicted == tf['category'])
print("Accuracy: " + str(home))
for p in predicted:
    if p == 1:
        clubEmails.append(tf['emails'][ind])
        ind += 1
    elif p == 2:
        classEmails.append(tf['emails'][ind])
        ind += 1
    elif p==3:
        adminEmails.append(tf['emails'][ind])
        ind +=1
    else:
        msc.append(tf['emails'][ind])
        ind +=1



print("Club/Events Emails")
print(clubEmails)
print("Predicted No Club Emails:%s" %len(clubEmails))

print("Class Emails")
print(classEmails)
print("Predicted No Class Emails: %s" %len(classEmails))

print("Admin Emails")
print(adminEmails)
print("Predicted No Admin Emails: %s" %len(adminEmails))

print("Miscellaneous")
print(msc)
print("Predicted No Miscellaneous Emails: %s" %len(msc))

confusionMatrix=confusion_matrix(tf["category"], predicted)
print("confusion matrix-->\n", confusionMatrix)

# with open('clubEmails.csv', 'wb') as myfile:
#     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#     wr.writerows(clubEmails)
#
# with open('classEmails.csv', 'wb') as myfile:
#     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#     wr.writerows(classEmails)
#
# with open('adminEmails.csv', 'wb') as myfile:
#     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#     wr.writerows(adminEmails)
#
# with open('msc.csv', 'wb') as myfile:
#     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#     wr.writerows(msc)

# def get_result():
#     """Returns the result"""
#     return [clubEmails, classEmails, adminEmails, msc, confusionMatrix]

import pickle
result = {"adminEmails":adminEmails, "clubEmails": clubEmails, "classEmails":classEmails, "msc":msc, "confusionMatrix":confusionMatrix}
pickle.dump(result, open("RESULT.pickle", "wb"))