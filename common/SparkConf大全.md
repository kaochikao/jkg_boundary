

## Partition Overwrite Mode
```
spark.conf.set("spark.sql.sources.partitionOverwriteMode","dynamic")
```
- https://issues.apache.org/jira/browse/SPARK-20236
- by default, overwrite是對整張table. 所以，如果只要overwrite某個partition, 要用這個，不然其他partitions會被刪掉

