rdd = spark.sparkContext.parallelize([1, 2, 3])
rdd.localCheckpoint()
tmp = rdd.isLocallyCheckpointed() #True


spark.sparkContext.setCheckpointDir('s3://path/test_checkpoint/')
rdd = spark.sparkContext.parallelize([1, 2, 3])
rdd.checkpoint()
rdd.getCheckpointFile() #S3 path
rdd.isLocallyCheckpointed() #False


