from pyspark.sql import SparkSession, functions as f
from pyspark.ml.regression import RandomForestRegressor
from ML.pipeline import split_data, model_pipeline

def clean_data():
    spark = SparkSession.builder.appName("Cleaning").getOrCreate()
    df = spark.read.parquet("data/bronze_dataset")
    
    # Calcul de la durée et filtres 
    df_silver = df_silver.withColumn("duration_minutes", (f.unix_timestamp("tpep_dropoff_datetime") - f.unix_timestamp("tpep_pickup_datetime")) / 60)

    # Filtrer les durees aberrantes
    df_silver = df_silver.filter(f.col("duration_minutes") > 0)
    df_silver = df_silver.filter(f.col("duration_minutes") < 180)

    # Filtrer les distances aberrantes
    df_silver = df_silver.filter(f.col("trip_distance") > 0)
    df_silver = df_silver.filter(f.col("trip_distance") < 200)


    
    # Feature Engineering
    df_silver = df_silver.withColumn("trip_duration", f.log1p("duration_minutes"))
    df_silver = df_silver.withColumn("pickup_hour", f.hour("tpep_pickup_datetime"))
    
    # Sauvegarde Silver
    df_silver.write.mode("overwrite").parquet("data/silver_dataset")
    spark.stop()


def train_model():
    spark = SparkSession.builder.appName("Training").getOrCreate()
    df_bronze= spark.read.parquet("data/silver_dataset")
    
    num_cols = [ 'trip_distance',
            'fare_amount',
            'total_amount',
            'tip_amount',
            'Airport_fee',
            'tolls_amount',]
    
    train_df, test_df = split_data(df_bronze, target="trip_duration")
    
    # Pipeline RF
    rf = RandomForestRegressor(numTrees=100)
    pipeline = model_pipeline(num_cols, rf)
    model = pipeline.fit(train_df)
    
    # Sauvegarde du modele
    model.write().overwrite().save("models/spark_model")
    spark.stop()