# Best practices to scale Apache Spark jobs and partition data with AWS Glue
https://aws.amazon.com/blogs/big-data/best-practices-to-scale-apache-spark-jobs-and-partition-data-with-aws-glue/


## Worker Types:
- Standard: 
    - 16 GB mem
    - 4 vCPUs
    - 50 GB EBS storage
    - 2 Spark executors 
- G.1X:  
    - 16 GB mem
    - 4 vCPUs
    - 64 GB EBS storage
    - 1 Spark executors 
- G.2X: (相較於G.1X, 雙倍資源給1個Executor)
    - 32 GB mem
    - 8 vCPUs
    - 128 GB EBS storage
    - 1 Spark executors 


- 1 Standard worker node = 1 G.1X worker node = 1 DPU = run 8 concurrent tasks
- 1 G2.X worker node = 2 DPUs = run 16 concurrent tasks
Question: 這裡1個vCPU有幾個Cores? why 4 vCPU可以run 8 concurrent tasks??
- 總之，G系列就是1個executor獨享一整個node的資源