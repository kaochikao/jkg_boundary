

Questions:
- 如何主動影響GC行為？
- Full GC cycle vs. partial??



- One of the most attractive features of Java is that developers needn’t explicitly manage the lifecycle of objects: objects are created when needed, and when the object is no longer in use, the JVM automatically frees the object.
    - free的實際時間點是等到下次GC cycle?
- 為避免memory fragmentation, GC必須"compact the heap"
![alt_txt](https://github.com/kaochikao/jkg_boundary/blob/master/img/jvm_heap_mem_fragmentation.png)
