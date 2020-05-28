
Questions:
- performance monitoring??
- 是否還是小batch? 這個batch size可以configure?
- 如何定義一個source / sink?
- streaming 會有什麼樣的action?




## 核心概念：
- 除了"streaming本身"以外的features:
    - exactly-once-processing
    - fault-tolerance: WAL, checkpointing
    - Event-Time Processing: record 進來時可能順序會亂掉
- "treat `a stream of data` as a `table` to which data is continuously appended"
- "...Internally, Structured Streaming will automatically figure out how to “incrementalize” your query.."
- 可以JOIN streaming data & offline data
- 一樣有transformation & actions.
- There is generally `only one action` available in Structured Streaming: that of `starting a stream`, which will then run continuously and output results.

## Supported Sources (Spark 2.2):
- Kafka
- Files on HDFS / S3 (read new files in a directory)
    - why Glue還沒支援？
- a socket source for testing.

## Supported Sinks (Spark 2.2):
- Kafka
- File (almost any format)
    - Q: new files in dir or new record in file????
- `foreach sink`
- dev/test
    - `console sink`
    - `memory sink`


## Output Mode:
- 3種：
    - Append (only add new records to the output sink)
    - Update (update changed records in place)
    - Complete (rewrite the full output)
- 跟batch一樣有append & overwrite, 多一個update.
- certain queries, and certain sinks, only support certain output modes

## Triggers:
- "...Whereas `output modes` define `how` data is output, `triggers` define `when` data is output..."
- By `default`, Structured Streaming will look for new input records as soon as it has finished processing the last group of input data, giving the `lowest latency possible` for new results. 
- However, this behavior can lead to writing `many small output files` when the sink is a set of files. 
- Thus, Spark also supports triggers based on `processing time` (only look for new data at a `fixed interval`). In the future, other types of triggers may also be supported.

## Event-time Processing:
- "Event-time means time fields that are embedded in your data."
    - 代表要讀payload?
- "... even if records arrive out of order at the streaming application due to `slow uploads` or `network delays`...."
- Expressing event-time processing is simple in Structured Streaming. Because the system views the input data as a table, `the event time is just another field in that table`, and your application can do grouping, aggregation, and windowing using standard SQL operators. 
- However, under the hood, Structured Streaming can take some special actions when it knows that one of your columns is an `event-time field`, including optimizing query execution or determining when it is safe to forget state about a time window. Many of these actions can be controlled using `watermarks`.


## Watermarks:
- Watermarks are a feature of streaming systems that allow you to specify `how late` they expect to see data in event time. 
    - For example, in an application that processes logs from mobile devices, one might expect logs to be up to 30 minutes late due to upload delays. 
- Systems that support event time, including Structured Streaming, usually allow setting watermarks to limit `how long they need to remember old data`. 
- Watermarks can also be used to control `when to output` a result for a particular `event time window` (e.g., waiting until the watermark for it has passed).

## 實作：
- Schema Inference:
    - Structured Streaming does not let you perform schema inference without explicitly enabling it. 
    - You can enable schema inference for this by setting the configuration `spark.sql.streaming.schemaInference` to true.

```scala
val query = activityCounts.writeStream.queryName("activity_counts").format("memory").outputMode("complete").start()
query.awaitTermination()
```