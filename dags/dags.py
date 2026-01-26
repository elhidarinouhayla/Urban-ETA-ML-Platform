from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql import SparkSession, functions as f
from pyspark.ml.regression import RandomForestRegressor

def clean_data():
    spark = SparkSession.builder.appName("Cleaning").getOrCreate()
    df = spark.read.parquet("/opt/airflow/data/bronze/bronze_dataset")
    
    # Calcul de la duree et filtres - FIXED: changed df_silver to df
    df = df.withColumn("duration_minutes", 
                       (f.unix_timestamp("tpep_dropoff_datetime") - 
                        f.unix_timestamp("tpep_pickup_datetime")) / 60)
    
    # Filtrer les durees aberrantes
    df_silver = df.filter(
        (f.col("duration_minutes") > 0) & 
        (f.col("duration_minutes") < 180) &
        (f.col("trip_distance") > 0) & 
        (f.col("trip_distance") < 200)
    )
    
    # Feature Engineering
    df_silver = df_silver.withColumn("trip_duration", f.log1p("duration_minutes"))
    df_silver = df_silver.withColumn("pickup_hour", f.hour("tpep_pickup_datetime"))
    
    # Sauvegarde Silver
    df_silver.write.mode("overwrite").parquet("/opt/airflow/data/silver/silver_dataset")
    spark.stop()

# split du data 
def split_data(df_bronze, target, test_size=0.2, random_state=42):
    df_bronze = df_bronze.withColumnRenamed(target, "label")
    train_df, test_df = df_bronze.randomSplit([1-test_size, test_size], seed=random_state)
    return train_df, test_df

# realisation du pipeline 
def model_pipeline(num_cols, model):
    # Assembler les colonnes numeriques en vecteur
    assembler = VectorAssembler(
        inputCols=num_cols,
        outputCol="features_unscaled",
        handleInvalid="skip"
    )
    
    scaler = StandardScaler(
        inputCol="features_unscaled",
        outputCol="features",
        withStd=True,
        withMean=True
    )
    
    # Configurer le modele pour utiliser les colonnes correctes
    model.setFeaturesCol("features")
    model.setLabelCol("label")
    model.setPredictionCol("prediction")
    
    return Pipeline(stages=[assembler, scaler, model])

def train_model():
    spark = SparkSession.builder.appName("Training").getOrCreate()
    df_bronze = spark.read.parquet("/opt/airflow/data/silver/silver_dataset")
    
    num_cols = [
        'trip_distance',
        'fare_amount',
        'total_amount',
        'tip_amount',
        'Airport_fee',
        'tolls_amount',
    ]
    
    train_df, test_df = split_data(df_bronze, target="trip_duration")
    
    # Pipeline RF
    rf = RandomForestRegressor(numTrees=100)
    pipeline = model_pipeline(num_cols, rf)
    model = pipeline.fit(train_df)
    
    # Sauvegarde du modele
    model.write().overwrite().save("/opt/airflow/ML/spark_model")
    spark.stop()

with DAG(
    dag_id="smart_logitrack_pipeline",
    start_date=datetime(2026, 1, 15),
    schedule_interval="@daily",
    catchup=False,
    tags=['ml', 'spark', 'logitrack']
) as dag:

    # task1 (nettoyage)
    task_clean = PythonOperator(
        task_id="clean_bronze_to_silver",
        python_callable=clean_data
    )
    
    # task2 (entrainement)
    task_train = PythonOperator(
        task_id="train_random_forest",
        python_callable=train_model
    )
    
    task_clean >> task_train