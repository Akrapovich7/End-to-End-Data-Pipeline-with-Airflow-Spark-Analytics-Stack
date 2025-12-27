from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, arrays_zip, from_unixtime
from pyspark.sql.types import DateType
import os

def app():
    spark = (
        SparkSession.builder
        .appName("FormatStock")
        .master("spark://spark-master:7077")
        .config("spark.ui.enabled", "false")
        .config("fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID", "minio"))
        .config("fs.s3a.secret.key", os.getenv("AWS_SECRET_ACCESS_KEY", "minio123"))
        .config("fs.s3a.endpoint", "http://minio:9000")
        .config("fs.s3a.path.style.access", "true")
        .config("fs.s3a.connection.ssl.enabled", "false")
        .config("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .getOrCreate()
    )

    base_path = os.getenv("SPARK_APPLICATION_ARGS")

    df = spark.read.json(f"s3a://{base_path}/prices.json")

    df_exploded = (
        df.select("timestamp", explode("indicators.quote").alias("quote"))
          .select("timestamp", "quote.*")
    )

    df_zipped = (
        df_exploded
        .select(arrays_zip("timestamp", "close", "high", "low", "open", "volume").alias("z"))
        .select(explode("z").alias("c"))
        .select(
            "c.timestamp",
            "c.close",
            "c.high",
            "c.low",
            "c.open",
            "c.volume"
        )
        .withColumn("date", from_unixtime("timestamp").cast(DateType()))
    )

    df_zipped.write \
        .mode("overwrite") \
        .option("header", "true") \
        .csv(f"s3a://{base_path}/formatted_prices")

    spark.stop()

if __name__ == "__main__":
    app()
