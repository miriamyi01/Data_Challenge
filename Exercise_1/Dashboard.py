import streamlit as st
import requests
import pandas as pd
import json
import altair as alt
import random
import plotly.graph_objects as go

    # Function code...
def get_data_from_api(api_key):
    '''
    Retrieves data from the INEGI API.

    Parameters:
    - api_key (str): The API key for accessing the INEGI API.

    Returns:
    - data_list (list): A list of dictionaries containing the retrieved data. Each dictionary represents an observation and contains the following keys:
        - 'Indicator': The indicator code.
        - 'Year': The year of the observation.
        - 'Number': The value of the observation.

    Función para obtener los datos de la API del INEGI
    1002000001 - Población total
        1002000002 - Población total - Hombres
        1002000003 - Población total - Mujeres
    6207020032 - Porcentaje - Hombres
    6207020033 - Porcentaje - Mujeres

    6200205289 - Población de 5 años y más con religión no especificada
    6200205273 - Población de 5 años y más católica
    6200205257 - Población de 5 años y más con religión distinta de católica
    6200205256 - Población de 5 años y más sin religión
    6200240301 - Población católica
    6200240497 - Población no católica

    1002000058 - Población de 0 a 4 años
        1002000059 - Población de 0 a 4 años - Hombres
        1002000060 - Población de 0 a 4 años - Mujeres
    1002000061 - Población de 10 a 14 años
        1002000062 - Población de 10 a 14 años - Hombres
        1002000063 - Población de 10 a 14 años - Mujeres
    1002000064 - Población de 100 años y más
        1002000065 - Población de 100 años y más - Hombres
        1002000066 - Población de 100 años y más - Mujeres
    1002000067 - Población de 15 a 19 años
        1002000068 - Población de 15 a 19 años - Hombres
        1002000069 - Población de 15 a 19 años - Mujeres
    1002000070 - Población de 20 a 24 años
        1002000071 - Población de 20 a 24 años - Hombres
        1002000072 - Población de 20 a 24 años - Mujeres
    1002000073 - Población de 25 a 29 años
        1002000074 - Población de 25 a 29 años - Hombres
        1002000075 - Población de 25 a 29 años - Mujeres
    1002000076 - Población de 30 a 34 años
        1002000077 - Población de 30 a 34 años - Hombres
        1002000078 - Población de 30 a 34 años - Mujeres
    1002000079 - Población de 35 a 39 años
        1002000080 - Población de 35 a 39 años - Hombres
        1002000081 - Población de 35 a 39 años - Mujeres
    1002000082 - Población de 40 a 44 años
        1002000083 - Población de 40 a 44 años - Hombres
        1002000084 - Población de 40 a 44 años - Mujeres
    1002000085 - Población de 45 a 49 años
        1002000086 - Población de 45 a 49 años - Hombres
        1002000087 - Población de 45 a 49 años - Mujeres
    1002000088 - Población de 5 a 9 años
        1002000089 - Población de 5 a 9 años - Hombres
        1002000090 - Población de 5 a 9 años - Mujeres
    1002000091 - Población de 50 a 54 años
        1002000092 - Población de 50 a 54 años - Hombres
        1002000093 - Población de 50 a 54 años - Mujeres
    1002000094 - Población de 55 a 59 años
        1002000095 - Población de 55 a 59 años - Hombres
        1002000096 - Población de 55 a 59 años - Mujeres
    1002000097 - Población de 60 a 64 años
        1002000098 - Población de 60 a 64 años - Hombres
        1002000099 - Población de 60 a 64 años - Mujeres
    1002000100 - Población de 65 a 69 años
        1002000101 - Población de 65 a 69 años - Hombres
        1002000102 - Población de 65 a 69 años - Mujeres
    1002000103 - Población de 70 a 74 años
        1002000104 - Población de 70 a 74 años - Hombres
        1002000105 - Población de 70 a 74 años - Mujeres
    1002000106 - Población de 75 a 79 años
        1002000107 - Población de 75 a 79 años - Hombres
        1002000108 - Población de 75 a 79 años - Mujeres
    1002000109 - Población de 80 a 84 años
        1002000110 - Población de 80 a 84 años - Hombres
        1002000111 - Población de 80 a 84 años - Mujeres
    1002000112 - Población de 85 a 89 años
        1002000113 - Población de 85 a 89 años - Hombres
        1002000114 - Población de 85 a 89 años - Mujeres
    1002000115 - Población de 90 a 94 años
        1002000116 - Población de 90 a 94 años - Hombres
        1002000117 - Población de 90 a 94 años - Mujeres
    1002000118 - Población de 95 a 99 años

    1002000026 - Nacimientos registrados
    1002000030 - Defunicaciones registradas

    6200240337 - Relación divorcios - matrimonios

    6200205259 - Población nacida en otro país residente en México
    6200205268 - Población nacida en otro país residente en México hombres
    6200205284 - Población nacida en otro país residente en México mujeres
    6200205277 - Población de 5 años y más emigrante
    6200205252 - Población de 5 años y más inmigrante
    '''

    # Datos relacionados con la cantidad de población
    url_1 = f'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001,1002000002,1002000003,6207020032,6207020033/es/0700/false/BISE/2.0/{api_key}?type=json' # Género
    url_2 = f'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/6200205289,6200205273,6200205257,6200205256,6200240301,6200240497,1002000026,1002000030,1002000038,1002000039/es/0700/false/BISE/2.0/{api_key}?type=json' # Religion, natalidad, mortalidad y nupcialidad

    # Lista de todos los indicadores
    indicadores = ['1002000058', '1002000059', '1002000060', '1002000061', '1002000062', '1002000063', 
                   '1002000064', '1002000065', '1002000066', '1002000067', '1002000068', '1002000069', 
                   '1002000070', '1002000071', '1002000072', '1002000073', '1002000074', '1002000075', 
                   '1002000076', '1002000077', '1002000078', '1002000079', '1002000080', '1002000081', 
                   '1002000082', '1002000083', '1002000084', '1002000085', '1002000086', '1002000087', 
                   '1002000088', '1002000089', '1002000090', '1002000091', '1002000092', '1002000093', 
                   '1002000094', '1002000095', '1002000096', '1002000097', '1002000098', '1002000099', 
                   '1002000100', '1002000101', '1002000102', '1002000103', '1002000104', '1002000105', 
                   '1002000106', '1002000107', '1002000108', '1002000109', '1002000110', '1002000111', 
                   '1002000112', '1002000113', '1002000114', '1002000115', '1002000116', '1002000117', 
                   '1002000118', '1002000119', '1002000120', '6200205259', '6200205268', '6200205284',
                   '6200205277', '6200205252'] # Edad y migracion

    # Divide los indicadores en grupos de 5
    grupos_indicadores = [indicadores[i:i + 11] for i in range(0, len(indicadores), 11)]

    urls = [url_1, url_2]  # lista de URLs

    for grupo in grupos_indicadores:
        # Crea la URL para cada grupo de indicadores y la agrega a la lista de URLs
        urls.append(f'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/{",".join(grupo)}/es/0700/false/BISE/2.0/{api_key}?type=json')

    data_list = []  # lista para almacenar los datos

    for url in urls:  # iterar sobre las URLs
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = json.loads(response.text)  # carga la respuesta de la API

                for series in data['Series']:
                    for observation in series['OBSERVATIONS']:
                        data_dict = {}  # diccionario para almacenar los datos de cada observación
                        data_dict['Indicator'] = series['INDICADOR']
                        data_dict['Year'] = observation['TIME_PERIOD']
                        data_dict['Number'] = observation['OBS_VALUE']
                        data_list.append(data_dict)  # agrega el diccionario a la lista
            except json.decoder.JSONDecodeError:
                st.error("⛔ La respuesta no es un JSON válido")
                return []
        else:
            st.error(f'⛔ Error: {response.status_code}')
            return []

    return data_list  # devuelve la lista de diccionarios


def get_population_values(data, year):
    """
    Retrieves population values for a given year from the provided data.

    Args:
        data (DataFrame): The data containing population information.
        year (int): The year for which population values are required.

    Returns:
        tuple: A tuple containing the total population, male population, female population,
               male percentage, and female percentage for the given year. 
        
        If the required columns are not present in the data, the function returns 0 for all values.
    """

    # Comprueba si los datos tienen las columnas necesarias
    if 'Indicator' not in data.columns or 'Number' not in data.columns or 'Year' not in data.columns:
        return 0, 0, 0

    # Filtra los datos para el año seleccionado
    data = data[data['Year'] == year]

    # Filtra los datos para obtener la población total, hombres y mujeres
    total_population = data[data['Indicator'] == '1002000001']['Number'].sum()
    male_population = data[data['Indicator'] == '1002000002']['Number'].sum()
    female_population = data[data['Indicator'] == '1002000003']['Number'].sum()
    male_percentage = data[data['Indicator'] == '6207020032']['Number'].sum()
    female_percentage = data[data['Indicator'] == '6207020033']['Number'].sum()

    return total_population, male_population, female_population, male_percentage, female_percentage


def get_religion_values(data, year):
    """
    Retrieves the values of different religion indicators for a given year from the provided data.

    Args:
        data (DataFrame): The data containing religion indicators.
        year (int): The year for which the values are to be retrieved.

    Returns:
        tuple: A tuple containing the following values:
            - inespecific_religion (int): The sum of values for the 'inespecific religion' indicator.
            - catolical_religion (int): The sum of values for the 'catolical religion' indicator.
            - diferent_religion (int): The sum of values for the 'different religion' indicator.
            - no_religion (int): The sum of values for the 'no religion' indicator.
            - catholic_population (int): The sum of values for the 'catholic population' indicator.
            - uncatolical_population (int): The sum of values for the 'uncatolical population' indicator.

        If the required columns are not present in the data, the function returns 0 for all values.
    """
    # Comprueba si los datos tienen las columnas necesarias
    if 'Indicator' not in data.columns or 'Number' not in data.columns or 'Year' not in data.columns:
        return 0, 0, 0

    # Filtra los datos para el año seleccionado
    data = data[data['Year'] == year]

    inespecific_religion = data[data['Indicator'] == '6200205289']['Number'].sum()
    catolical_religion = data[data['Indicator'] == '6200205273']['Number'].sum()
    diferent_religion = data[data['Indicator'] == '6200205257']['Number'].sum()
    no_religion = data[data['Indicator'] == '6200205256']['Number'].sum()
    catholic_population = data[data['Indicator'] == '6200240301']['Number'].sum()
    uncatolical_population = data[data['Indicator'] == '6200240497']['Number'].sum()

    return inespecific_religion, catolical_religion, diferent_religion, no_religion, catholic_population, uncatolical_population


def get_live_values(data, year):
    """
    Retrieves the total number of births and deaths for a given year from the provided data.

    Args:
        data (DataFrame): The data containing information about births and deaths.
        year (int): The year for which to retrieve the data.

    Returns:
        tuple: A tuple containing the total number of births and deaths for the specified year.
    """
    # Comprueba si los datos tienen las columnas necesarias
    if 'Indicator' not in data.columns or 'Number' not in data.columns or 'Year' not in data.columns:
        return 0, 0, 0

    # Filtra los datos para el año seleccionado
    data = data[data['Year'] == year]

    births = data[data['Indicator'] == '1002000026']['Number'].sum()
    deaths = data[data['Indicator'] == '1002000030']['Number'].sum()

    return births, deaths


def get_age_values(data, year):
    """
    Calculates the sum of population numbers for different age groups and genders for a given year.

    Args:
        data (DataFrame): The input data containing columns 'Indicator', 'Number', and 'Year'.
        year (int): The year for which the population numbers are calculated.

    Returns:
        tuple: A tuple containing the sum of population numbers for different age groups and genders.
    """

    # Comprueba si los datos tienen las columnas necesarias
    if 'Indicator' not in data.columns or 'Number' not in data.columns or 'Year' not in data.columns:
        return 0, 0, 0

    # Filtra los datos para el año seleccionado
    data = data[data['Year'] == year]
    
    population_0_4 = data[data['Indicator'] == '1002000058']['Number'].sum()
    population_0_4_males = data[data['Indicator'] == '1002000059']['Number'].sum()
    population_0_4_females = data[data['Indicator'] == '1002000060']['Number'].sum()
    
    population_10_14 = data[data['Indicator'] == '1002000061']['Number'].sum()
    population_10_14_males = data[data['Indicator'] == '1002000062']['Number'].sum()
    population_10_14_females = data[data['Indicator'] == '1002000063']['Number'].sum()

    population_100_plus = data[data['Indicator'] == '1002000064']['Number'].sum()
    population_100_plus_males = data[data['Indicator'] == '1002000065']['Number'].sum()
    population_100_plus_females = data[data['Indicator'] == '1002000066']['Number'].sum()

    population_15_19 = data[data['Indicator'] == '1002000067']['Number'].sum()
    population_15_19_males = data[data['Indicator'] == '1002000068']['Number'].sum()
    population_15_19_females = data[data['Indicator'] == '1002000069']['Number'].sum()
    
    population_20_24 = data[data['Indicator'] == '1002000070']['Number'].sum()
    population_20_24_males = data[data['Indicator'] == '1002000071']['Number'].sum()
    population_20_24_females = data[data['Indicator'] == '1002000072']['Number'].sum()
    
    population_25_29 = data[data['Indicator'] == '1002000073']['Number'].sum()
    population_25_29_males = data[data['Indicator'] == '1002000074']['Number'].sum()
    population_25_29_females = data[data['Indicator'] == '1002000075']['Number'].sum()

    population_30_34 = data[data['Indicator'] == '1002000076']['Number'].sum()
    population_30_34_males = data[data['Indicator'] == '1002000077']['Number'].sum()
    population_30_34_females = data[data['Indicator'] == '1002000078']['Number'].sum()

    population_35_39 = data[data['Indicator'] == '1002000079']['Number'].sum()
    population_35_39_males = data[data['Indicator'] == '1002000080']['Number'].sum()
    population_35_39_females = data[data['Indicator'] == '1002000081']['Number'].sum()

    population_40_44 = data[data['Indicator'] == '1002000082']['Number'].sum()
    population_40_44_males = data[data['Indicator'] == '1002000083']['Number'].sum()
    population_40_44_females = data[data['Indicator'] == '1002000084']['Number'].sum()

    population_45_49 = data[data['Indicator'] == '1002000085']['Number'].sum()
    population_45_49_males = data[data['Indicator'] == '1002000086']['Number'].sum()
    population_45_49_females = data[data['Indicator'] == '1002000087']['Number'].sum()

    population_5_9 = data[data['Indicator'] == '1002000088']['Number'].sum()
    population_5_9_males = data[data['Indicator'] == '1002000089']['Number'].sum()
    population_5_9_females = data[data['Indicator'] == '1002000090']['Number'].sum()

    population_50_54 = data[data['Indicator'] == '1002000091']['Number'].sum()
    population_50_54_males = data[data['Indicator'] == '1002000092']['Number'].sum()
    population_50_54_females = data[data['Indicator'] == '1002000093']['Number'].sum()

    population_55_59 = data[data['Indicator'] == '1002000094']['Number'].sum()
    population_55_59_males = data[data['Indicator'] == '1002000095']['Number'].sum()
    population_55_59_females = data[data['Indicator'] == '1002000096']['Number'].sum()

    population_60_64 = data[data['Indicator'] == '1002000097']['Number'].sum()
    population_60_64_males = data[data['Indicator'] == '1002000098']['Number'].sum()
    population_60_64_females = data[data['Indicator'] == '1002000099']['Number'].sum()

    population_65_69 = data[data['Indicator'] == '1002000100']['Number'].sum()
    population_65_69_males = data[data['Indicator'] == '1002000101']['Number'].sum()
    population_65_69_females = data[data['Indicator'] == '1002000102']['Number'].sum()

    population_70_74 = data[data['Indicator'] == '1002000103']['Number'].sum()
    population_70_74_males = data[data['Indicator'] == '1002000104']['Number'].sum()
    population_70_74_females = data[data['Indicator'] == '1002000105']['Number'].sum()

    population_75_79 = data[data['Indicator'] == '1002000106']['Number'].sum()
    population_75_79_males = data[data['Indicator'] == '1002000107']['Number'].sum()
    population_75_79_females = data[data['Indicator'] == '1002000108']['Number'].sum()

    population_80_84 = data[data['Indicator'] == '1002000109']['Number'].sum()
    population_80_84_males = data[data['Indicator'] == '1002000110']['Number'].sum()
    population_80_84_females = data[data['Indicator'] == '1002000111']['Number'].sum()

    population_85_89 = data[data['Indicator'] == '1002000112']['Number'].sum()
    population_85_89_males = data[data['Indicator'] == '1002000113']['Number'].sum()
    population_85_89_females = data[data['Indicator'] == '1002000114']['Number'].sum()

    population_90_94 = data[data['Indicator'] == '1002000115']['Number'].sum()
    population_90_94_males = data[data['Indicator'] == '1002000116']['Number'].sum()
    population_90_94_females = data[data['Indicator'] == '1002000117']['Number'].sum()

    population_95_99 = data[data['Indicator'] == '1002000118']['Number'].sum()
    population_95_99_males = data[data['Indicator'] == '1002000119']['Number'].sum()
    population_95_99_females = data[data['Indicator'] == '1002000120']['Number'].sum()

    return (population_0_4, population_0_4_males, population_0_4_females, 
        population_5_9, population_5_9_males, population_5_9_females,
        population_10_14, population_10_14_males, population_10_14_females, 
        population_15_19, population_15_19_males, population_15_19_females, 
        population_20_24, population_20_24_males, population_20_24_females, 
        population_25_29, population_25_29_males, population_25_29_females,
        population_30_34, population_30_34_males, population_30_34_females,
        population_35_39, population_35_39_males, population_35_39_females,
        population_40_44, population_40_44_males, population_40_44_females,
        population_45_49, population_45_49_males, population_45_49_females,
        population_50_54, population_50_54_males, population_50_54_females,
        population_55_59, population_55_59_males, population_55_59_females,
        population_60_64, population_60_64_males, population_60_64_females,
        population_65_69, population_65_69_males, population_65_69_females,
        population_70_74, population_70_74_males, population_70_74_females,
        population_75_79, population_75_79_males, population_75_79_females,
        population_80_84, population_80_84_males, population_80_84_females,
        population_85_89, population_85_89_males, population_85_89_females,
        population_90_94, population_90_94_males, population_90_94_females,
        population_95_99, population_95_99_males, population_95_99_females,
        population_100_plus, population_100_plus_males, population_100_plus_females)


def get_nupcial_values(data, year):
    """
    Retrieves the sum of 'Number' values for the 'Indicator' '6200240337' in the given year.

    Args:
        data (DataFrame): The input data containing the necessary columns: 'Indicator', 'Number', and 'Year'.
        year (int): The year for which to retrieve the data.

    Returns:
        int: The sum of 'Number' values for the 'Indicator' '6200240337' in the given year.
    """
    # Comprueba si los datos tienen las columnas necesarias
    if 'Indicator' not in data.columns or 'Number' not in data.columns or 'Year' not in data.columns:
        return 0, 0, 0

    # Filtra los datos para el año seleccionado
    data = data[data['Year'] == year]

    marriages = data[data['Indicator'] == '1002000038']['Number'].sum()
    divorces = data[data['Indicator'] == '1002000039']['Number'].sum()

    return marriages, divorces

def get_migration_values(data, year):
    # Comprueba si los datos tienen las columnas necesarias
    if 'Indicator' not in data.columns or 'Number' not in data.columns or 'Year' not in data.columns:
        return 0, 0, 0

    # Filtra los datos para el año seleccionado
    data = data[data['Year'] == year]

    poblacion_5_anos_inmigrante = data[data['Indicator'] == '6200205252']['Number'].sum()
    poblacion_5_anos_emigrante = data[data['Indicator'] == '6200205277']['Number'].sum()
    poblacion_nacida_otro_pais_residente_mexico = data[data['Indicator'] == '6200205259']['Number'].sum()
    poblacion_nacida_otro_pais_residente_mexico_hombres = data[data['Indicator'] == '6200205268']['Number'].sum()
    poblacion_nacida_otro_pais_residente_mexico_mujeres = data[data['Indicator'] == '6200205284']['Number'].sum()

    return poblacion_5_anos_inmigrante, poblacion_5_anos_emigrante, poblacion_nacida_otro_pais_residente_mexico, poblacion_nacida_otro_pais_residente_mexico_hombres, poblacion_nacida_otro_pais_residente_mexico_mujeres

def create_text(plot, align, dy, input_response, input_text):
    input_response = str(int(round(float(input_response))))
    return plot.mark_text(
        align=align,
        dy=dy,
        fontSize=20, 
        fontWeight=700
    ).encode(
        text=alt.value(f'{input_response}%'),
        theta=alt.Theta(field="% value", type="quantitative", stack=True)
    ).transform_filter(
        alt.datum.Topic == input_text
    )


def make_donut(input_response1, input_text1, input_color1, input_response2, input_text2, input_color2):

    chart_color = [input_color1, input_color2]
        
    source = pd.DataFrame({
        "Topic": [input_text1, input_text2],
        "% value": [input_response1, input_response2]
    })
        
    plot = alt.Chart(source).mark_arc(innerRadius=50, cornerRadius=10).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            domain=[input_text1, input_text2],
                            range=chart_color),
                        legend=None),
    ).properties(width=150, height=150)
    
    text1 = create_text(plot, 'right', 10, input_response1, input_text1)
    text2 = create_text(plot, 'left', -10, input_response2, input_text2)

    return plot + text1 + text2


def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'

def convert_to_float_and_format(data):
    return format_number(float(data))

def calculate_percentage(data):
    return round(float(data), 2)


def main():
    """
    This function is the entry point of the dashboard application.
    It sets the page configuration, enables the dark theme, retrieves data from an API,
    and displays various visualizations and metrics based on the selected data.

    Parameters:
        None

    Returns:
        None
    """
    st.set_page_config(
        page_title="México Población - Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    alt.themes.enable("dark")

    api_key = 'cc1b4dab-8051-3e70-b972-3d32758dcd7b'
    data_list = get_data_from_api(api_key)
    if data_list:
        for data_dict in data_list:
            number = float(data_dict['Number'])
            if number.is_integer():
                number = int(number)
            # st.write(f"Indicador: {data_dict['Indicator']}, Año: {data_dict['Year']}, Numero: {number}")

    with st.sidebar:
        st.title('👤 México Población - Dashboard')
        
        # Crea una lista de todos los años únicos en los datos
        year_list = list(set(data_dict['Year'] for data_dict in data_list))
        year_list.sort(reverse=True)

        # Crea un cuadro de selección para el año
        selected_year = st.selectbox('Selecciona el año', year_list)

        # Filtra los datos para el año seleccionado
        selected_data = [data_dict for data_dict in data_list if data_dict['Year'] == selected_year]

        for data_dict in selected_data:
            number = float(data_dict['Number'])
            if number.is_integer():
                number = int(number)
            # st.write(f"Year: {data_dict['Year']}, Number: {number}, Indicator: {data_dict['Indicator']}")

    col = st.columns((1, 1, 1), gap='medium')

    with col[0]:
        # Convierte selected_data en un DataFrame de pandas
        data = pd.DataFrame(selected_data)

        total_population, male_population, female_population, male_percentage, female_percentage = get_population_values(data, selected_year)
        
        # Convierte los valores a números y formatea
        formatted_population = convert_to_float_and_format(total_population)
        formatted_male_population = convert_to_float_and_format(male_population)
        formatted_female_population = convert_to_float_and_format(female_population)
        
        # Porcentajes de la población masculina y femenina
        male_percentage = calculate_percentage(male_percentage)
        female_percentage = calculate_percentage(female_percentage)

        births, deaths = get_live_values(data, selected_year)

        formatted_births = convert_to_float_and_format(births)
        formatted_deaths = convert_to_float_and_format(deaths)

        # Muestra los valores en las métricas
        st.metric(label="Población Total", value=formatted_population)


        st.markdown('### MORTALIDAD Y NATALIDAD')
        
        col1, col2 = st.columns(2)
        difference_birth = float(births) - float(deaths)
        if float(births) != 0:
            difference_percentage_birth = difference_birth / float(births) * 100
        else:
            difference_percentage_birth = 0
        
        difference_death = float(deaths) - float(births)
        if float(births) != 0:
            difference_percentage_death = difference_death / float(births) * 100
        else:
            difference_percentage_death = 0
        
        col1.metric(label="Natalidad", value=formatted_births, delta=f"{difference_percentage_birth:.2f}%")
        col2.metric(label="Mortalidad", value=formatted_deaths, delta=f"{difference_percentage_death:.2f}%")


        st.markdown('### GÉNERO')
    
        # Crea el gráfico de donut para la población masculina y femenina
        donut_chart = make_donut(male_percentage, 'Población masculina', 'rgb(58, 166, 185)', female_percentage, 'Población femenina', 'rgb(255, 158, 170)')
        if male_percentage != 0 and female_percentage != 0:
            st.altair_chart(donut_chart)
        else:
            st.warning("⚠️ No se dispone de datos sobre los porcentajes de hombres y mujeres")
            
        if male_population != 0 and female_population != 0:
            data = {"Población masculina": [formatted_male_population], "Población femenina": [formatted_female_population]}
            df = pd.DataFrame(data)
            st.dataframe(df, hide_index=True)
        else:
            st.warning("⚠️ No se dispone de datos sobre la cantidad de hombres y mujeres")

        

    with col[1]:
        # Convierte selected_data en un DataFrame de pandas
        data = pd.DataFrame(selected_data)

        inespecific_religion, catolical_religion, diferent_religion, no_religion, catholic_population, uncatolical_population = get_religion_values(data, selected_year)

        poblacion_5_anos_inmigrante, poblacion_5_anos_emigrante, poblacion_nacida_otro_pais_residente_mexico, poblacion_nacida_otro_pais_residente_mexico_hombres, poblacion_nacida_otro_pais_residente_mexico_mujeres = get_migration_values(data, selected_year)
        
        st.markdown('### MIGRACIÓN')

        if poblacion_5_anos_inmigrante != 0 and poblacion_5_anos_emigrante != 0 and poblacion_nacida_otro_pais_residente_mexico != 0 and poblacion_nacida_otro_pais_residente_mexico_hombres != 0 and poblacion_nacida_otro_pais_residente_mexico_mujeres != 0:
            migration_data = pd.DataFrame(
                {
                    "Tipo": ["Inmigrantes", "Emigrantes", "Residentes en México"],
                    "Población": [poblacion_5_anos_inmigrante, poblacion_5_anos_emigrante, poblacion_nacida_otro_pais_residente_mexico],
                    "Población masculina": [0, 0, poblacion_nacida_otro_pais_residente_mexico_hombres],
                    "Población femenina": [0, 0, poblacion_nacida_otro_pais_residente_mexico_mujeres],
                }
            )
            
            # Crear la gráfica de barras
            fig = go.Figure(data=[
                go.Bar(name='Población', x=migration_data['Tipo'], y=migration_data['Población'], marker_color='rgba(199, 56, 189, 0.5)', width=[0.8, 0.8]),
                go.Bar(name='Población masculina', x=migration_data['Tipo'], y=migration_data['Población masculina'], marker_color='rgb(58, 166, 185)'),
                go.Bar(name='Población femenina', x=migration_data['Tipo'], y=migration_data['Población femenina'], marker_color='rgb(255, 158, 170)')
            ])
            
            # Actualizar el layout para apilar las barras
            fig.update_layout(barmode='group')
            
            # Redimensionar el gráfico
            fig.update_layout(autosize=False, width=300, height=200, margin=dict(t=0))
        
            # Quitar la leyenda
            fig.update_layout(showlegend=False)
            
            st.plotly_chart(fig)

        else:
            st.warning(" ⚠️ No se dispone de datos migratorios")


        st.markdown('### RELIGIÓN')

        formatted_catholic_population = convert_to_float_and_format(catholic_population)
        formatted_uncatolical_population = convert_to_float_and_format(uncatolical_population)

        if catholic_population != 0 and uncatolical_population != 0:
            data = {"Población católica": [formatted_catholic_population], "Población no católica": [formatted_uncatolical_population]}
            df = pd.DataFrame(data)
            st.dataframe(df, hide_index=True)

        else:
            st.warning(" ⚠️ No se dispone de datos sobre los diferentes tipos de religión")
    

        if inespecific_religion != 0 and catolical_religion != 0 and diferent_religion != 0 and no_religion != 0:  
            chart_data = pd.DataFrame(
                {
                    "Religión": ["Inespecífica", "Católica", "Diferente", "Sin religión"],
                    "Población": [inespecific_religion, catolical_religion, diferent_religion, no_religion]
                }
            )
            
            # Crear una lista de colores única para cada religión
            colors = {
                'Inespecífica': 'rgb(195, 255, 147)',  # Rojo
                'Católica': 'rgb(255, 219, 92)',  # Verde
                'Diferente': 'rgb(255, 175, 97)',  # Azul
                'Sin religión': 'rgb(255, 112, 171)'  # Amarillo
            }

            fig = go.Figure(data=[
                            go.Bar(
                                x=chart_data[chart_data['Religión'] == religion]['Religión'], 
                                y=chart_data[chart_data['Religión'] == religion]['Población'], 
                                name=religion,
                                marker_color=colors[religion]
                            ) for religion in chart_data['Religión'].unique()
                        ])
            
            fig.update_layout(barmode='group')
            
            # Ocultar los nombres de las religiones en el eje x
            fig.update_xaxes(showticklabels=False)
            
            # Redimensionar el gráfico
            fig.update_layout(autosize=False, width=300, height=300, margin=dict(t=0))
            
            st.plotly_chart(fig)

        else:
            st.warning(" ⚠️ No se dispone de datos sobre las preferencias religiosas de las personas")


    with col[2]:
        # Convierte selected_data en un DataFrame de pandas
        data = pd.DataFrame(selected_data)
    
        (population_0_4, population_0_4_males, population_0_4_females, 
        population_5_9, population_5_9_males, population_5_9_females,
        population_10_14, population_10_14_males, population_10_14_females, 
        population_15_19, population_15_19_males, population_15_19_females, 
        population_20_24, population_20_24_males, population_20_24_females, 
        population_25_29, population_25_29_males, population_25_29_females,
        population_30_34, population_30_34_males, population_30_34_females,
        population_35_39, population_35_39_males, population_35_39_females,
        population_40_44, population_40_44_males, population_40_44_females,
        population_45_49, population_45_49_males, population_45_49_females,
        population_50_54, population_50_54_males, population_50_54_females,
        population_55_59, population_55_59_males, population_55_59_females,
        population_60_64, population_60_64_males, population_60_64_females,
        population_65_69, population_65_69_males, population_65_69_females,
        population_70_74, population_70_74_males, population_70_74_females,
        population_75_79, population_75_79_males, population_75_79_females,
        population_80_84, population_80_84_males, population_80_84_females,
        population_85_89, population_85_89_males, population_85_89_females,
        population_90_94, population_90_94_males, population_90_94_females,
        population_95_99, population_95_99_males, population_95_99_females,
        population_100_plus, population_100_plus_males, population_100_plus_females) = get_age_values(data, selected_year)
    
        st.markdown('### EDAD')

        if (population_0_4 != 0 and population_0_4_males != 0 and population_0_4_females != 0 and 
            population_5_9 != 0 and population_5_9_males != 0 and population_5_9_females != 0 and
            population_10_14 != 0 and population_10_14_males != 0 and population_10_14_females != 0 and 
            population_15_19 != 0 and population_15_19_males != 0 and population_15_19_females != 0 and 
            population_20_24 != 0 and population_20_24_males != 0 and population_20_24_females != 0 and 
            population_25_29 != 0 and population_25_29_males != 0 and population_25_29_females != 0 and
            population_30_34 != 0 and population_30_34_males != 0 and population_30_34_females != 0 and
            population_35_39 != 0 and population_35_39_males != 0 and population_35_39_females != 0 and
            population_40_44 != 0 and population_40_44_males != 0 and population_40_44_females != 0 and
            population_45_49 != 0 and population_45_49_males != 0 and population_45_49_females != 0 and
            population_50_54 != 0 and population_50_54_males != 0 and population_50_54_females != 0 and
            population_55_59 != 0 and population_55_59_males != 0 and population_55_59_females != 0 and
            population_60_64 != 0 and population_60_64_males != 0 and population_60_64_females != 0 and
            population_65_69 != 0 and population_65_69_males != 0 and population_65_69_females != 0 and
            population_70_74 != 0 and population_70_74_males != 0 and population_70_74_females != 0 and
            population_75_79 != 0 and population_75_79_males != 0 and population_75_79_females != 0 and
            population_80_84 != 0 and population_80_84_males != 0 and population_80_84_females != 0 and
            population_85_89 != 0 and population_85_89_males != 0 and population_85_89_females != 0 and
            population_90_94 != 0 and population_90_94_males != 0 and population_90_94_females != 0 and
            population_95_99 != 0 and population_95_99_males != 0 and population_95_99_females != 0 and
            population_100_plus != 0 and population_100_plus_males != 0 and population_100_plus_females != 0):

            age_data = pd.DataFrame(
                {
                    "Edad": ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80-84", "85-89", "90-94", "95-99", "100+"],
                    "Población": [population_0_4, population_5_9, population_10_14, population_15_19, population_20_24, population_25_29, population_30_34, population_35_39, population_40_44, population_45_49, population_50_54, population_55_59, population_60_64, population_65_69, population_70_74, population_75_79, population_80_84, population_85_89, population_90_94, population_95_99, population_100_plus],
                    "Población masculina": [population_0_4_males, population_5_9_males, population_10_14_males, population_15_19_males, population_20_24_males, population_25_29_males, population_30_34_males, population_35_39_males, population_40_44_males, population_45_49_males, population_50_54_males, population_55_59_males, population_60_64_males, population_65_69_males, population_70_74_males, population_75_79_males, population_80_84_males, population_85_89_males, population_90_94_males, population_95_99_males, population_100_plus_males],
                    "Población femenina": [population_0_4_females, population_5_9_females, population_10_14_females, population_15_19_females, population_20_24_females, population_25_29_females, population_30_34_females, population_35_39_females, population_40_44_females, population_45_49_females, population_50_54_females, population_55_59_females, population_60_64_females, population_65_69_females, population_70_74_females, population_75_79_females, population_80_84_females, population_85_89_females, population_90_94_females, population_95_99_females, population_100_plus_females],
                }
            )
            
            # Crear la gráfica de barras
            fig = go.Figure(data=[
                go.Bar(name='Población', x=age_data['Edad'], y=age_data['Población'], marker_color='rgba(253, 255, 194, 0.5)'),
                go.Scatter(name='Población masculina', x=age_data['Edad'], y=age_data['Población masculina'], mode='lines', line=dict(color='rgb(58, 166, 185)', width=5)),
                go.Scatter(name='Población femenina', x=age_data['Edad'], y=age_data['Población femenina'], mode='lines', line=dict(color='rgb(255, 158, 170)', width=5))
            ])
            
            # Cambiar el modo de la gráfica a 'group'
            fig.update_layout(barmode='group')
            
            # Redimensionar el gráfico
            fig.update_layout(autosize=False, width=300, height=400, margin=dict(t=0))
        
            # Quitar la leyenda
            fig.update_layout(showlegend=False)
            
            st.plotly_chart(fig)
        else:
            st.warning(" ⚠️ No se dispone de datos sobre edad de las personas")
        

        marriages, divorces = get_nupcial_values(data, selected_year)
        
        st.markdown('### NUPCIALIDAD')

        def clean_number(number_str):
            # Split the string by space and keep only the first part
            number_str = number_str.split()[0]
            return float(number_str)

        marriages = clean_number(marriages)
        divorces = clean_number(divorces)
        total = marriages + divorces

        marriages_percentage = round((marriages / total) * 100, 2)
        divorces_percentage = round((divorces / total) * 100, 2)
    
        # Crea el gráfico de donut para la población masculina y femenina
        donut_chart = make_donut(marriages_percentage, 'Matrimonios', 'rgb(0, 223, 162)', divorces_percentage, 'Divorcios', 'rgb(175, 71, 210)')
        if marriages_percentage != 0 and divorces_percentage != 0:
            st.altair_chart(donut_chart)
        else:
            st.warning("⚠️ No se dispone de datos sobre los datos nupciales")
                
if __name__ == "__main__":
    main()