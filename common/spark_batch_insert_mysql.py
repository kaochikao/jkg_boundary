



url = 'jdbc:mysql://xxxx.xxxxx.eu-west-1.rds.amazonaws.com:3306/test' + '?rewriteBatchedStatements=true'


df.write \
    .format("jdbc") \
    .mode('append')\
    .option("url", url) \
    .option("driver", "com.mysql.jdbc.Driver") \
    .option("dbtable", "test") \
    .option("user", "<>") \
    .option("password", "<>") \
    .save()