import pandas as pd

# Cargar la hoja 'E Comm' del dataset
df = pd.read_excel('E Commerce Dataset.xlsx', sheet_name='E Comm')

# Exploración inicial del dataset
# print(df.head())
# print(df.info())
# print(df.describe())

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Identificar características numéricas y categóricas
numeric_features = ['Tenure', 'WarehouseToHome', 'HourSpendOnApp', 'NumberOfDeviceRegistered', 'SatisfactionScore', 'NumberOfAddress', 'OrderAmountHikeFromlastYear', 'CouponUsed', 'OrderCount', 'DaySinceLastOrder', 'CashbackAmount']
categorical_features = ['PreferredLoginDevice', 'CityTier', 'PreferredPaymentMode', 'Gender', 'PreferedOrderCat', 'MaritalStatus', 'Complain']

# Preprocesamiento para características numéricas y categóricas
numeric_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(drop='first')

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Imprimir las columnas del DataFrame
# print(df.columns)

# Asegurarse de que la columna 'Churn' exista en el DataFrame antes de intentar eliminarla
if 'Churn' in df.columns:
    X = df.drop('Churn', axis=1)
    y = df['Churn']
else:
    print("La columna 'Churn' no existe en el DataFrame.")

# Dividir el dataset en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

# Crear un pipeline que incluye el preprocesamiento y el modelo
models = {
    'Logistic Regression': LogisticRegression(),
    'Random Forest': RandomForestClassifier()
}

for name, model in models.items():
    pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', model)])
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred)
    
    print(f"{name} - Accuracy: {accuracy:.2f}, ROC AUC: {roc_auc:.2f}")
    print(classification_report(y_test, y_pred))

# Supongamos que Random Forest es el mejor modelo
best_model = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', RandomForestClassifier())])
best_model.fit(X_train, y_train)

# Extraer la importancia de las características del modelo Random Forest
importances = best_model.named_steps['classifier'].feature_importances_
feature_names = numeric_features + list(best_model.named_steps['preprocessor'].transformers_[1][1].get_feature_names(categorical_features))

# Crear un DataFrame para visualizar la importancia de las características
feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

print(feature_importance_df)