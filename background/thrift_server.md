

# Apache Thrift
- cross-language service framework
    - 用於micro-service architecture
    - 原本service間溝通的方式可以用SOAP(XML) or JSON, 現在多了Thrift.
- for client / services development
- use an IDL (interface description language)
- use a compiler to generate source code.
- 寫Thrift IDL, 用Thrift compiler產生code.

## Create a Thrift-based app
- define a Thrift file: interface definition, Thrift types definitions, service definition
- our client will be able to call our services
- use Thrift compiler to generate source code.
    - `thrift --gen <language> <Thrift file>`
- Projects using Thrift: Cassandra, HBase

## Sample Thrift file
```
# time.thrift
namespace java tserver.gen
typedef i64 Timestamp

service TimeServer{
    Timestamp time()
}

# thrift --gen java time.thrift

```


# Spark Thrift Server

- HUE裡的Spark SQL是用Thrift server嗎？？
- Spark Thrift Server是Spark社区基于HiveServer2实现的一个Thrift服务。旨在无缝兼容HiveServer2。
- Spark Thrift Server大量复用了HiveServer2的代码。
- 因为Spark Thrift Server的接口和协议都和HiveServer2完全一致，因此我们部署好Spark Thrift Server后，可以直接使用hive的beeline访问Spark Thrift Server执行相关语句。
- Spark Thrift Server的目的也只是取代**HiveServer2**，因此它依旧可以和**Hive Metastore**进行交互，获取到hive的元数据。
- Spark thrift server is pretty similar to hiveserver2 thrift, rather than submitting the sql queries as hive mr job it will use spark SQL engine which underline uses full spark capabilities. As an use case tools like Tableau can easily connect to spark thrift server through ODBC driver just like hiveserver2 and access the hive or spark temp tables to run the sql queries on spark framework.
- Spark SQL can also act as a distributed query engine using its JDBC/ODBC or command-line interface. In this mode, end-users or applications can interact with Spark SQL directly to run SQL queries, without the need to write any code.
- Spark Thrift Server说白了就是小小的改动了下HiveServer2，代码量也不多。虽然接口和HiveServer2完全一致，但是它以单个Application在集群运行的方式还是比较奇葩的。可能官方也是为了实现简单而没有再去做更多的优化。


![alt_txt](https://github.com/kaochikao/jkg_boundary/blob/master/img/sparksqlthriftserver.png)

- 還是一樣使用Hive metastore, 只是跳過HiveServer2 & 背後執行的不是MR or Tez, 而是Spark core.


## Operations

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

![alt_txt](https://github.com/kaochikao/jkg_boundary/blob/master/img/spark_thrift_vs_hive.png)


Reference:
- https://blog.csdn.net/u013332124/article/details/90339850