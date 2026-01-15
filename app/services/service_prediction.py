from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from pyspark.sql import Row


def dict_to_spark_df(data: dict, spark):
    row = Row(**data)
    return spark.createDataFrame([row])

spark = SparkSession.builder.appName("prediction_service").getOrCreate()

MODEL_PATH = "ML/spark_model"

loaded_model = PipelineModel.load(MODEL_PATH)

def predict(data: dict):
    df_silver = dict_to_spark_df(data, spark)

    prediction = loaded_model.transform(df_silver)
    prediction_value = prediction.select("prediction").collect()[0][0]
    return prediction_value


# test = {
#   "trip_distance": 5,
#   "RatecodeID": 1,
#   "fare_amount": 18,
#   "tip_amount": 3,
#   "tolls_amount": 0,
#   "total_amount": 25,
#   "Airport_fee": 0,
#   "pickup_hour": 14,
#   "month": 1
# }

# print(predict(test))