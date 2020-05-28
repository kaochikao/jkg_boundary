Bridge: p.184 (175-201)

- Spark's language interoperability can be thought of in 2 tiers:
    1. the worker code inside your transformations (the lambda's inside of your maps)
    2. be able to specify the transformations on RDDs/Datasets.
- "the performance characteristics between the different languages are quite different once they need to execute `outside of the JVM`."
- "On the worker side, ..., if necessary will start another `process` for the target and copy the required data and result".
- "... `Unix pipes` are used for interfacing with Python code on the workers".
- "Work on both `Tungsten` and `Arrow` integration means that in the future it will be easier to work with data from Spark outside of the JVM".

- "Interacting with different `format` ... as much of Spark's load/save code is based on `Hadoop's Java interfaces`. This means that any data loaded is `initially loaded into the JVM` and then transferred to Python"
- "DataFrames and Datasets avoid many of the performance downside of the Python RDD API by keeping the data inside the JVM for as long as possible."
- "PySpark doesn't use `Jython` because it has been found that a lot of Python users need access to libraries, like numpy, scipy, and pandas, which do not work well in Jython"
- "Some early work is being investigated to see if Jython can be used to accelerate Python UDFs, which don't depend on C extensions. (SPARK-15369)"