from collections import Counter #, defaultdict
import math
import word_processor
# import sys


# __________________________LOAD DATA COLLECTION

# # file1 = 'AFINN-111.txt'
# file2 = 'phrase_list.txt'
# sample = dict(map(lambda (k,v): (k,int(v)), [ line.split('\t') for line in open(file2) ]))
# # summ = sum(map(lambda word: afinn.get(word, 0), "Rainy day but still in a good mood".lower().split()))
#
# sample_text = "It's been a nice day trying to study"

class Classifier:

    # sample = {}

    def __init__(self, samp):
        self.sample = samp
        self.class_division = {}
        self.pos_neg = {}
        self.pos_set_size = 0
        self.neg_set_size = 0
        self.posProbability = 0
        self.negProbability = 0
        self.smoothing = 1





    # print sample

    # pos_tweets = [('I love this car', 'positive'),
    #               ('This view is amazing', 'positive'),
    #               ('I feel great this morning', 'positive'),
    #               ('I am so excited about the concert', 'positive'),
    #               ('He is my best friend', 'positive')]
    #
    # neg_tweets = [('I do not like this car', 'negative'),
    #               ('This view is horrible', 'negative'),
    #               ('I feel tired this morning', 'negative'),
    #               ('I am not looking forward to the concert', 'negative'),
    #               ('He is my enemy', 'negative')]


    # test
    def _likelihood(theta, h):
        return (theta)**(h)*(1-theta)**(1-h)


    # size in terms of quantity of items of sample
    # dataset_size = len(self.sample)

    # pos_set_size = 0
    #
    # neg_set_size = 0

    # smoothing = 1

    # {classA: ['ciao','hei','uno'], classB:['mio,','trenta']}
    features_by_class = {}


    # {classA: 2, classB: 40, classC: 25}
    class_distribution = {}


    # [('bello':1), ('casa',-4), ('ciao',2)....]
    training_set =  []
    testing_set = []




    def _processSentence(self, sentence):
        return word_processor.tokenize(sentence)




    def _splitSet(self, data_set):
        """Takes data_set as input, iterates through it
        and generates training set = 67% of original and testing set = 33% of original"""
        training_size = int(self.data_set_size*0.67)
        temp_training_set = []
        temp_testing_set = []
        i = 0
        for x in data_set.iteritems():
            if i < training_size:
                temp_training_set.append(x)
                i+=1
            else: temp_testing_set.append(x)
        return (temp_training_set, temp_test_set)

    # FOR WORDLIST
    # def divideFeaturesByClass(sample):
    #     """takes input of sample (labelled words) and returns object
    #     with K = label V = [features]"""
    #     temp = {}
    #     for word, label in sample.iteritems():
    #         if label not in temp:
    #             temp[label] = []
    #             temp[label].append(word.lower())
    #         else:
    #             temp[label].append(word.lower())
    #     return temp


    # FOR SENTENCE LIST
    # @staticmethod
    def _divideFeaturesByClass(self, training_set):
        """takes input of training_set (labelled words) and returns object
        with K = label V = [features]"""
        temp = {}
        for word, label in training_set.iteritems():
            if label not in temp:
                temp[label] = []
                # print word.lower()
                temp[label].extend(self._processSentence(word.lower()))
            else:
                temp[label].extend(self._processSentence(word.lower()))
        self.class_division = temp


    def _generateWordDistributionByClass(self, dictionary):
        # {classA: [{},{},{}]
        temp = {}
        # tempA = {}
        # tempB = {}
        for label, words in dictionary.iteritems():
            if label not in temp:
                temp[label] = []
                temp[label].append(Counter(words))
            else:
                temp[label].append(Counter(words))
        tempA = dict(Counter(temp[1][0].elements()))
        tempB = dict(Counter(temp[0][0].elements()))
        temp = {'positive':tempA, 'negative':tempB}
        return temp


    # for dic in generateWordDistributionByClass(divid).iteritems():
    #     print dic


    def _createClassDistribution(self, sample):
        """takes input of sample (labelled words) and returns object
        with K = label V = number of features"""
        temp = {}
        for word, label in self.sample.iteritems():
            if label not in temp:
                temp[label] = 1 + self.smoothing
            else:
                temp[label]+=1
        return temp

    # def createWordFrequency():
    #     temp = P

    # print divideFeaturesByClass(afinn)
    # print [x[0] for x in [ line.split('\t') for line in open(file2) ]]
    # __________________________PROCESS SENTENCE

    def _decomposeSentence(self, sentence):
        array = word_processor.tokenize(sentence)
        return word_processor.filterTokens(array)

    #
    def _findMatches(self, dataset, tokens, label):
        occurrences = 0
        for token in tokens:
            if dataset.get(label).get(token, 0) > 0:
                occurrences+=dataset.get(label).get(token)
                # print token,' is=',dataset.get(label).get(token)
        return occurrences

    # class_division = _divideFeaturesByClass(sample)
    # pos_neg = _generateWordDistributionByClass(class_division)
    # pos_set_size = len(pos_neg.get('positive'))
    # neg_set_size = len(pos_neg.get('negative'))


    def _findMatch(self, data_set, token, label):
        if data_set.get(label).get(token, 0) > 0:
            return data_set.get(label).get(token)
        return 1


    # def findMatches(data_set, tokens, label):
    #     occurrences = 0
    #     for token in tokens:
    #         occurrences+=findMatch(data_set, token, label)
    #     return occurrences


    # posProbability = float(pos_set_size)/(pos_set_size+neg_set_size)
    # negProbability = float(neg_set_size)/(pos_set_size+neg_set_size)


    def _calculateProbability(self, data_set, tokens, label):
        probability = 1

        if label is 'positive':
            for token in tokens:
                probability*= math.log((float(self._findMatch(data_set, token, label))/self.posProbability),2 )
                # print  'and prob here is=',probability

        elif label is 'negative':
            for token in tokens:
                probability*= math.log((float(self._findMatch(data_set, token, label))/self.negProbability),2 )
                # print  'and prob here is=',math.log((float(_findMatch(data_set, token, label))/negProbability),2 )

        return probability



    def _getClassificationValue(self, data_set, tokens):
        # returns number of matches in form of integer
        positive = self._findMatches(data_set, tokens, 'positive')
        negative = self._findMatches(data_set, tokens, 'negative')

        #
        posLikelihood = self._calculateProbability(data_set, tokens, 'positive')
        negLikelihood = self._calculateProbability(data_set, tokens, 'negative')

        # logPos = math.log(posOtot, 2)
        # logNeg = math.log(negOtot, 2)

        if(posLikelihood > negLikelihood):
            return (posLikelihood,'positive')
        elif(posLikelihood < negLikelihood):
            return (-1*negLikelihood,'negative')
        else: return (1,'neutral')


    def train(self):
        # _splitSet(data_set)
        self._divideFeaturesByClass(self.sample)
        self.pos_neg = self._generateWordDistributionByClass(self.class_division)
        self.pos_set_size = len(self.pos_neg.get('positive'))
        self.neg_set_size = len(self.pos_neg.get('negative'))
        self.posProbability = float(self.pos_set_size)/(self.pos_set_size+self.neg_set_size)
        self.negProbability = float(self.neg_set_size)/(self.pos_set_size+self.neg_set_size)



    def classify(self, sentence):
        tokens = self._decomposeSentence(sentence)
        # print tokens
        value, label = self._getClassificationValue(self.pos_neg, tokens)
        return value


    # import twitter_api as twitter
    # import tweet_tools as twtools
    

    # print classify(data_set)
    def startUserInput(self):
        input1 = raw_input("Wanna enter something: ")
        cl = 1
        while(input1  != 'no'):
                input2 = raw_input("Please enter something: ")
                print classify(input2)
                input1


    # print normaliseDate('Tue Aug 09 19:10:50 +0000 2011')
    # for i,tweet in enumerate(twitter.getLocalData()):
    #     # print tweet
    # # print count
    # # print "_______________",sentence
    #     sentence = tweet.get('text')
    #     year = twtools.getTweetMonth(tweet)
    #     print "_______________DATE=",tweet.get('created_at')
    #     print "_______________YEAR=",year
    #
    #     print i,"______________SENTIMENT=", analysis.sentiment
    #     print "________________CLASSIFY=", classify(pos_neg,_decomposeSentence(tweet.get('text')))


    # def getAfinn():
    #     return afinn


    # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
