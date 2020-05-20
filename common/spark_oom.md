


## Executor

![alt_txt](https://github.com/kaochikao/jkg_boundary/blob/master/img/spark-executor-mem.jpg)

1. 执行内存 (Execution Memory) : 主要用于存放 Shuffle、Join、Sort、Aggregation 等`计算过程中的临时数据`；
2. 存储内存 (Storage Memory) : 主要用于存储 spark 的 cache 数据，例如`RDD的缓存`、unroll数据；
3. 用户内存（User Memory）: 主要用于存储 RDD 转换操作所需要的数据，例如 `RDD 依赖`等信息；
4. 预留内存（Reserved Memory）: 系统预留内存，会用来存储`Spark内部对象`。

Executor OOM 當下的情況：
- By default, the memory allocated for Spark executor is 1GB.
    - Glue是多少
- If the memory is not adequate this would lead to `frequent Full Garbage collection`. Full Garbage collection typically results in releasing redundant memory.
- If the amount of memory released after each `Full GC cycle` is `less than 2%` in the last `5 consecutive Full GC's`, then `JVM` will throw and `Out of Memory exception`.
```
17/06/07 11:25:00 ERROR akka.ErrorMonitor: Uncaught fatal error from thread [sparkDriverakka.
actor.default-dispatcher-29] shutting down ActorSystem [sparkDriver]
java.lang.OutOfMemoryError: Java heap space
Exception in thread "task-result-getter-0" java.lang.OutOfMemoryError: Java heap space
```
- This can `hang` the executor process and the executor would not progress. Tasks would `be eventually killed` by with below stack trace:
```
Container killed by YARN for exceeding memory limits. 12.0 GB of 12 GB physical memory used. 
Consider boosting spark.yarn.executor.memoryOverhead
```

Solution:
- Increase the Spark executor Memory. If running in Yarn, its recommended to increase the `overhead memory` as well to avoid OOM issues. Overhead memory is used for JVM threads, internal metadata etc.
```
--conf “spark.executor.memory=12g”
--conf “spark.yarn.executor.memoryOverhead=2048”
```

