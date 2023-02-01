# Importacion de librerías
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go


# Definimos las columnas que nos interesan
fields = ['course_title', 'is_paid',  'price',  'num_subscribers',  'num_reviews',  'num_lectures',  'level',  'content_duration', 'subject', 'published_date',  'published_month']

# Cargamos el DataFrame sólo con esas columnas
# df = pd.read_csv('wine_reviews.csv', usecols=fields)
udemy = pd.read_csv('./datasets/udemy_courses.csv')

#------------------#
# Transformaciones #
#------------------#

# Eliminamos los valores nulos/nan
def drop_nan_vals(df):
    df.dropna(inplace=True)
    return df
udemy = drop_nan_vals(udemy)

# Eliminamos los registros duplicados
def drop_duplicates(df):
    df = df.drop_duplicates()
    return df
udemy = drop_duplicates(udemy)

# Creamos nuevas columnas published_date, published_month a partir de published_date
def create_date_cols(df):
    df['published_timestamp'] = pd.to_datetime(df.published_timestamp, format='%Y-%m-%dT%H:%M:%SZ')
    df['published_date'] = df['published_timestamp'].dt.date
    df['published_month'] = df['published_timestamp'].dt.month
    df = df.drop('published_timestamp', axis=1)
    return df
udemy = create_date_cols(udemy)


st.title('Calidad de videos en Udemy')

def barplot_visualization(df, col_name, title, x_label, y_label):
    fig = plt.Figure(figsize=(18,8))
    fig = px.bar(
                x = df[col_name].value_counts().index,
                y = df[col_name].value_counts().values,
                color = df[col_name].value_counts().index,
                height=500,
                width=800,
                labels={
                    'x': x_label,
                    'y': y_label
                }
                )
    fig.update_layout(
        title={
            'text': title,
            # 'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font_size':18,
            'font_color':'blue'})
    
    st.plotly_chart(fig)
    
def pieplot_visualization(df, col_name, title, x_label, y_label):
    fig = px.pie(
                values = df[col_name].value_counts().values,
                names = df[col_name].value_counts().index,
                labels={
                    'x': x_label,
                    'y': y_label
                }
    )
    fig.update_layout(
        title={
            'text': title,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font_size':18,
            'font_color':'blue'
        }
    )

    st.plotly_chart(fig)

def plot_displot():
    fig = px.histogram(udemy, x="price", color="level",
                   marginal="box", # or violin, rug
                   hover_data=udemy.columns)
    fig.update_layout(
        title={
            'text': title,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font_size':18,
            'font_color':'blue'
        }
    )
    
    fig.show()
    

if st.checkbox('Mostrar Distribución de cantidad de videos por nivel',False):
    barplot_visualization(udemy, 'level', 'Distribución de cantidad de videos por nivel', 'Nivel', 'Cantidad de Cursos')

if st.checkbox('Mostrar Distribución de cantidad de videos pagados y gratuitos',False):
    barplot_visualization(udemy, 'is_paid', 'Distribución de cantidad de videos por nivel', 'Tipo de pago(Grauito o Pagado)', 'Cantidad de cursos')

if st.checkbox('Mostrar distribución de cantidad de videos pagados y gratuitos',False):
    pieplot_visualization(udemy, 'is_paid', 'Distribución de cantidad de videos por nivel', 'Tipo de pago(Grauito o Pagado)', 'Cantidad de cursos')
    