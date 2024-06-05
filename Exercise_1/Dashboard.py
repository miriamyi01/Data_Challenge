import streamlit as st
import requests
import pandas as pd
import json
import altair as alt
import plotly.graph_objects as go

values = []  # Move the declaration and assignment outside of the function

def get_data_from_api(api_key):
    '''
    Función para obtener los datos de la API del INEGI
    1002000001 - Población total
    1002000002 - Población total hombres
    1002000003 - Población total mujeres
    6207020032 - Porcentaje hombres
    6207020033 - Porcentaje mujeres

    6200205289 - Población de 5 años y más con religión no especificada
    6200205273 - Población de 5 años y más católica
    6200205257 - Población de 5 años y más con religión distinta de católica
    6200205256 - Población de 5 años y más sin religión
    6200240301 - Población católica
    6200240497 - Población no católica
    '''

    # Datos relacionados con la cantidad de población
    url = f'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001,1002000002,1002000003,6207020032,6207020033,6200205289,6200205273,6200205257,6200205256,6200240301,6200240497/es/0700/false/BISE/2.0/{api_key}?type=json'

    response = requests.get(url)
    data_list = []  # lista para almacenar los datos
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
    
    text1 = create_text(plot, 'right', -10, input_response1, input_text1)
    text2 = create_text(plot, 'left', 10, input_response2, input_text2)

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
        st.markdown('### MORTALIDAD Y NATALIDAD')


        # Obtén los valores de la población masculina y femenina
        # Convierte selected_data en un DataFrame de pandas
        data = pd.DataFrame(selected_data)

        total_population, male_population, female_population, male_percentage, female_percentage = get_population_values(data, selected_year)

        st.markdown('### GÉNERO')
        
        # Convierte los valores a números y formatea
        formatted_population = convert_to_float_and_format(total_population)
        formatted_male_population = convert_to_float_and_format(male_population)
        formatted_female_population = convert_to_float_and_format(female_population)
        
        # Porcentajes de la población masculina y femenina
        male_percentage = calculate_percentage(male_percentage)
        female_percentage = calculate_percentage(female_percentage)
    
        # Crea el gráfico de donut para la población masculina y femenina
        donut_chart = make_donut(male_percentage, 'Población masculina', '#87CEEB', female_percentage, 'Población femenina', 'pink')

        st.metric(label="Población total", value=formatted_population)
        if male_population != 0 and female_population != 0:
            data = {"Población masculina": [formatted_male_population], "Población femenina": [formatted_female_population]}
            df = pd.DataFrame(data)
            st.dataframe(df, hide_index=True)
        else:
            st.warning("⚠️ No se dispone de datos sobre la cantidad de hombres y mujeres")
        
        
        if male_percentage != 0 and female_percentage != 0:
            st.altair_chart(donut_chart)
        else:
            st.warning("⚠️ No se dispone de datos sobre los porcentajes de hombres y mujeres")


    with col[1]:
        st.markdown('### EDAD')

    with col[2]:
        # Convierte selected_data en un DataFrame de pandas
        data = pd.DataFrame(selected_data)

        inespecific_religion, catolical_religion, diferent_religion, no_religion, catholic_population, uncatolical_population = get_religion_values(data, selected_year)

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
            
            fig = go.Figure(data=[
                go.Bar(name='Religión', x=chart_data['Religión'], y=chart_data['Población'])
            ])
            
            fig.update_layout(barmode='group')
            
            # Ocultar los nombres de las religiones en el eje x
            fig.update_xaxes(showticklabels=False)
            
            # Redimensionar el gráfico
            fig.update_layout(autosize=False, width=400, height=300)
            st.plotly_chart(fig)

        else:
            st.warning(" ⚠️ No se dispone de datos sobre las preferencias religiosas de las personas")

                
if __name__ == "__main__":
    main()