
### Chapter結構:

- 前半部：1個Spark UI範例
- 後半部：First Aid to common issues.

- Spark 官方提供的monitoring工具就兩個選項：
    1. Spark UI
    2. Spark Logs

### Configurable Metrics:
- understanding the state of the executors is also extremely important for monitoring individual Spark jobs. 
- To help with this challenge, Spark has a `configurable metrics system` based on the `Dropwizard Metrics Library`. 
- The metrics system is configured via a `configuration file` that Spark expects to be present at `$SPARK_HOME/conf/metrics.properties`. 
- A `custom file location` can be specified by changing the `spark.metrics.conf` configuration property. 
- These metrics can be output to `a variety of different sinks`, including cluster monitoring solutions like `Ganglia`.
    - Glue的CloudWatch metrics是怎麼實現的?
    - Spark on EMR 有metrics嗎？
        - Console中的application History應該就只是跟Spark History Server一樣的東西．

### Sparl Logs:
- `spark.sparkContext.setLogLevel("INFO")`
- One challenge, however, is that `Python` won’t be able to integrate directly with `Spark’s Java-based logging library`. Using Python’s `logging` module or even simple `print` statements will still print the results to `standard error`, however, and make them easy to find.
- The logs themselves will be printed to standard error when running a local mode application, or `saved to files` by your `cluster manager` when running Spark on a cluster. Refer to each cluster manager’s documentation about how to find them — typically, they are available through the cluster manager’s web UI.

### Sparl UI:
- `Every SparkContext` running launches a web UI.
- port 4040
- If you’re running multiple applications, they will launch web UIs on increasing port numbers (4041, 4042, ...). 
- Cluster managers will also link to each application’s web UI from their own UI.

### Spark UI 範例:
- "...projection (selecting/adding/filtering columns)..."
- "Notice that in Figure 18-5 the number of output rows is six. This convienently lines up with the number of output rows multiplied by the number of partitions at aggregation time. This is because Spark performs an aggregation for each partition (in this case a hash-based aggregation) before shuffling the data around in preparation for the final stage."
    - 這句話不太懂