import pandas as pd
import sqlite3

# Cargar el archivo Excel
file_path = 'SQL_TEST.xlsx'
xls = pd.ExcelFile(file_path)

# Cargar cada hoja del archivo Excel en un DataFrame
dfs = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}

# Conectar a una base de datos SQLite en memoria
conn = sqlite3.connect(':memory:')

# Guardar cada DataFrame en la base de datos SQLite
for sheet_name, df in dfs.items():
    df.to_sql(sheet_name, conn, index=False, if_exists='replace')

# Verificar las tablas cargadas
query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = pd.read_sql(query, conn)
print(tables)

# Definir las consultas
query1 = """
WITH PurchasesCount AS (
    SELECT
        Name,
        LastName,
        Region,
        COUNT(*) AS PurchaseCount
    FROM
        Sales
    GROUP BY
        Name, LastName, Region
),
TopCustomers AS (
    SELECT
        *,
        RANK() OVER (PARTITION BY Region ORDER BY PurchaseCount DESC) AS Rank
    FROM
        PurchasesCount
)
SELECT
    Name,
    LastName,
    Region,
    PurchaseCount
FROM
    TopCustomers
WHERE
    Rank = 1;
"""

query2 = """
SELECT
    Email
FROM
    Sales
WHERE
    Gender = 'Female'
    AND ProductValue > 100;
"""

query3 = """
SELECT
    Region,
    COUNT(DISTINCT ProductID) AS NumberOfProducts,
    COUNT(DISTINCT CustomerID) AS NumberOfCustomers,
    SUM(ProductValue) AS TotalAmount
FROM
    Sales
GROUP BY
    Region;
"""

# Ejecutar las consultas y obtener los resultados
result1 = pd.read_sql(query1, conn)
result2 = pd.read_sql(query2, conn)
result3 = pd.read_sql(query3, conn)

# Mostrar los resultados
print("Query 1 Result:\n", result1)
print("\nQuery 2 Result:\n", result2)
print("\nQuery 3 Result:\n", result3)