
- `pip install awswrangler`
- `python setup.py bdist_wheel`
- https://docs.aws.amazon.com/glue/latest/dg/add-job-python.html
- working dir is /tmp

```
/
total 84
drwxr-xr-x   1 root root 4096 May  6 04:40 .
drwxr-xr-x   1 root root 4096 May  6 04:40 ..
-rwxr-xr-x   1 root root    0 May  6 04:40 .dockerenv
drwxr-xr-x   2 root root 4096 Apr 28 21:12 bin
drwxr-xr-x   2 root root 4096 Aug 30  2019 boot
drwxr-x---   2 root root 4096 May  6 04:40 connection
drwxr-xr-x   5 root root  340 May  6 04:40 dev
drwxr-xr-x   1 root root 4096 May  6 04:40 etc
drwxr-xr-x   3 root root 4096 Apr 28 21:12 glue
drwxr-xr-x   2 root root 4096 Aug 30  2019 home
drwxr-xr-x   8 root root 4096 Apr 28 21:12 lib
drwxr-xr-x   2 root root 4096 Apr 28 21:12 lib64
drwxr-xr-x   2 root root 4096 Oct 14  2019 media
drwxr-xr-x   2 root root 4096 Oct 14  2019 mnt
drwxr-xr-x   3 root root 4096 Nov 11 20:54 opt
dr-xr-xr-x 112 root root    0 May  6 04:40 proc
drwxr-x---   2 root root 4096 May  6 04:40 reporting
drwx------   3 root root 4096 Apr 28 21:12 root
drwxr-xr-x   3 root root 4096 Apr 28 21:12 run
drwxr-xr-x   2 root root 4096 Apr 28 21:12 sbin
drwxr-xr-x   2 root root 4096 Oct 14  2019 srv
dr-xr-xr-x  13 root root    0 May  6 04:40 sys
drwxrwxrwt   1 root root 4096 May  6 04:40 tmp
drwxr-xr-x  10 root root 4096 Apr 28 21:12 usr
drwxr-xr-x  11 root root 4096 Apr 28 21:12 var
```

```
/tmp
total 32
drwxrwxrwt 1 root  root 4096 May  6 04:29 .
drwxr-xr-x 1 root  root 4096 May  6 04:29 ..
drwxr-xr-x 2 root  root 4096 Apr 28 21:12 bin
drwx------ 2 10000 root 4096 May  6 04:29 glue-python-scripts-ofilex1e
drwxr-xr-x 2 root  root 4096 Apr 28 21:12 include
drwxr-xr-x 3 root  root 4096 Apr 28 21:12 lib
-rwxr-xr-x 5 root  root 5969 Nov 11 18:44 runscript.py
```


在沒有任何external package的情況下

```
subprocess.call(['ls', '/tmp/lib/python3.6/site-packages'])
__pycache__
easy_install.py
pip
pip-19.3.1.dist-info
pkg_resources
setuptools
setuptools-41.6.0.dist-info
wheel
wheel-0.33.6.dist-info
```


### Job Param:
```python
# with job param: --test_key, test_val

import sys
from awsglue.utils import getResolvedOptions

args = getResolvedOptions(sys.argv,['test_key'])
print ("test_key is: ", args['test_key'])
# test_val
```


working solution (tested):
```python
import subprocess
import sys

subprocess.call(['mkdir', 'custom_lib'])
subprocess.call(['pip', 'install', '-t', '/tmp/custom_lib', 'requests'])
subprocess.call(['ls', '/tmp/custom_lib/'])

sys.path.insert(0, "/tmp/custom_lib")

import requests
```