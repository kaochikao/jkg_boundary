
from awsglue.context import GlueContext
glueConext = GlueContext(spark)


dyf = glueConext.create_dynamic_frame_from_catalog(
    database='<database>',
    table_name='<table>'
)


dyf = glueConext.create_dynamic_frame_from_options(
    connection_type='sqlserver',
    connection_options={
        "url": "jdbc:sqlserver://database-2.xxx.eu-west-1.rds.amazonaws.com:1433/test",
        "user": "admin",
        "password": "<password>",
        "dbtable": "<table>"
    }
)

dyf.toDF().show()