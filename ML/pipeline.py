from sklearn.preprocessing import StandardScaler
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator


# split du data 

def split_data(df_silver, target, test_size=0.2, random_state=42):
    
    df_silver = df_silver.withColumnRenamed(target, "label")

    train_df, test_df = df_silver.randomSplit([1-test_size, test_size], seed=random_state)
    
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
    
    # Configurer le modèle pour utiliser les colonnes correctes
    model.setFeaturesCol("features")
    model.setLabelCol("label")
    model.setPredictionCol("prediction")
    
    return Pipeline(stages=[assembler, scaler, model])


# Metriques d'evaluation 

def metric_model(predictions):
    
    evaluator_mae = RegressionEvaluator(
        labelCol="label",
        predictionCol="prediction",
        metricName="mae"
    )
    mae = evaluator_mae.evaluate(predictions)
    
    evaluator_rmse = RegressionEvaluator(
        labelCol="label",
        predictionCol="prediction",
        metricName="rmse"
    )
    rmse = evaluator_rmse.evaluate(predictions)
   
    
    evaluator_r2 = RegressionEvaluator(
        labelCol="label",
        predictionCol="prediction",
        metricName="r2"
    )
    r2 = evaluator_r2.evaluate(predictions)
    
    return mae, rmse, r2