
### create dummy table:
```sql
create table customer1(
    customer_id integer,
    customer_name varchar(10)
);

create table customer2(
    customer_id integer,
    customer_name varchar(10)
);

insert into customer1 values (1, 'joey');
insert into customer1 values (2, 'john');
insert into customer1 values (3, 'jeff');

insert into customer2 select * from customer1;
```


### Enable General Logging.
#### 改config: 
- `/etc/my.cnf.d/server.cnf` (有另一個`/etc/my.cnf`)
```conf
# this is read by the standalone daemon and embedded servers
[server]
general_log_file   = /home/ec2-user/mysql/general.log
general_log        = 1
```

- 如果沒設table, 則用`select * from mysql.general_log;`會沒東西，雖然在log file裡會有．
```sql
SET GLOBAL log_output = 'FILE,TABLE';

SHOW VARIABLES LIKE "general_log%";
-- +------------------+--------------------------+
-- | Variable_name    | Value                    |
-- +------------------+--------------------------+
-- | general_log      | ON                       |
-- | general_log_file | /var/log/mysql/mysql.log |
-- +------------------+--------------------------+
```

### Ops shell cmds

#### install
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-lamp-amazon-linux-2.html
```shell
sudo yum update -y
sudo yum install -y mariadb-server
sudo mysql_secure_installation
```

```shell
mysql -u root -p
sudo systemctl start mariadb
sudo systemctl stop mariadb
sudo systemctl status mariadb
sudo systemctl restart mariadb
```

### Create User
```sql
CREATE USER 'spark-user' IDENTIFIED BY 'xxxx';
GRANT ALL PRIVILEGES ON test.* TO 'spark-user';
FLUSH PRIVILEGES;

SHOW GRANTS FOR 'spark-user';
```

### Remote Connect
```
mysql -u user_name -h ec2-xxxx.eu-west-1.compute.amazonaws.com -p
```
- 其實好像不用改config就可以remote connect了, 主要是一個user create是有無specify user@localhost, 所以似乎無法以root從remote connect. 
- 記得改security group. 

Connection string
```
jdbc:mysql://database-1.xxx.eu-west-1.rds.amazonaws.com:3306/dev
```

Ref:
- General Log: https://mariadb.com/kb/en/writing-logs-into-tables/
- General Log: https://gist.github.com/joseluisq/40ec9169669aa1848492141fa6f57fcb