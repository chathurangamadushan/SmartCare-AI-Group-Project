from pathlib import Path
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier



# PROJECT PATHS


BASE_DIR = Path(__file__).resolve().parent

possible_dataset_paths = [
    BASE_DIR / "smartcare_ai_dataset_1000.csv",
    BASE_DIR / "data" / "smartcare_ai_dataset_1000.csv",
]

DATA_PATH = None

for path in possible_dataset_paths:
    if path.exists():
        DATA_PATH = path
        break

if DATA_PATH is None:
    raise FileNotFoundError(
        "smartcare_ai_dataset_1000.csv was not found. "
        "Place it in the project folder or inside a data folder."
    )

MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR / "smartcare_no_show_model.joblib"



#  LOAD DATA


df = pd.read_csv(DATA_PATH)

print("_" * 60)
print("SMARTCARE AI - APPOINTMENT NO-SHOW PIPELINE")
print("_" * 60)

print("\nOriginal dataset shape:", df.shape)



#  DATA CLEANING


df = df.drop_duplicates().copy()

invalid_history = (
    df["missed_previous_appointments"]
    > df["previous_appointments"]
)

print("Invalid appointment-history records:", invalid_history.sum())

df = df.loc[~invalid_history].copy()

print("Cleaned dataset shape:", df.shape)



#  FEATURE ENGINEERING


df["appointment_date"] = pd.to_datetime(
    df["appointment_date"],
    errors="coerce"
)

df["appointment_month"] = df["appointment_date"].dt.month

df["appointment_day_of_week"] = (
    df["appointment_date"].dt.day_name()
)

df["appointment_is_weekend"] = (
    df["appointment_date"]
    .dt.dayofweek
    .isin([5, 6])
    .astype(int)
)


def calculate_previous_no_show_rate(row):
    previous = row["previous_appointments"]
    missed = row["missed_previous_appointments"]

    if previous == 0:
        return 0.0

    return missed / previous


df["previous_no_show_rate"] = df.apply(
    calculate_previous_no_show_rate,
    axis=1
)

df["has_previous_no_show"] = (
    df["missed_previous_appointments"] > 0
).astype(int)



#  SELECT FEATURES


FEATURES = [
    "age",
    "gender",
    "blood_group",
    "department",
    "diagnosis",
    "waiting_days",
    "previous_appointments",
    "missed_previous_appointments",
    "previous_admissions",
    "appointment_month",
    "appointment_day_of_week",
    "appointment_is_weekend",
    "previous_no_show_rate",
    "has_previous_no_show",
]

TARGET = "no_show"

X = df[FEATURES].copy()
y = df[TARGET].copy()

print("\nNumber of model features:", len(FEATURES))
print("Target:", TARGET)

print("\nTarget distribution:")
print(y.value_counts())



#  TRAIN / TEST SPLIT


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))



#  PREPROCESSING


numerical_features = [
    "age",
    "waiting_days",
    "previous_appointments",
    "missed_previous_appointments",
    "previous_admissions",
    "appointment_is_weekend",
    "previous_no_show_rate",
    "has_previous_no_show",
]

categorical_features = [
    "gender",
    "blood_group",
    "department",
    "diagnosis",
    "appointment_month",
    "appointment_day_of_week",
]

numeric_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median"),
        ),
        (
            "scaler",
            StandardScaler(),
        ),
    ]
)

categorical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent"),
        ),
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
        ),
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            numeric_pipeline,
            numerical_features,
        ),
        (
            "cat",
            categorical_pipeline,
            categorical_features,
        ),
    ]
)



#  MODELS


models = {
    "Logistic Regression": LogisticRegression(
        C=0.01,
        solver="liblinear",
        random_state=42,
        max_iter=1000,
    ),

    "Decision Tree": DecisionTreeClassifier(
        criterion="entropy",
        max_depth=3,
        min_samples_leaf=1,
        min_samples_split=2,
        random_state=42,
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        min_samples_leaf=2,
        min_samples_split=2,
        random_state=42,
        n_jobs=-1,
    ),
}



#  TRAIN AND EVALUATE


results = []
trained_models = {}

for model_name, model in models.items():

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)
    probabilities = pipeline.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0,
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0,
    )

    roc_auc = roc_auc_score(
        y_test,
        probabilities,
    )

    cm = confusion_matrix(
        y_test,
        predictions
    )

    results.append(
        {
            "Model": model_name,
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1 Score": f1,
            "ROC-AUC": roc_auc,
        }
    )

    trained_models[model_name] = pipeline

    print("\n" + "_" * 60)
    print(model_name)
    print("_" * 60)

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print(f"ROC-AUC  : {roc_auc:.4f}")

    print("\nConfusion Matrix:")
    print(cm)



#  MODEL COMPARISON


results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="F1 Score",
    ascending=False
)

print("\n" + "_" * 60)
print("MODEL COMPARISON")
print("_" * 60)

print(
    results_df.to_string(
        index=False
    )
)



#  SAVE FINAL MODEL


best_model = trained_models[
    "Logistic Regression"
]

joblib.dump(
    best_model,
    MODEL_PATH
)

print("\n" + "_" * 60)
print("FINAL MODEL SAVED")
print("_" * 60)

print(MODEL_PATH)