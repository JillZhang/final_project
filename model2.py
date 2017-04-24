# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 11:36:04 2017

@author: jiang
"""
import json
from pyspark.ml.feature import HashingTF, Tokenizer, IDF
#from pyspark.mllib.regression import LabeledPoint
from pyspark.ml.classification import NaiveBayes   
from pyspark import SparkContext
from pyspark.ml import Pipeline, PipelineModel
from pyspark.sql import Row, SQLContext
from pyspark.sql.functions import col
from pyspark.sql.types import DoubleType
sc = SparkContext("local[2]", "twitter")
sqlCtx = SQLContext(sc)

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

transformed1 = documents1.map(lambda line: (extract(line),0),preservesPartitioning=True)\
                            .filter(lambda line: type(line[0]) is not None and len(line[0])>5)

documents2 = sc.textFile("/data/tweets-0.json")

transformed2 = documents2.map(lambda line: (extract(line),1),preservesPartitioning=True)\
                            .filter(lambda line: type(line[0]) is not None and len(line[0])>5)
transformed = sc.union([transformed1, transformed2])

newDF = sqlContext.createDataFrame(transformed, ["text", "label"])


dfWithLabel = newDF.withColumn("label", col("label").cast(DoubleType()))

tokenizer = Tokenizer(inputCol="text", outputCol="word")
hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="E2")
idf = IDF(inputCol=hashingTF.getOutputCol(), outputCol="features")
nb = NaiveBayes()
#create pipeline
pipeline = Pipeline(stages=[tokenizer, hashingTF,idf,nb])

model = pipeline.fit(dfWithLabel) 


#labels = transformed.map(lambda doc: doc[1],preservesPartitioning=True)
#tf = HashingTF(numFeatures=100).transform(transformed.map(lambda doc: doc[0], preservesPartitioning=True))


print "Make prediction for tweets. The tweet test is 'RT @Zareef_Osman: March Madness https://t.co/yKMAhptsCm'"

test = sc.parallelize([(1L,'RT @Zareef_Osman: March Madness https://t.co/yKMAhptsCm')])

testDF=sqlContext.createDataFrame(test,["ID","text"])

prediction = model.transform(testDF)
selected = prediction.select("prediction")
print selected.first()[0]

model.save("/program/nb-model/spark-model")
pipeline.save("/program/nb-model/unfit-model")
model = PipelineModel.load("/program/nb-model/spark-model")

#predictionAndLabel = model.predict(new_tfidf)
#print "This is a social unrest tweet 0 for no, 1 for yes",predictionAndLabel.first()
