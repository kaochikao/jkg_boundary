
原文：https://github.com/ColZer/DigAndBuried/blob/master/spark/spark-join.md


### Join原理

- IterA，IterB为`两个Iterator`，根据规则A将两个Iterator中相应的Row进行合并，然后按照规则B对合并后Row进行过滤。 比如Inner_join，它的合并规则A为：对IterA中每一条记录，生成一个key，并利用该key从`IterB`的`Map集合`中获取到相应记录，并将它们进行合并；而对于规则B可以为任意过滤条件，比如IterA和IterB任何两个字段进行比较操作。
- 对于IterA和IterB，当我们利用iterA中key去IterB中进行一一匹配时，我们称IterA为`streamedIter`，IterB为`BuildIter`或者`hashedIter`。即我们`流式遍历streamedIter中每一条记录`，`去hashedIter中去查找相应匹配的记录`。
- BuildIter也称为hashedIter，即需要将BuildIter构建为一个`内存Hash`，从而加速Build的匹配过程；此时如果BuildIter和streamedIter大小相差较大，显然利用小的来建立Hash，内存占用要小很多！
- 对于`fullouter`，IterA和IterB`同时为streamedIter和hashedIter`，即先IterA＝streamedIter，IterB＝hashedIter进行leftouter，然后再用先IterB＝streamedIter，IterA＝hashedIter进行leftouter，再把两次结果进行合并。

### HashJoin & SortJoin

- 在`HashJoin`过程中，针对BuildIter建立hashedIter是为了加速匹配过程中。`匹配查找`除了`建立Hash表`这个方法以外，将streamedIter和BuildIter进行排序，也是一个加速匹配过程，即我们这里说的sortJoin。
- 但是建立一个`Hash表`需要`占用大量的内存`。 那么问题来：如果我们的Iter太大，无法建立Hash表怎么吧？在分布式Join计算下，`Join过程中发生在Shuffle阶段`，如果一个数据集的Key存在`数据偏移`，很容易出现一个BuildIter超过内存大小，无法完成Hash表的建立，进而导致HashJoin失败
- 排序不也是需要内存吗？是的，首先`排序占用内存比建立一个hash表要小很多`，其次排序如果内存不够，可以将一部分数据Spill到磁盘，而Hash为`全内存`，如果内存不够，将会导致整个Shuffle失败。
- 对于`FullOuterJoin`，如果采用HashJoin方式来实现，代价较大，`需要建立双向的Hash表`，而基于SortJoin，它的代价与其他几种Join相差不大，因此`FullOuter`默认都是基于`SortJon`来实现。

- Spark针对Join提供了分布式实现，`但是Join操作本质上也是单机进行`，怎么理解？如果要对两个数据集进行分布式Join，Spark会先对两个数据集进行Exchange，即进行`ShuffleMap`操作，将Key相同数据分到一个分区中，然后在`ShuffleFetch`过程中利用HashJoin/SortJoin单机版算法来对两个分区进行Join操作。
- 另外如果Build端的整个数据集（非一个iter）大小较小，可以将它进行`Broadcast`操作，从而节约Shuffle的开销。

- 因此Spark支持`ShuffledHashJoinExec`, `SortMergeJoinExec`, `BroadcastHashJoinExec`三种`Join算法`，那么它怎么进行选择的呢？
    1. 如果build-dataset支持Broadcastable，并且它的大小小于`spark.sql.autoBroadcastJoinThreshold`，默认10M，那么优先进行`BroadcastHashJoinExec`
    2. 如果dataset支持Sort，并且`spark.sql.join.preferSortMergeJoin`为`True`，那么优先选择SortMergeJoinExec
    3. 如果dataset不支持Sort，那么只能选择ShuffledHashJoinExec了
        - 如果Join同时支持BuildRight和BuildLeft，那么根据两边数据大小，优先选择数据量小的进行Hash。