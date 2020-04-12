

Steps: 
- write scala class (implement UDF interface): https://medium.com/wbaa/using-scala-udfs-in-pyspark-b70033dd69b9
- compile with scalac
- "jar -cf jarfile_name.jar ."
- pyspark --jars /path/to/jar
- spark.udf.registerJavaFunction("temp_udf_name", "com.jk.spark.udf.Hello", StringType())

```scala
package com.jk.spark.udf

class Hello {

    def jk(something: String): String = {
        return "Hello " + something
    }
}
```