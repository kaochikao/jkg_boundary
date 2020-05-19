

```
export JAVA_HOME=/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home

spark-submit --master local \
--jars lib/aws-java-sdk-1.7.4.jar,lib/jets3t-0.9.4.jar,lib/hadoop-aws-2.7.3.jar \
test2.py
```

Spark本身不支援S3, 所以要額外的jar. 手動下載jar是可行的，但關鍵是版本要對．
我用的是hadoop-aws 2.7.3，從下面maven link可以看到hadoop-aws 2.7.3對應的aws java sdk版本是1.7.4
所以原本用aws-java-sdk-1.11.30.jar就一直報錯，後來用aws-java-sdk-1.7.4.jar就可以．
hadoop-aws: https://mvnrepository.com/artifact/org.apache.hadoop/hadoop-aws/2.7.3
AWS Java SDK: https://mvnrepository.com/artifact/com.amazonaws/aws-java-sdk/1.7.4


Other references:
- https://www.philipphoffmann.de/post/spark-shell-s3a-support/
- https://gist.github.com/robcowie/ec6dde807f13a32d3e5d42db06ad55d4
- https://stackoverflow.com/questions/52310416/noclassdeffounderror-org-apache-hadoop-fs-streamcapabilities-while-reading-s3-d
- https://stackoverflow.com/questions/33574084/brew-installed-apache-spark-unable-to-access-s3-files
- https://medium.com/@mrpowers/working-with-s3-and-spark-locally-1374bb0a354