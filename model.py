# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 11:36:04 2017

@author: jiang
"""
import json
from pyspark.mllib.feature import HashingTF, IDF
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import NaiveBayes   
from pyspark import SparkContext
sc = SparkContext("local[2]", "twitter")

def extract(line):    
    try:
        i = line.strip()
        o = json.loads(i)
        p = o.strip()
        q = json.loads(p)
        if 'text' not in q.keys():
            return " "
        else:
            return q['text']
    except:
        return " "

documents1 = sc.textFile("/program/sample/tweets-0.json")

transformed1 = documents1.map(lambda line: (extract(line).lower().split(""),0),preservesPartitioning=True)\
                            .filter(lambda line: type(line[0]) is not None and len(line[0])>5)

documents2 = sc.textFile("/data/tweets-0.json")

transformed2 = documents2.map(lambda line: (extract(line).lower().split(""),1),preservesPartitioning=True)\
                            .filter(lambda line: type(line[0]) is not None and len(line[0])>5)
transformed = sc.union([transformed1, transformed2])

labels = transformed.map(lambda doc: doc[1],preservesPartitioning=True)
tf = HashingTF(numFeatures=100).transform(transformed.map(lambda doc: doc[0], preservesPartitioning=True))

idf = IDF().fit(tf)
tfidf = idf.transform(tf)

training = labels.zip(tfidf).map(lambda x: LabeledPoint(x[0], x[1]))
model = NaiveBayes.train(training)


print "Make prediction for tweets. The tweet test is 'RT @Zareef_Osman: March Madness https://t.co/yKMAhptsCm'"

new_doc = sc.parallelize(['RT @Zareef_Osman: March Madness https://t.co/yKMAhptsCm'])
tf_new = HashingTF(numFeatures=100).transform(new_doc.map(lambda doc: doc.split(), preservesPartitioning=True))
new_tfidf = idf.transform(tf_new)


predictionAndLabel = model.predict(new_tfidf)
print "This is a social unrest tweet 0 for no, 1 for yes",predictionAndLabel.first()
