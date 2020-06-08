"""
+---+------+--------+
| id|  type|quantity|
+---+------+--------+
|  1| apple|      23|
|  2| apple|     542|
|  3|banana|      34|
|  4|banana|      54|
|  5|banana|      32|
|  6|orange|      76|
|  7|cherry|    null|
|  8|  null|      90|
+---+------+--------+
"""

"""
>>> spark.range(1, 7, 2).show()
+---+
| id|
+---+
|  1|
|  3|
|  5|
+---+
"""

from pyspark.sql import functions as F
from pyspark.sql.types import *
# --------------------------------------------------------------------------------------------------

df = spark.read.option('header', 'true').csv(data_dir + 'dummy', inferSchema=True)
df = spark.createDataFrame([('Tom', 80), (None, 60), ('Alice', None)], ["name", "height"])
# --------------------------------------------------------------------------------------------------


schema = StructType([
    StructField("id", IntegerType()),
    StructField("type", StringType()),
    StructField("quantity", IntegerType())
])

df = spark.read.option('header', 'true').csv(data_dir + 'dummy', schema=schema)
# --------------------------------------------------------------------------------------------------

# Partition
# TODO: foreachPartition
# TODO: sortWithinPartitions
df.rdd.getNumPartitions()
df.select('*', F.spark_partition_id().alias("pid")).show()

df.where(df.type == 'apple').show() # where = filter

# Select
df.select('*', 'id').show()
df.select(f.concat(df.id, F.lit('-'), df.type).alias('s')).show()
df.select(f.format_string('%d-%s', df.id, df.type).alias('test_foramt')).show()
df.select(df.id.cast(StringType())).printSchema()
df.select("*", F.when(df.quantity > 50, 'High').when(df.quantity < 30, 'Low').otherwise('Medium').name('Q')).show()

# Filter
df.filter(df.type.contains('a')).show()
df.filter(df.type.like('app%')).show()


# Columns
df.withColumn('today', F.current_date())
df.withColumnRenamed('type', 'new_type').show()

# Aggregations
# TODO: crosstab
# TODO: cube
# TODO: join
df.groupBy('id', 'type').sum('quantity').show()
df.agg(f.countDistinct(df.id, df.type).alias('unique')).show()


# TODO: initialize a spark session

# handle missing values
df.na.drop().show()
df.na.fill('-').show()