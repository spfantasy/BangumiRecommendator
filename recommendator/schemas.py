from pyspark.sql.types import (
    StructType, StructField, StringType, FloatType, IntegerType, LongType, DateType)

# schema for anime infomation
animeSchema = StructType([
    StructField("id", LongType(), False),           #
    StructField("episode", IntegerType(), True),    #'话数: '
    StructField("name", StringType(), False),       #'中文名: '
    StructField("nameEN", StringType(), True),
    StructField("nameJP", StringType(), True),      #
    StructField("releaseDate", DateType(), True),   #'放送开始: '
    StructField("averageRating", FloatType(), True),#
    StructField("popularity", LongType(), True),    #
    StructField("imageURL", StringType(), True),    #
])

ratingSchema = StructType([
    StructField("userID", LongType(), False),
    StructField("animeID", LongType(), False),
    StructField("rating", IntegerType(), False),
])
