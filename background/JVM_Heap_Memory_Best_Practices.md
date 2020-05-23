
## JDG Chapter 7: Heap Memory Best Practices

### 核心觀念：
- Trade-off: 2 conflicting goals:
    1. The first general rule is to `create objects sparingly` and to `discard them as quickly as possible`.
        - 謹慎create objects, 盡量少用memory.
        - 好處：memory用量少
        - 壞處：
    2. Re-use objects:
        - 好處：
        - 壞處：要re-use就必須為long-live -> impact the GC (how?)

----------------------------------------------------------------------
### Heap Space Analysis：
- 這邊有些tool不會用到，先掃過即可．
- GC logs and the tools discussed in Chapter 5 are great at understanding the impact GC has on an application, but for additional visibility, we must `look into the heap itself`. 
- The tools discussed in this section provide insight into the `objects that the application is currently using`.


```
% jcmd 8998 GC.class_histogram
8898:

 num     #instances         #bytes  class name
 ---------------------------------------------
   1:        789087       31563480  java.math.BigDecimal
   2:        237997       22617192  [C
   3:        137371       20696640  <constMethodKlass>
   4:        137371       18695208  <methodKlass>
   5:         13456       15654944  <constantPoolKlass>
   6:         13456       10331560  <instanceKlassKlass>
   7:         37059        9238848  [B
   8:         10621        8363392  <constantPoolCacheKlass>
```
- 8898是pid

----------------------------------------------------------------------
### 方向1: Use less memory：

實際方式：
1. reduce object size
2. lazy initialization of objects
3. use canonical objects

Lazy Initialization
- 以Calendar object為例，即使續用率不高，但因為it is expensive to create, 所以"保留once created"會比每次重建還要合理．
- 等於是往後推遲instantiation，直到真的需要用到時．

```java

// Eager
public class CalDateInitialization {
    private Calendar calendar = Calendar.getInstance(); // 直接instantiate
    private DateFormat df = DateFormat.getDateInstance();

    private void report(Writer w) {
        w.write("On " + df.format(calendar.getTime()) + ": " + this);
    }
}

// Lazy
public class CalDateInitialization {
    private Calendar calendar; // 先不instantiate
    private DateFormat df;

    private void report(Writer w) {
        // 當method被invoke時才去check有無instance.
        if (calendar == null) {
            calendar = Calendar.getInstance();
            df = DateFormat.getDateInstance();
        }
        w.write("On " + df.format(calendar.getTime()) + ": " + this);
    }
}
```
- 


----------------------------------------------------------------------

### Some Digest:
- Why using less memory could improve a Java program's performance? -> less GC.
- 當GC要移動object在memory中的位置時(heap compaction), 必須pause所有threads in the Java program from accessing the object.


### 延伸問題：
- thread-safe??