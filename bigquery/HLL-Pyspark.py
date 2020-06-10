import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import pyspark
from pyspark.sql import *
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext

import os

# create the session
from pyspark import SparkContext
sc = SparkContext("local", "HLL")
#shakespeare = sc.textFile('shakespeare.csv')

sqlContext = SQLContext(sc)
rdd = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('shakespeare.csv')
df = rdd.toDF("Words")
acd = approxCountDistinct(df.Words)


print(acd)
print("hey i have finsihed the program")
#spark.read.csv(
#    "shakespeare.csv", header=True, mode="DROPMALFORMED"
#)