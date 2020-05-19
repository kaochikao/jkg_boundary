
- Manager running on every node (driver and executors) which provides interfaces for putting and retrieving blocks both locally and remotely into various stores (memory, disk, and off-heap).
- BlockManager是spark自己的存储系统，`RDD-Cache`、 `Shuffle-output`、`broadcast` 等的实现都是基于BlockManager来实现的，BlockManager也是分布式结构，在driver和所有executor上都会有blockmanager节点，每个节点上存储的block信息都会汇报给driver端的blockManagerMaster作统一管理，BlockManager对外提供get和set数据接口，可将数据存储在memory, disk, off-heap。


BlockManagerMaster服务
- BlockManagerMaster服务取名为Master其实是一个挺迷糊的名称;虽然它是Master,但是该对象并不是BlockManager的分布式服务的Master节点;而只是对Master节点一个连接符, 通过该连接符,从而已可以和真正的Master节点进行通信;不管是在Driver还是在Executor上,都有一个BlockManagerMaster.
- 最后,一句话:上面谈到了BlockManagerMaster`Actor`这个只会在Driver上创建,但是不管是在Driver还是在Slave上都会创建BlockManagerMaster; 所以取名为BlockManagerMaster很模糊.


Spark中的Block类型：
1. RDDBlock
2. ShuffleBlock
3. BroadcastBlock
4. TaskResultBlock
5. StreamBlock
6. TempBlock