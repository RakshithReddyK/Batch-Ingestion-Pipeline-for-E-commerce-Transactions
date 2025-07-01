import sys
import json
import boto3
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from awsglue.job import Job
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType

# Step 1: Job arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Step 2: Glue & Spark Context
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Step 3: Load Redshift credentials from Secrets Manager
secret_name = "redshift!redshift-ns1-admin"  
region_name = "us-east-1"
client = boto3.client('secretsmanager', region_name=region_name)
secret = json.loads(client.get_secret_value(SecretId=secret_name)['SecretString'])

username = secret['username']
password = secret['password']

# Step 4: Define schema for CSV
schema = StructType([
    StructField("transaction_id", IntegerType(), True),
    StructField("user_name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("country", StringType(), True),
    StructField("product_category", StringType(), True),
    StructField("purchase_amount", DoubleType(), True),
    StructField("payment_method", StringType(), True),
    StructField("transaction_date", TimestampType(), True)
])

# Step 5: Read and validate CSV
print("🔹 Reading CSV from S3...")
df = spark.read.option("header", "true") \
               .schema(schema) \
               .csv("s3://my-payment-pipeline-data/raw/payments/payments.csv")

print("🔹 Data preview:")
df.show(5)
df.printSchema()

# Step 6: Drop nulls, validate
df_cleaned = df.dropna(subset=["transaction_id", "user_name", "purchase_amount", "transaction_date"])

# Optional: Coalesce to 1 partition for safe write
df_cleaned = df_cleaned.coalesce(1)
df_cleaned.printSchema()


# Step 7: Write to Redshift via JDBC
print("🔹 Writing to Redshift...")
df_cleaned.limit(1000).write \
    .format("jdbc") \
    .option("url", "jdbc:redshift://redshift-wg1.700630379984.us-east-1.redshift-serverless.amazonaws.com:5439/dev") \
    .option("user", username) \
    .option("password", password) \
    .option("dbtable", "payments") \
    .option("driver", "com.amazon.redshift.jdbc42.Driver") \
    .mode("overwrite") \
    .save()

print("✅ Data loaded successfully to Redshift!")

job.commit()


