# Apache Arrow

## Official Definition
Apache Arrow is a cross-language development platform for in-memory data. It specifies a standardized language-independent columnar memory format for flat and hierarchical data, organized for efficient analytic operations on modern hardware.


## Analogy
- consider traveling to Europe on vacation before the EU. To visit 5 countries in 7 days, you could count on the fact that you were going to spend a few hours at the border for passport control, and you were going to lose some of your money in the currency exchange. 
- This is how working with data in-memory works without Arrow: 
    - enormous inefficiencies exist to serialize and de-serialize data structures, 
    - and a copy is made in the process, wasting precious memory and CPU resources. 
- In contrast, Arrow is like visiting Europe after the EU and the Euro: you don't wait at the border, and there are one currency is used everywhere.

The Euro zone members:
```
Calcite
Cassandra
Dremio
Drill
Hadoop
HBase
Ibis
Impala
Kudu
Pandas
Parquet
Phoenix
Spark
Storm
```


## Key Points:
- Arrow also promotes `zero-copy data sharing`. As Arrow is adopted as the internal representation in each system, one system can hand data directly to the other system for consumption. And when these systems are located on the same node, `the copy described above can also be avoided through the use of shared memory`. This means that in many cases, moving data between two systems will have no overhead.
- features a **zero serialization/ deserialization design**, allowing low-cost data movement between nodes.
- **standard in-memory representation** that every engine can use
- makes sharing of data across platforms seamless and efficient.
- Arrow combines the benefits of **columnar data structures** with **in-memory computing**. 
- It facilitates communication between many components, for example, reading a parquet file with Python (pandas) and transforming to a Spark dataframe, Falcon Data Visualization or Cassandra without worrying about conversion.



```python
import pyarrow as pa

# HDFS
host = 'x.x.x.x' # name node
port = 8022
fs = pa.hdfs.connect(host, port)

# JSON
js_df = pd.read_json('example.json')

import pyarrow.parquet as pq
pq.write_table(table, 'example.parquet')

path = 'hdfs:///iris/part-00000–71c8h2d3-fcc9–47ff-8fd1–6ef0b079f30e-c000.snappy.parquet'
table = pq.read_table(path)

from pyarrow import csv
table = csv.read_csv('example.csv')
df = table.to_pandas()
```

How Arrow is used in Spark:
- Pandas DF <-> spark DF
- Pandas UDF (a.k.a Vectorized UDFs)

Benchmarking conversion time
```python

%time 
pdf = df.toPandas()

spark.conf.set(“spark.sql.execution.arrow.enabled”, “true”)

%time 
pandas_df = df.toPandas()
pandas_df.describe()
```


## References:
- https://towardsdatascience.com/a-gentle-introduction-to-apache-arrow-with-apache-spark-and-pandas-bb19ffe0ddae
- Arrow + Spark + Tensorflow: https://databricks.com/session/accelerating-tensorflow-with-apache-arrow-on-spark-bonus-making-it-available-in-scala
- https://www.dremio.com/apache-arrow-explained/


# Wes McKinney - Apache Arrow: Leveling Up the Data Science Stack
- https://www.youtube.com/watch?v=uZA55cGDaBQ


- Arrow Project本身分為兩個部分：
    1. Memory format / protocol `specification` ("the Arrow columanr format")
        -> 定義"what is a table"
    2. `Standard Libraries` for key programming languages
- "ORC 算是Arrow的competitor"

# Parquet & Arrow
- https://www.youtube.com/watch?v=dPb2ZXnt2_U
- Parquet: Common need for `on disk` columnar.
- Arrow: Common need for `in memory` columnar.
- Arrow is building on the success of Parquet.