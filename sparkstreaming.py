import json
from pyspark.ml.feature import HashingTF, Tokenizer, IDF
from pyspark.ml.classification import NaiveBayes
from pyspark import SparkContext
from pyspark.ml import Pipeline, PipelineModel
from pyspark.sql import Row, SQLContext
from pyspark.sql.functions import col
from pyspark.sql.types import DoubleType
from pyspark.sql.streaming import StructType
from pyspark.sql import SparkSession

sc = SparkContext("local[2]", "twitter")
sqlContext = SQLContext(sc)
#from pyspark.streaming import StreamingContext
#ssc = StreamingContext(sc, 10)

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

spark = SparkSession.builder \
    .master("local") \
    .appName("Word Count") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()
userSchema = StructType().add("text", "string")
testDF = spark \
    .readStream \
    .schema(userSchema) \
    .csv("/program/test")


model = PipelineModel.load("/program/nb-model/spark-model")
#lines = ssc.textFileStream("/program/test")
#test = sc.parallelize([(1L,'RT @Zareef_Osman: March Madness https://t.co/yKMAhptsCm')])
prediction = model.transform(testDF)
selected = prediction.select("prediction")
query = selected.writeStream.format("console").start()
query.awaitTermination() 
