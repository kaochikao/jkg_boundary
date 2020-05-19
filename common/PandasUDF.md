

## Types of Pandas UDF
1. Scalar Pandas UDF
2. Grouped Map Pandas UDF

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


### SPARK-22216
- Improving PySpark/Pandas interoperability
- This is an umbrella ticket tracking the general effort to improve performance and interoperability between PySpark and Pandas. The core idea is to use `Apache Arrow` as serialization format to reduce the overhead between PySpark and Pandas.