from pyspark.sql import SparkSession

# Создать сеанс Spark
spark = SparkSession.builder.appName( "SimplePySparkJob" ).getOrCreate()

# Считать CSV-файл в DataFrame
input_file = "size_brands.csv"
df = spark.read.csv(input_file, header= True , inferSchema= True )

df.show()

spark.stop()