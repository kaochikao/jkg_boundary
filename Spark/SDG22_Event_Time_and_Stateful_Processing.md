
Structure: 
- Event Time
- Stateful Processing
- Arbitrary Stateful Processing
- Event-Time Basics
- Windows on Event Time
    - Tumbling Windows
    - Handling Late Data with Watermarks
- Dropping Duplicates in a Stream
- Arbitrary Stateful Processing
    - Time-Outs
    - Output Modes
    - mapGroupsWithState
    - flatMapGroupsWithState
- Conclusion

![alt_txt](https://github.com/kaochikao/jkg_boundary/blob/master/img/windows.png)
------------------------------------------------------------------------------------

Chapter Bridge: 
- 前半部：Spark內建的stateful processing
    - Tumbling & Sliding Windows, Watermark
- 後半部：Arbitrary Statefule Processing
    - user 自己定義的window, manage state 的方式．
    - 有些概念還不好懂

------------------------------------------------------------------------------------

- Viz: Spark在處理stream時不是一個record, 一個record做，而是會buffer一下，然後flush到persistent storage.

Event Time:
- 想像兩個streaming source, 一個在台灣，一個在美國，同時stream到美國的server, record抵達時間就很有可能不是按event time.

Stateful Processing:
- Spark stores the `intermediate information` in a `state store`. 
- Spark’s current state store implementation is an `in-memory state store` that is made `fault tolerant` by storing intermediate state to the `checkpoint directory`.
    - 主要是in-memory, 但用persistent storage提高reliability.

Arbitrary Stateful Processing:
- = custom stateful processing
- 一般的stateful processing是Spark幫你管理．這裡是你自己定義．


```python
from pyspark.sql.functions import col, window

withEventTime\
    .withWatermark('event_time', '30 minutes')\
    .groupBy(window(col('event_time'), '10 minutes', '5 minutes'))\
    .count()\
    .writeStream\
    .queryName('example')\
    .format('memory')\
    .outputMode('complete')\
    .start()
```
- configure watermark的方式幾乎就跟configure DataFrame read/write option一樣．

```python
.dropDuplicates(["User", "event_time"])\
```
- 要deduplicate也是就直接chain上去．

De-duplication:
- One of the more difficult operations in record-at-a-time systems is removing duplicates from the stream. Almost by definition, you must operate on a batch of records at a time in order to find duplicates
    - 沒錯，只看一個record怎麼會知道有重複
- deduplication是參照user-defined keys?


# Arbitrary Stateful Processing

- 上面在講的都是Spark內建的實現, Arbitrary就是user custom的實現．
- 例子：Maintain `user sessions` of an `undetermined amount of time` and save those sessions to perform some analysis on later.
    - 這就不是fixed time window.