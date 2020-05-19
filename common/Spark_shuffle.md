## 基礎Spark Shuffle實現分析 

原文：https://github.com/ColZer/DigAndBuried/blob/master/spark/shuffle-study.md

- 在Spark中，两个RDD之间的依赖关系是Spark的核心。站在RDD的角度，两者依赖表现为点对点依赖， 但是在Spark中，RDD存在分区（partition）的概念，两个RDD之间的转换会被细化为两个RDD分区之间的转换。
![alt_txt](https://github.com/kaochikao/jkg_boundary/blob/master/img/spark_rdd_partition_dependency.jpg)
    - 所以所謂的Resilience, 是個別partition可以重算，不用重算整個RDD.
    - RDD_B对RDD_A的依赖: 窄依赖
    - RDD_D对RDD_C的依赖: 宽依赖，子RDD中的每个数据分区依赖于父RDD中的所有数据分区。

窄依赖 vs. 宽依赖:
- 实现上：对于窄依赖，rdd之间的转换可以直接pipe化，而宽依赖需要采用shuffle过程来实现。
- 任务调度上：
    - 窄依赖意味着可以在某一个计算节点上直接通过父RDD的某几块数据（通常是一块）计算得到子RDD某一块的数据； 
    - 而相对的，宽依赖意味着子RDD某一块数据的计算必须等到它的`父RDD所有数据都计算完成之后才可以进行`，而且需要对父RDD的计算结果需要经过shuffle才能被下一个rdd所操作。
- 容错恢复上：
    - 窄依赖的错误恢复会比宽依赖的错误恢复要快很多，因为对于窄依赖来说，只有丢失的那一块数据需要被重新计算，
    - 而宽依赖意味着所有的祖先RDD中所有的数据块都需要被重新计算一遍，这也是我们建议在长“血统”链条特别是有宽依赖的时候， 需要在适当的时机设置一个数据`检查点`以避免过长的容错恢复。


Shuffle執行過程：
- 上面我们谈到了Shuffle Stage,其实是`Shuffle Map`的过程,即Shuffle Stage的ShuffleTask按照一定的规则将数据写到相应的`文件`中,并把写的文件"位置信息" 以MapOutput返回给`DAGScheduler`, MapOutput将它更新到特定位置就完成了整个Shuffle Map过程.
- 在Spark中, Shuffle reduce过程抽象化为`ShuffledRDD`,即这个RDD的compute方法计算每一个分片即每一个reduce的数据是通过拉取ShuffleMap输出的文件并返回Iterator来实现的

- 首先`MapOutput`是什么? `MapStatus`; 每个Shuffle都对应一个ShuffleID,该ShuffleID下面对应多个MapID,每个MapID都会输出一个MapStatus,通过该MapStatus,可以定位每个 MapID所对应的`ShuffleMapTask`运行过程中所对应的机器;
- `MapOutputTracker`也是提供了这样的`接口`,可以把每个Map输出的MapStatus`注册到Tracker`,同时Tracker也提供了`访问接口`,可以`从该Tracker中读取指定每个ShuffleID所对应的map输出的位置`;
- MapOutputTracker: MapOutputTracker也是主从结构,其中Master提供了将Map输出注册到Tracker的入口, `slave运行在每个Executor上`, 提供读取入口, 但是这个读取过程需要和Master进行交互,将指定的 ShuffleID所对应的MapStatus信息从Master中fetch过来
- 什么时候会进行`registerShuffle`和`registerMapOutput`的注册?这里简单回答一下:在创建Stage过程中,如果遇到了ShuffleStage,那么就会进行`registerShuffle`的注册; 在上面谈到的handleTaskCompletion时候, 如果这里的Task是`ShuffleMapTask`, 就会调用`registerMapOutput`将结果进行注册;

--------------------------------------------------------------------------------------------------
Map按照什么规则进行output? -- `ShuffleManager`的实现 上面我们说每个shuffleMapStage由多个map组成,每个map将该map中属于每个reduce的数据按照一定规则输出到`文件`中,并返回MapStatus给Driver;这里还有几个问题?

1. 每个mapTask按照什么规则进行write?
2. 每个reduceTask按照什么规则进行reduce?因为每个reduceTask通过shuffleID和Reduce,只能获取一组表示map输出的mapStatus,reduce怎么从这组mapStatus读取指定 reduce的数据?

这一切都是由`ShuffleManager`来实现的. 各个公司都说自己针对Shuffle做了什么优化来提供Spark的性能,本质上就是对ShuffleManager进行优化和提供新的实现; 在1.1以后版本的Spark中ShuffleManager实现为可插拨的接口, 用户可以实现自己的ShuffleManager, 同时提供了两个默认的ShuffleManager的实现;
```scala
val shortShuffleMgrNames = Map(
      "hash" -> "org.apache.spark.shuffle.hash.HashShuffleManager",
      "sort" -> "org.apache.spark.shuffle.sort.SortShuffleManager")
val shuffleMgrName = conf.get("spark.shuffle.manager", "sort")
val shuffleMgrClass = shortShuffleMgrNames.getOrElse(shuffleMgrName.toLowerCase, shuffleMgrName)
val shuffleManager = instantiateClass[ShuffleManager](shuffleMgrClass)
```

即老版本的`HashShuffleManager`和1.1新发布的`SortShuffleManager`, 可以通过"spark.shuffle.manager""进行配置,`默认为SortShuffleManager`.

--------------------------------------------------------------------------------------------------

ShuffleManager接口
```scala
private[spark] class BaseShuffleHandle[K, V, C](
    shuffleId: Int,
    val numMaps: Int,
    val dependency: ShuffleDependency[K, V, C])
  extends ShuffleHandle(shuffleId)

private[spark] trait ShuffleManager {
  def registerShuffle(shuffleId: Int, numMaps: Int,dependency: ShuffleDependency): ShuffleHandle

  def getWriter(handle: ShuffleHandle, mapId: Int, context: TaskContext): ShuffleWriter

  def getReader(handle: ShuffleHandle,startPartition: Int,endPartition: Int,context: TaskContext): ShuffleReader
  
  def unregisterShuffle(shuffleId: Int): Boolean

  def shuffleBlockManager: ShuffleBlockManager

  def stop(): Unit
}
```