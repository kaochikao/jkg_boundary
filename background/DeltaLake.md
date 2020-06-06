


```python
# normal parquet
dataframe.write.format("parquet").save("some_path/customers/")

# delta lake
dataframe.write.format("delta").save("some_path/customers/")
```

- 使用`format("delta")`就等於create a `delta table`.
- 一個`delta table`在S3中的`實體`：
    - `some_path/customers/`路徑下除了存actual data (Parquet files), 還有metadata存在`some_path/customers/_delta_log/`
    - 如果partition by country, folder structure長這樣：
        - some_path/customers/country=TW/
        - some_path/customers/country=UK/
        - some_path/customers/country=JP/
        - some_path/customers/_delta_log/

WHY:
- https://spark.apache.org/docs/latest/sql-data-sources-load-save-functions.html#save-modes
- Sprak Doc quote: "Save operations can optionally take a SaveMode, that specifies how to handle existing data if present. It is important to realize that `these save modes do not utilize any locking and are not atomic`. Additionally, `when performing an Overwrite, the data will be deleted before writing out the new data.`"
    - 之前EMR任務就是這樣，overwrite會先刪掉s3 path, overwrite失敗也不會rollback.

## Lambda Architecture
- https://databricks.com/glossary/lambda-architecture
- New data comes continuously, as a feed to the data system. It gets fed to the batch layer and the speed layer simultaneously.
- Speed Layer (Stream Layer):
    - This layer handles the data that are `not already delivered in the batch view` due to the latency of the batch layer. 
    - In addition, it only deals with recent data in order to provide a complete view of the data to the user by creating real-time views.