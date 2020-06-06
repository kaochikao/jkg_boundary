


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

關於Off-heap memory:
- Spark 1.6 开始引入了 Off-heap memory
- 这种模式`不在 JVM 内申请内存`，而是调用 Java 的 unsafe 相关 API 进行诸如 C 语言里面的 malloc() 直接向操作系统申请内存
- 好處：这种方式下 `Spark 可以直接操作系统堆外内存`，减少了不必要的内存开销，以及频繁的 `GC 扫描`和`回收`，提升了处理性能。另外，堆外内存可以被精确地申请和释放，而且序列化的数据占用的空间可以被精确计算，所以相比堆内内存来说降低了管理的难度，也降低了误差。
- 壞處：缺点是必须自己编写内存申请和释放的逻辑。
- config: 默认情况下Off-heap模式的内存并不启用，我们可以通过`spark.memory.offHeap.enabled`参数开启