# Log4J


### custom log4j config file
```sh
spark-submit \
--deploy-mode client \
--master yarn \
--executor-memory 1g \
--files /home/hadoop/custom_log4j.properties \
--conf "spark.driver.extraJavaOptions=-Dlog4j.configuration=file:///home/hadoop/custom_log4j.properties" \
--class org.apache.spark.examples.SparkPi /usr/lib/spark/examples/jars/spark-examples.jar 10
```

### 3 components of Log4J:
1. Logger: used in scripts
2. Appender: pipe log messages to devices (e.g. console, files, streams, linux syslog daemon, remote server via TCP)
3. Layout: format of log message


### directly configure logger in code
```java
import org.apache.log4j.BasicConfigurator;
import org.apache.log4j.Logger;

public class Main {
     private static Logger logger = Logger.getLogger(Main.class);

     public static void main(String[] args) {
     BasicConfigurator.configure();

     logger.info("This is an info message.");
     logger.debug("This is a debug message.");

     Logger.getRootLogger().setLevel(Level.INFO);
     Logger.getLogger(String loggerName).setLevel(Level.INFO);
 }
}
```


### Logger hierarchy
```
root
|_com
|_come.foo
|_come.foo.bar
```

child logger inherit parent logger's properties when not explicitly set

### Log Appender
- bind logger to output device 
- logger:appender = logger:deivce = 1:M

## EMR log4j config

### using variable
```
spark.yarn.app.container.log.dir=/var/log/spark/user/${user.name}
...
log4j.appender.DRFA-stderr.file=${spark.yarn.app.container.log.dir}/stderr
...
log4j.appender.DRFA-stdout.file=${spark.yarn.app.container.log.dir}/stdout
```

### General Setting Block
```
log4j.rootCategory=INFO,console
log4j.appender.console=org.apache.log4j.ConsoleAppender
log4j.appender.console.target=System.err
log4j.appender.console.layout=org.apache.log4j.PatternLayout
log4j.appender.console.layout.ConversionPattern=%d{yy/MM/dd HH:mm:ss} %p %c{1}: %m%n
```

### Special setting for spark shell, overwrite root logger's log level
```
log4j.logger.org.apache.spark.repl.Main=WARN
```

### Special Setting for Spark Streaming (for both stderr & stdout), focus on DailyRollingFileAppender (DRFA) here.
```
log4j.logger.org.apache.spark.streaming=INFO,DRFA-stderr,DRFA-stdout
log4j.appender.DRFA-stderr=org.apache.log4j.DailyRollingFileAppender
log4j.appender.DRFA-stderr.file=${spark.yarn.app.container.log.dir}/stderr
log4j.appender.DRFA-stderr.DatePattern='.'yyyy-MM-dd-HH
log4j.appender.DRFA-stderr.layout=org.apache.log4j.PatternLayout
log4j.appender.DRFA-stderr.layout.ConversionPattern=%d{ISO8601} %p [%t] %c:%m%n
```

```
/var/log/spark/user/
                    |_hadoop
                            |_stderr
                            |_stdout
                    |spark
                            |_stderr
                            |_stdout
                    |livy
                            |_stderr
                            |_stdout
```