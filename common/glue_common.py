
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

# with recurse, 
"""
in S3:
a/b1/c1/files.csv
a/b1/c2/files.csv
"""
dyf = glueContext.create_dynamic_frame.from_options(
    's3', 
    connection_options={"paths": ["s3://a/"], 'recurse':True}, 
    format='json', 
    transformation_ctx = "tmp"
)

dyf.toDF().show()