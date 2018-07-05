import re
import pandas as pd
import nltk
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.cross_validation import train_test_split
# from sklearn import naive_bayes
# from sklearn.metrics import roc_auc_score


dataset = pd.read_csv('SMSSpamCollection.tsv',sep='\t',header=None)
stopwords = nltk.corpus.stopwords.words('english')
ps = nltk.PorterStemmer()

# remove punctuation and joins back the words
text = "".join([word.lower() for word in text if word not in string.punctuation])


def tokenize(text):
    tokens = re.split('\W+', text)
    return tokens

def remove_stopwords(tokenized_list):
    text = [word for word in tokenized_list if word not in stopwords]
    return text
data['body_text_nostop'] = data['body_text_tokenized'].apply(lambda x: remove_stopwords(x))
data.head()

def stemming(tokenized_text):
    text = [ps.stem(word) for word in tokenized_text]
    return text
