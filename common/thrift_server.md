

- what is Thrift?
- what is Spark Thrift server for?

# Spark Thrift Server


- Spark Thrift Server是Spark社区基于HiveServer2实现的一个Thrift服务。旨在无缝兼容HiveServer2。
- Spark Thrift Server大量复用了HiveServer2的代码。
- 因为Spark Thrift Server的接口和协议都和HiveServer2完全一致，因此我们部署好Spark Thrift Server后，可以直接使用hive的beeline访问Spark Thrift Server执行相关语句。
- Spark Thrift Server的目的也只是取代`HiveServer2`，因此它依旧可以和`Hive Metastore`进行交互，获取到hive的元数据。
- Spark thrift server is pretty similar to hiveserver2 thrift, rather than submitting the sql queries as hive mr job it will use spark SQL engine which underline uses full spark capabilities. As an use case tools like Tableau can easily connect to spark thrift server through ODBC driver just like hiveserver2 and access the hive or spark temp tables to run the sql queries on spark framework.
- Spark SQL can also act as a distributed query engine using its JDBC/ODBC or command-line interface. In this mode, end-users or applications can interact with Spark SQL directly to run SQL queries, without the need to write any code.


![alt_txt](https://github.com/kaochikao/jkg_boundary/img/sparksqlthriftserver.png)

To start the JDBC/ODBC server, run the following in the Spark directory:
```
./sbin/start-thriftserver.sh
```

Beeline:
```
./bin/beeline
beeline> !connect jdbc:hive2://localhost:10000
```
In non-secure mode, simply enter the username on your machine and a blank password. 

Spark SQL CLI (Note that the Spark SQL CLI cannot talk to the Thrift JDBC server.):
```
./bin/spark-sql
```