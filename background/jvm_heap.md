
![alt_txt](https://github.com/kaochikao/jkg_boundary/blob/master/img/jvm_heap_structure.png)

## Young Generation

- Most of the `newly created objects` are located in the `Eden` memory space.
- When Eden space is filled with objects, `Minor GC` is performed and all the survivor objects are moved to `one of the survivor spaces`.
- Minor GC also checks the survivor objects and move them to the other survivor space. So at a time, one of the survivor space is always empty.
- Objects that are `survived after many cycles of GC`, are moved to the `Old generation` memory space. Usually, it’s done by setting a threshold for the `age` of the young generation objects before they become eligible to `promote` to Old generation.


## Old Generation

- Old Generation memory contains the objects that are long-lived and survived after `many rounds` of `Minor GC`. 
- Usually, garbage collection is performed in Old Generation memory when it’s full. Old Generation Garbage Collection is called `Major GC` and usually takes a longer time.


## Stop the World Event
- `All` the Garbage Collections are “Stop the World” events because all application `threads` are stopped until the operation completes.
- Since Young generation keeps short-lived objects, `Minor GC is very fast and the application doesn’t get affected by this`.
- However, Major GC takes a long time because it checks all the live objects. Major GC should be minimized because it will make your application unresponsive for the `garbage collection duration`. 

## Java Stack Memory
- Java Stack memory is used for execution of a thread. 
- They contain method specific values that are short-lived and references to other objects in the heap that is getting referred from the method.

## Some Heap Memory Switches
1. -Xms: initial heap size when JVM starts.
2. -Xmn: size of YG, the rest goes to OG.
3. -Xmx: max heap size.


## GC:
- a program running in the background.
- steps:
    1. Marking
    2. Normal Deletion
    3. Deletion with Compaction
- There are two problems with a simple mark and delete approach.
    1. First one is that it’s not efficient because most of the newly created objects will become unused
    2.Secondly objects that are in-use for multiple garbage collection cycle are most likely to be in-use for future cycles too.
- The above shortcomings with the simple approach is the reason that Java Garbage Collection is `Generational` and we have YG and OG spaces in the heap memory. I have already explained above how objects are scanned and moved from one `generational space` to another based on the Minor GC and Major GC.

![alt_txt](https://github.com/kaochikao/jkg_boundary/blob/master/img/jvm_components.png)
