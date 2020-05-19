## HashShuffle和SortShuffleManager实现分析

原文：https://github.com/ColZer/DigAndBuried/blob/master/spark/shuffle-hash-sort.md

- Shuffle包括`ShuffleMapStage`和`ShuffledRDD`两步骤，分别对应了Shuffle的`Map`和`Reduce`；在这两个步骤中ShuffleManager充当了很重要的角色。


### HashShuffleManager
- HashShuffleManager是Spark最早版本的ShuffleManager，该ShuffleManager的严重缺点是会`产生太多小文件`，特别是reduce个数很多时候，存在很大的性能瓶颈。
    - = (ShuffleMapTask个数) × (reduce个数)
    - 其實就是map & reduce 數的cartesian product
    - 注意，不是executor數，而是task數
- 在HashShuffleManager中,不管是否支持consolidateFiles, 同一个map的多个reduce之间都对应了不同的文件,至于对应哪个文件,是由分区函数进行Hash来确定的; 这是为什么它要叫做HashShuffleManager.


### SortShuffleManager
- 和HashShuffleManager有一个本质的差别,即同一个map的多个reduce的数据都写入到同一个文件中
- SortShuffleManager产生的Shuffle 文件个数为2*Map个数
- 不是说,每个map只对应一个文件吗?为什么要乘以2呢?下面我们来一一分析;
- 在IndexShuffleBlockManager中,针对每个Map有两个文件,一个是index文件,一个是data文件;

- 我们知道ShuffleMapStage中所有ShuffleMapTask是分散在Executor上的, 每个Map对应一个Task, Task运行结束以后, 会把MapOutput的信息保存在MapStatus返回给Driver, Driver将其`注册`到`MapOutputTrack中`; 到目前为止, ShuffleMapStage的过程就执行完成了;
- ShuffledRDD会为每个reduce创建一个分片, 对于运行在Executor A上的shuffleRDD的一个分片的Task, 为了获取该分片的对于的Reduce数据, 它需要向MapOutputTrack获取 指定ShuffleID的所有的MapStatus, 由于MapOutputTrack是一个主从结构, 获取MapStatus也涉及到Executor A请求Driver的过程. 一旦获得该Shuffle所对于的所有的MapStatus, 该Task从每个MapStatus所对应的`Map节点`(BlockManager节点)去`拉取指定reduce的数据`, 并把所有的数据组合为Iterator, 从而完成`ShuffledRDD`的compute的过程;