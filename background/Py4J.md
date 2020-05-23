
## Py4J
- Py4J enables Python programs running in a Python interpreter to dynamically access Java objects in a Java Virtual Machine. Methods are called as if the Java objects resided in the Python interpreter and Java collections can be accessed through standard Python collection methods. 
- Py4J also enables Java programs to call back Python objects. (雙向的)
- Note that the Java program must be started before executing the Python code above. In other words, the Py4J does not start a JVM.



```java
import py4j.GatewayServer;

public class AdditionApplication {

  public int addition(int first, int second) {
    return first + second;
  }

  public static void main(String[] args) {
    AdditionApplication app = new AdditionApplication();
    //在Java端要instantiate server
    GatewayServer server = new GatewayServer(app);
    server.start();
  }
}
```


```python
from py4j.java_gateway import JavaGateway

# connect to JVM
gateway = JavaGateway()

# 直接使用Java class, method
random = gateway.jvm.java.util.Random()
number1 = random.nextInt(10)

# 直接使用自己定義的java class
addition_app = gateway.entry_point
value = addition_app.addition(number1, number2)
```

```python
# apache/spark/blob/master/python/pyspark/java_gateway.py
script = "./bin/spark-submit.cmd" if on_windows else "./bin/spark-submit"
command = [os.path.join(SPARK_HOME, script)]

command = command + shlex.split(submit_args)
...
proc = Popen(command, **popen_kwargs)
...
gateway = JavaGateway(
            gateway_parameters=GatewayParameters(
                port=gateway_port,
                auth_token=gateway_secret,
                auto_convert=True))

gateway.proc = proc
```

```python

# spark/python/pyspark/context.py
from pyspark.java_gateway import launch_gateway, local_connect_and_auth

...
SparkContext._ensure_initialized(self, gateway=gateway, conf=conf)
...

@classmethod
def _ensure_initialized(cls, instance=None, gateway=None, conf=None):
    """
    Checks whether a SparkContext is initialized or not.
    Throws error if a SparkContext is already running.
    """
    with SparkContext._lock:
        if not SparkContext._gateway:
            SparkContext._gateway = gateway or launch_gateway(conf)
            SparkContext._jvm = SparkContext._gateway.jvm
	...

```
