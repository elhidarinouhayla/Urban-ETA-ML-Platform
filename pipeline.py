from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator


# split du data 

def split_data(df, target, test_size=0.2, random_state=42):
    
    df = df.withColumnRenamed(target, "label")

    train_df, test_df = df.randomSplit([1-test_size, test_size], seed=random_state)
    
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














# # split du data

# def split_data(df, target, test_size=0.2, random_state=42):
#     df = df.toPandas()
#     x = df.drop(columns=[target])
#     y = df[target]

#     x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=test_size, random_state=random_state)

#     return x_train, x_test, y_train, y_test


# # realisation du pipiline sklearn

# def model_pipeline(num_cols, model):

#     numeric_transform = Pipeline(steps=[("scaler", StandardScaler())])

#     preprocessor = ColumnTransformer(
#         transformers=[
#             ("num", numeric_transform, num_cols)
#         ]
#     )

#     return Pipeline(
#         [
#             ("preprocessor", preprocessor),
#             ("model", model)
#         ]
#     )



# # Metriques d'evoluation

# def metric_model(y_test, y_pred):
#     mae = mean_absolute_error(y_test, y_pred)
#     mse = mean_squared_error(y_test, y_pred)
#     r2 = r2_score(y_test, y_pred)

#     return mae, mse, r2