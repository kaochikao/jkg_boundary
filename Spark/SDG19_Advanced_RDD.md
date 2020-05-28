## Key Topics in this chapter:
1. Key-value RDDs
    - why reduceByKey is better than groupByKey
2. Custom Partitioning


## Topic 1: Key-value RDDs:
- 很多method都會要求RDD是key-value format, 也就是PairRDD type.
    - 所以必須先把RDD manipulate成這種format.


#### RDD -> PairRDD
- 2 種方式：
    1. 手動map.
    2. 用RDD keyBy method.

```scala
val words_kv = words.map(word => (word.toLowerCase, 1))
// 用第一個char當key
val keyword = words.keyBy(word => word.toLowerCase.toSeq(0).toString)
```

```python
# value為1
words_kv = words.map(lambda word: (word.lower(), 1))
#用第一個char當key
keyword = words.keyBy(lambda word: word.lower()[0])
```

#### 一些可以用於PairRDD的操作
```python

# lookup, 有點像HashMap, 但沒有enforce key必須為unique, 所以例子中會返還"Spark" & "Simple"
keyword.lookup("s")

keyword.keys().collect()
keyword.values().collect()
```

#### Why reduceByKey is better than groupByKey?
- 這邊說groupByKey會影響`stability`, 而不是說會影響`performance`，是因為只有在key skew時才會影響效能．

```scala
// 注意，groupByKey的語法是：groupByKey -> map, 而reduceByKey則是直接帶入function.
KVcharacters.groupByKey().map(row => (row._1, row._2.reduce(addFunc))).collect()

KVcharacters.reduceByKey(addFunc).collect()
```

groupByKey:
- "... `each executor` must hold all `values` for `a given key` in memory before applying the function to them. ... If you have massive `key skew`, some partitions might be completely overloaded with a ton of values for a given key, and you will get OutOfMemoryErrors." 
- "If you have `consistent value sizes` for `each key` and know that they will `fit in the memory` of a given executor, you’re going to be just fine."

reduceByKey:
- This implementation is much more stable because the reduce happens `within each partition` and doesn’t need to put everything in memory. 
- Additionally, there is `no incurred shuffle` during this operation; everything happens at each worker individually before performing a `final reduce`. 

自己的理解：
- groupBy中必須先準備"groups", shuffle好，並把整個group放在mem中等準備執行實際aggregation. 
- 而reducBy則是直接就說我要apply某個function, 所以很多事可以直接在"map-size"先完成，最後再做final reduce.
- 注意，這裡是pure RDD運算，沒有Catalyst, 沒有optimized execution plan.

##### the aggregate function

```python
# 0: start value
# maxFunc: agg func to be performed within partitions
# addFunc: agg func to be performed across partitions
nums.aggregate(0, maxFunc, addFunc)
```

- 注意，".. `aggregate` ... performs the final aggregation on the driver. "

##### CoGroup
```python
import random
distinctChars = words.flatMap(lambda word: word.lower()).distinct()
charRDD = distinctChars.map(lambda c: (c, random.random()))
charRDD2 = distinctChars.map(lambda c: (c, random.random()))
charRDD.cogroup(charRDD2).take(5)
```
- 其實就是不只groupBy 1個RDD, 可以同時JOIN 2個RDD然後group.

##### JOIN
```python
keyedChars = distinctChars.map(lambda c: (c, random.random()))
outputPartitions = 10
KVcharacters.join(keyedChars).count()
KVcharacters.join(keyedChars, outputPartitions).count()
```
- JOIN 一樣要求RDD為key-value pair

## Topic 2: Custom Partitioning:

### coalesce
```scala
words.coalesce(1).getNumPartitions // 1
```

```python
words.coalesce(1).getNumPartitions() # 1
```

### Custom Partitioner:
- Structured API 也可以使用coalesce & repartition, 但無法使用`custom partitioner`.

```python
def partitionFunc(key):
  import random
  if key == 17850 or key == 12583:
    return 0
  else:
    return random.randint(1,2)

keyedRDD = rdd.keyBy(lambda row: row[6])
keyedRDD\
  .partitionBy(3, partitionFunc)\
  .map(lambda x: x[0])\
  .glom()\
  .map(lambda x: len(set(x)))\
  .take(5)

"""
partitionBy(self, numPartitions, partitionFunc=portable_hash)
Return a copy of the RDD partitioned using the specified partitioner.
"""  
```
- 上面這個例子的情境是，customer ID為17850 & 12583的customer有很多流量，所以把他們兩個放在單獨1個partition, 其他客戶放到其他的2個partitions.
- build-in partitioners: `HashPartitioner`, `RangePartitioner`.
    - "Spark’s Structured APIs will already use these, although we can use the same thing in RDDs"
- 總之，custom partitioning的用意跟一般partitioning 一樣，就是要平均分配，避免data skew.
- "If you’re going to use `custom partitioners`, you should `drop down` to RDDs from the Structured APIs, apply your `custom partitioner`, and then convert it back to a DataFrame or Dataset. This way, you get the best of both worlds, only dropping down to custom partitioning when you need to."


[延伸] MR 裡也有Combiner & Partitioner:
- Combiner:
    - "add a combiner to reduce the amount of output from the mapper to be sent to the reducer"
    - Hadoop Combiner reduces the time taken for data transfer between mapper and reducer.
    - It decreases the amount of data that needed to be processed by the reducer.
    - `Mini-reducer`
    - `local aggregation` on the mappers’ output -> helps to minimize the data transfer between mapper and reducer
    - Pass output to `Partitioners`


- Partitioner:
    - Partitioner controls the partitioning of the keys of the intermediate map-outputs.
    - Poor partitioning of data means that some reducers will have more data input than other 
    - The Default Hadoop partitioner in Hadoop MapReduce is `Hash Partitioner` which computes a hash value for the key and assigns the partition based on this result.
    - developer 可以自己實作partitioner class (java)
    - 如果在一個例子要算first name count, group by initial, 如果知道”A”開頭的名字比較多，可以實作一個partitioner 去把A開頭的分配到一個 reducer, 其他的給另一個reducer.
    - 不然by default, 可能的情況是依據hash function，A-J開頭的被分配到一個reducer, K-Z開頭的被分配到一個reducer.
