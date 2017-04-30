from pyspark.sql.types import DoubleType
from pyspark.sql.streaming import StructType
from pyspark.sql import SparkSession
from pyspark.sql.functions import window
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
from pyspark.sql.types import TimestampType
from pyspark.sql.functions import *
sc = SparkContext("local[2]", "twitter")
sqlContext = SQLContext(sc)
#from pyspark.streaming import StreamingContext
#ssc = StreamingContext(sc, 10)

def extract(line):
    try:
        i = line.strip()
        o = json.loads(i)


        if 'text' not in o.keys():
            return " "
        else:
            return o['text']
    except:
        return str("error in extract function")

bootstrapServers = '<The server host and port, it changes everytime we restart kakfa clusteer>'
subscribeType = 'subscribe'
topics = 'topic1,topic2'
spark = SparkSession.builder \
    .master("local") \
    .appName("WordCount") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

userSchema = StructType().add("text", "string")

 lines = spark\
        .readStream.schema(userSchema)\
        .format("kafka")\
        .option("kafka.bootstrap.servers", bootstrapServers)\
        .option(subscribeType, topics)\
        .option('includeTimestamp', 'true')\
        .load()\
        .selectExpr("CAST(value AS STRING)")


#testDF = spark \
#    .readStream \
#    .schema(userSchema) \
#    .csv("/program/test")
#
#
#
model = PipelineModel.load("/program/nb-model/spark-model")



#prediction = model.transform(testDF)
#selected = prediction.select("prediction")
#protest_count = lines.select(lines.value)
slen = udf(lambda s:extract(s), StringType())
test = lines.select(slen(lines.value).alias('text'),lines.timestamp.alias('time'))
prediction = model.transform(test)

aggDF = prediction.select("time","prediction").where("prediction = 1.0").withWatermark('time',"2 minutes")\
        .groupBy(window("time", "1 minutes","1 minutes")).count().orderBy('window')

#query = prediction.writeStream.format("console").start()
query2 = aggDF.writeStream.outputMode("complete").format("console").start()
#query3 = test.writeStream.format("console").start()


query2.awaitTermination()
#query3.awaitTermination()

