

## Types of Pandas UDF
1. Scalar Pandas UDF
2. Grouped Map Pandas UDF
3. Grouped Aggregate Pandas UDF

## 跟原本的UDF比較
寫法上其實只有function decorators不一樣，跟原本想的要pass in pandas df不一樣．
```python
from pyspark.sql.functions import udf

# Use udf to define a row-at-a-time udf
@udf('double')
# Input/output are both a single double value
def plus_one(v):
      return v + 1

df.withColumn('v2', plus_one(df.v))
```

```python
from pyspark.sql.functions import pandas_udf, PandasUDFType

# Use pandas_udf to define a Pandas UDF
@pandas_udf('double', PandasUDFType.SCALAR)
# Input/output are both a pandas.Series of doubles
def pandas_plus_one(v):
    return v + 1

df.withColumn('v2', pandas_plus_one(df.v))
```

- How `a column` is split into `multiple pandas.Series` is internal to Spark, and therefore the result of user-defined function must be independent of the splitting.


```python
import pandas as pd
from scipy import stats

@pandas_udf('double')
def cdf(v):
    return pd.Series(stats.norm.cdf(v))


df.withColumn('cumulative_probability', cdf(df.v))
```
- 這個例子就跟原本理解的UDF完全不一樣，原本不管如何serialize, 運算邏輯上都是row-by-row. 但這邊是要對整個distribution做運算．

### Grouped Map Pandas UDFs
- 串在groupby後面
- 比較：
    - Scalar: pandas.Series -> UDF -> pandas.Series
    - Group Map: pandas.DataFrame -> UDF -> pandas.DataFrame
- 注意，UDF定義中，是用`pd.Series()`, 可以看出送到Python時就是pandas df了．


```python
@pandas_udf(df.schema, PandasUDFType.GROUPED_MAP)
# Input/output are both a pandas.DataFrame
def subtract_mean(pdf):
    return pdf.assign(v=pdf.v - pdf.v.mean())

df.groupby('id').apply(subtract_mean)
```

```python
sample = df.filter(id == 1).toPandas()
# Run as a standalone function on a pandas.DataFrame and verify result
subtract_mean.func(sample)

# Now run with Spark
df.groupby('id').apply(substract_mean)
```

- The input and output of the function are both `pandas.DataFrame`. The input data contains `all the rows and columns` for each group.
- Grouped map Pandas UDFs are used with `groupBy().apply()`
- Note that `all data for a group` will be `loaded into memory` before the function is applied. This can lead to `out of memory exceptions`, especially if the group sizes are `skewed`.


### Grouped Aggregate Pandas UDFs
```python
@pandas_udf("double", PandasUDFType.GROUPED_AGG)
def mean_udf(v):
    return v.mean()

df.groupby("id").agg(mean_udf(df['v'])).show()
```

- Grouped aggregate Pandas UDFs are used with `groupBy().agg()` and `pyspark.sql.Window`.


### SPARK-22216
- Improving PySpark/Pandas interoperability
- This is an umbrella ticket tracking the general effort to improve performance and interoperability between PySpark and Pandas. The core idea is to use `Apache Arrow` as serialization format to reduce the overhead between PySpark and Pandas.

### 官方解說

原文：https://spark.apache.org/docs/latest/sql-pyspark-pandas-with-arrow.html

```python
import numpy as np
import pandas as pd

# Enable Arrow-based columnar data transfers
spark.conf.set("spark.sql.execution.arrow.enabled", "true")

# Generate a Pandas DataFrame
pdf = pd.DataFrame(np.random.rand(100, 3))

# Create a Spark DataFrame from a Pandas DataFrame using Arrow
df = spark.createDataFrame(pdf)

# Convert the Spark DataFrame back to a Pandas DataFrame using Arrow
result_pdf = df.select("*").toPandas()
```
- Using the above optimizations with Arrow will produce the same results as when Arrow is not enabled. 
- Note that even with Arrow, toPandas() results in the collection of all records in the DataFrame to the driver program and should be done on a small subset of the data. 
- Not all Spark data types are currently supported and an error can be raised if a column has an unsupported type, see Supported SQL Types. 
- If an error occurs during createDataFrame(), Spark will `fall back` to create the DataFrame `without Arrow`.
- Question: Glue 有enable by default嗎？

### Setting Arrow Batch Size
- Data partitions in Spark are converted into `Arrow record batches`, which can `temporarily` lead to `high memory usage` in the `JVM`. 
- To avoid possible OOM exceptions, the size of the `Arrow record batches` can be adjusted by setting the conf `spark.sql.execution.arrow.maxRecordsPerBatch` to an integer that will determine the maximum number of rows for each batch. 
- The default value is 10,000 records per batch. If the `number of columns` is large, the value should be adjusted accordingly. Using this limit, `each data partition` will be made into `1 or more record batches` for processing.