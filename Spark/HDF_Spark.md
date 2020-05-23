
## HDG Spark Note

Applications, Jobs, Stages, Tasks:
- A Spark job is made up of a DAG of stages.
- Each stage is equivalent to a MR map or reduce phase.
- Stages are split into tasks by Spark runtime, just like MR tasks.
- A job always run in the context of an application (represented by a SparkContext instance)
- jobs in an application can be run either in series or in parallel, and provides the mechanism for a job to access an RDD that was cached by a previous job in the same application.
- 



- One way of telling if an operation is a transformation or an action is by looking at its return type: if the return type is RDD, then it’s a transformation; otherwise, it’s an action.
