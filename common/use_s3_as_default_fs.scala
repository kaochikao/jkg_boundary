

import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.FileSystem
import org.apache.hadoop.fs.Path

val conf = new Configuration()
val OutputPath = "s3://BUCKET/"
conf.addResource(new Path("file:///etc/hadoop/conf/core-site.xml")); 
conf.addResource(new Path("file:///etc/hadoop/conf/hdfs-site.xml"));
conf.set("fs.defaultFS", OutputPath)

val fs = FileSystem.get(conf)
fs.exists(new Path("s3://BUCKET/OBJECT"))

// User class threw exception: java.lang.IllegalArgumentException: Wrong FS: s3:// ....