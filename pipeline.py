from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# split du data

def split_data(df, target, test_size=0.2, random_state=42):
    df = df.toPandas()
    x = df.drop(columns=[target])
    y = df[target]

    x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=test_size, random_state=random_state)

    return x_train, x_test, y_train, y_test


# realisation du pipiline sklearn

def model_pipeline(num_cols, model):

    numeric_transform = Pipeline(steps=[("scaler", StandardScaler())])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transform, num_cols)
        ]
    )

    return Pipeline(
        [
            ("preprocessor", preprocessor),
            ("feature_selection", SelectKBest(score_func=f_classif)),
            ("model", model)
        ]
    )



# Metriques d'evoluation

def metric_model(y_test, y_pred):
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    return mae, mse, r2