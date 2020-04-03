
import boto3

client = boto3.client("glue")

response = client.create_dev_endpoint(
    EndpointName=dev_endpoint_name,
    RoleArn=ROLE_ARN,
    PublicKey=PUBLIC_KEY,
    WorkerType='Standard',
    GlueVersion='1.0',
    NumberOfWorkers=NODES,
    Tags=TAGS,
    Arguments={
        "GLUE_PYTHON_VERSION": "3",
        "--enable-spark-ui": "true",
        "--spark-event-logs-path": SPARK_LOG_LOCATION
    }
)

print(response)
