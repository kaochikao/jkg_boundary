

Hi Rick,

Thanks for coming back to this, it's great to know the job was able to run successfully now. Regarding using count in the script to check whether there's any record, since count is an Action in Spark, doing a count would make Spark create an additional Spark job within the Spark Application. This will add some additional overhead. In addition, it still needs to do the calculation even though the exact number does not really matter (except for zero). Alternatively, using "df.rdd.isEmpty()" could potentially has less performance impact. 

In addition, if the objective is to prevent Spark from creating schema-only parquet files, the ideal way would be to have your data partitioned in S3 and write files with Spark's partitionBy. When writing to partitions with partitionBy, no schema-only file or empty csv file will be generated. In addition, the partitioning could benefit downstream application's reading performance greatly.

As for the issue with "cannot resolve '`meta`' given input columns", does it happen when reading the table or when running the SparkSQL query? Could you also share with us the Job Run ID? Thank you.