import pandas as pd
import sqlite3

def execute_queries():
    """
    Executes three SQL queries on an SQLite database using data from an Excel file.

    Returns:
        result1 (DataFrame): Result of Query 1.
        result2 (DataFrame): Result of Query 2.
        result3 (DataFrame): Result of Query 3.
    """

    # Cargar el archivo Excel
    file_path = "SQL_TEST.xlsx"
    xls = pd.ExcelFile(file_path)

    # Conectar a una base de datos SQLite en memoria
    conn = sqlite3.connect(':memory:')

    # Definir las filas donde comienzan y terminan las tablas y las columnas que se deben leer
    table_ranges = {
        'Customer': ((2, 12), "B:F"),  # La tabla 'Customer comienza en la fila 3 y termina en la fila 13, y las columnas van de B a F
        'Product': ((2, 24), "I:P"),  # La tabla 'Product' comienza en la fila 3 y termina en la fila 13, y las columnas van de I a P
        'Station': ((2, 10), "R:T")  # La tabla 'Station' comienza en la fila 3 y termina en la fila 13, y las columnas van de R a T
    }

    for table_name, ((start_row, end_row), cols) in table_ranges.items():
        # Tomar el primer carácter del rango de columnas como la columna del nombre de la tabla
        table_col = cols[0]

        # Cargar el nombre de la tabla de la celda correcta
        table_name = xls.parse('SQL', header=None, nrows=1, skiprows=start_row-1, usecols=table_col).iloc[0,0]

        # Verificar que el nombre de la tabla no sea "nan"
        if pd.isnull(table_name):
            print(f"El nombre de la tabla en la fila {start_row} es 'nan', se saltará esta tabla.")
            continue

        # Cargar los nombres de las columnas de la fila siguiente
        column_names = xls.parse('SQL', header=None, nrows=1, skiprows=start_row, usecols=cols).iloc[0].tolist()

        # Cargar los datos de la tabla
        df = xls.parse('SQL', header=None, skiprows=start_row+1, nrows=end_row-start_row, usecols=cols)

        # Asignar los nombres de las columnas al DataFrame
        df.columns = column_names

        # Importar los datos del DataFrame a la tabla en la base de datos SQLite
        df.to_sql(table_name, conn, if_exists='append', index=False)

    # Definir las consultas
    # Query 1: Obtiene el nombre y apellido del cliente que ha realizado más compras en cada región (MX y USA)
    query1 = """
        WITH PurchaseCounts AS (
            SELECT 
                Customer.Customerid,
                Customer.Name,
                Customer.LastName,
                Station.Region,
                COUNT(Product.ProductID) AS PurchaseCount
            FROM 
                Customer
            JOIN 
                Product ON Customer.Customerid = Product.Customerid
            JOIN 
                Station ON Product.Stationid = Station.Stationid
            GROUP BY 
                Customer.Customerid,
                Customer.Name,
                Customer.LastName,
                Station.Region
        ),
        MaxPurchases AS (
            SELECT 
                Region,
                MAX(PurchaseCount) AS MaxPurchaseCount
            FROM 
                PurchaseCounts
            GROUP BY 
                Region
        )
        SELECT 
            PurchaseCounts.Name,
            PurchaseCounts.LastName,
            PurchaseCounts.Region,
            PurchaseCounts.PurchaseCount
        FROM 
            PurchaseCounts
        JOIN 
            MaxPurchases ON PurchaseCounts.Region = MaxPurchases.Region AND PurchaseCounts.PurchaseCount = MaxPurchases.MaxPurchaseCount;
        """

    # Query 2: Obtiene los correos electrónicos únicos de las clientes mujeres que han comprado productos con un valor superior a 100
    query2 = """
        SELECT DISTINCT
            Customer.Email
        FROM
            Customer
        JOIN
            Product ON Customer.Customerid = Product.Customerid
        WHERE
            Customer.Gender = 1  -- Filtra por clientes mujeres
            AND Product.Amount > 100;  -- Filtra por productos con un valor superior a 100
        """

    # Query 3: Obtiene el número de productos, número de clientes y el total de ventas por región
    query3 = """
        SELECT DISTINCT
            Station.Region,
            COUNT(DISTINCT Product.ProductID) AS NumberOfProducts,  -- Cuenta el número de productos únicos
            COUNT(DISTINCT Customer.Customerid) AS NumberOfCustomers,  -- Cuenta el número de clientes únicos
            SUM(Product.Amount) AS TotalAmount  -- Suma el total de ventas
        FROM
            Customer
        JOIN
            Product ON Customer.Customerid = Product.Customerid
        JOIN
            Station ON Product.Stationid = Station.Stationid
        GROUP BY
            Station.Region;  -- Agrupa los resultados por región
        """

    # Ejecutar las consultas y obtener los resultados
    result1 = pd.read_sql(query1, conn)
    result2 = pd.read_sql(query2, conn)
    result3 = pd.read_sql(query3, conn)

    return result1, result2, result3

# Ejecutar las consultas y mostrar los resultados
result1, result2, result3 = execute_queries()
print("Query 1 Result:\n", result1)
print("\nQuery 2 Result:\n", result2)
print("\nQuery 3 Result:\n", result3)