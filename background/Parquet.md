
## Databriack Parquet video
- https://www.youtube.com/watch?v=1j8SdS7s_NY
- Content structure:
    1. parquet file physical layout
    2. Optimization
    3. Delta Lake

Questions:
- xxx.parquet.snappy 是整個file的compression還是parquet內用的page encoding?

![alt_txt](https://github.com/kaochikao/jkg_boundary/blob/master/img/parquet_layout.png)
- `Row Group` -> `Column Chunk` -> `Page`
- `Row Group` = "橫的一段table"
- 1 row group = * column chunks.
- `Column chunk` = "橫的一段column"
- 1 chunk = * pages
- Page:
    - metadata: 這裡跟整個file的footer存的metadata不一樣，不是存schema, 是比較像zone-map.
    - encoded values: 實際的data


- "row-wise physical layout ... computers don't like fragmented access patterns"
- Compression (這裡是在說每個page用的encoding): 
    - dictionary-encoding, dictionary 有一個limit size, 如果dict過大，則會fall back回plain.
    - smaller files means less I/O
- [19:17] 提到"Compression of entire pages" (?)
- Snappy:light-weight compression scheme

```
# Run Length Encoding
00000011110000
->(0,6), (1, 4), (0, 4)
-> 061404
```

### Pushdown Predicate
![alt_txt](https://github.com/kaochikao/jkg_boundary/blob/master/img/parquet_pushdown.png)
- pushdown predicate有兩個層次：
    - file-level: leverage min/max statistics = `Row Group Skipping`
        - does not work well on unsorted data!
    - directory-level: partitioning
- `Parquet Dictionary Filtering`: 直接讀“dictionary encoding”中的dictionary, 不讀actual encoded values, 因為dictionary就是該page中所有的unique values.

### the Parquet/Snappy combo
- [Is Snappy compressed Parquet file splittable?](https://boristyukin.com/is-snappy-compressed-parquet-file-splittable/)
- The short answer is yes, if you compress Parquet files with Snappy they are indeed splittable 
- First off, why should you even care about compression? A typical Hadoop job is `IO bound`, `not CPU bound`, so a light and fast compression codec will actually improve performance. 
- HDG quote: 
    - The consequence of storing the metadata in the footer is that reading a Parquet file requires an `initial seek to the end of the file` (minus 8 bytes) to read the footer metadata length, then a second seek backward by that length to read the footer metadata. 
    - Unlike sequence files and Avro datafiles, where the metadata is stored in the header and sync markers are used to separate blocks, Parquet files don’t need sync markers since the `block boundaries` are stored in the `footer metadata`. 
    - This is possible because `the metadata is written after all the blocks have been written`, so the writer can retain the block boundary positions in memory until the file is closed.
    - Therefore, `Parquet files are splittable`, since `the blocks can be located after reading the footer` and can then be processed in parallel (by MapReduce, for example).
- 注意，是snappy.parquet, 不是parquet.snappy

### Many small files:
- impact:
    - set up internal data structure.
    - parse metadata.
    - fetch files.
    - instantiate reader objects.


### Delta Lake
- storage-layer on top of Parquet in Spark
- ACID transaction
    - Data lakes typically have `multiple data pipelines reading and writing data concurrently`, and data engineers have to go through a tedious process to `ensure data integrity`, due to the lack of transactions. 
    - Delta Lake brings ACID transactions to your data lakes. It provides `serializability`, the `strongest level of isolation level`.
- Time Travel (versioning via WAL)
- https://delta.io/
- "All data in Delta Lake is stored in Apache Parquet format"
- automated repartitioning = auto-optimize
- metadata handling
    - In big data, even the metadata itself can be "big data". 
    - Delta Lake `treats metadata just like data`, leveraging Spark's distributed processing power to handle all its metadata. 
    - As a result, Delta Lake can handle petabyte-scale tables with `billions of partitions and files` at ease.



```python
# normal parquet
dataframe.write.format("parquet").save("/data")

# delta lake
dataframe.write.format("delta").save("/data")
```

### Delta Lake Questions
- 有一個抽象層的“table”? 用Hive metastore??
- 除了WAL, 其他實現的component是什麼？