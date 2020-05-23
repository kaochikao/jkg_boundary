spark.executor.memory = 5g
spark.executor.cores = 4

spark.dynamicAllocation.enabled = true
spark.dynamicAllocation.maxExecutors = (depend on DPU

spark.driver.memory = 5g

spark.sql.warehouse.dir = hdfs:///user/spark/warehouse

spark.hadoop.parquet.enable.summary-metadata = false

spark.scheduler.mode = FIFO