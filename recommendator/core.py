def loadSparkSession(name):
    from pyspark.sql import SparkSession
    spark = SparkSession.builder.appName(name).getOrCreate()
    return spark
