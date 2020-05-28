
### Re:Invent Talk
- https://www.slideshare.net/AmazonWebServices/metricsdriven-performance-tuning-for-aws-glue-etl-jobs-ant332-aws-reinvent-2018
- 從33頁開始有關於DyF很好的解釋．
- compute schema 會產生一個新的stage.
- 似乎關鍵點是，DyF一直delay compute schema這件事．
- applyMapping是手動去set schema, 而不是要求Spark去compute出來．
    - "`applyMapping set the schema without an additional pass`" (p. 35)
- 有些transform需要schema (似乎都是需要對整個DyF運算的)
    - DropNullFields
    - Relationalize
    - ResolveChoice (when without specifying columns)
- 似乎就是說，只要是只針對幾個column去做的transform, 根本不需要知道其他column的schema, 也就是不需要知道整張table的schema.
- 是否能想成是，當讀入input data時，其實整個data set都其實還是all strings, 必須iterate 一次去infer schema.
- 例子中，在DropNullFields前先做ApplyMapping, 就少了一個stage, 快很多．
    - 是否表示，Spark只需iterate 一次，去執行transformations就可以了
    - 無需先iterate一次，計算出schema, 再iterate一次，去做實際的工作．


Python UDF (p.38)
- 這邊似乎驗證了之前的想法
- "Using map & filter in Python is expensive for large data sets"
- "all data is serialized and sent between the JVM and Python"
- Alternatives:
    - Use Glue Scala SDK
    - Convert to DF & use SparkSQL expressions. (官方竟然也這樣說)

```python
dyf2 = Filter.apply(frame = dyf1, f = filter_function, transformation_ctx = "tmp")
```

### 官方Doc

- DataFrames are powerful and widely used, but they have limitations with respect to ETL operations. Most significantly, they `require a schema to be specified before any data is loaded`. 
- SparkSQL addresses this by making two passes over the data—the first to infer the schema, and the second to load the data. 
- However, this inference is limited and doesn't address the realities of messy data. For example, the same field might be of a different type in different records. Apache Spark often gives up and reports the type as string using the original field text. This might not be correct, and you might want finer control over how schema discrepancies are resolved. 
- And for large datasets, an additional pass over the source data might be prohibitively expensive.
    - 總之是說，infer schema又貴又太保守(?)
    - 目前的理解：初始時，用DyF去load, applyMapping再轉成DF, 應該就是直接把schema pass過去，Spark DF就不用infer了(?)
- A DynamicFrame is similar to a DataFrame, except that each record is self-describing, so `no schema is required initially`. 
- Instead, AWS Glue `computes a schema on-the-fly when required`, and explicitly encodes schema inconsistencies using a `choice` (or `union`) type. 
- You can resolve these inconsistencies to make your datasets compatible with data stores that require a fixed schema.
- `DynamicFrameReader`-> `from_rdd(data, name, schema=None, sampleRatio=None)` 這裡的sampleRatio是什麼？
    - 由於schema也是optional arg, 難道是用於infer schema的sample ratio?


```python
df = spark.read.load("examples/src/main/resources/people.csv",
                     format="csv", sep=":", inferSchema="true", header="true")
```
- 確實，從很多場景會看到當create dataframe時，schema是直接pass進去的，這樣就不用infer.
- "When you do not specify a schema or a type `when loading data`, `schema inference triggers automatically`."
