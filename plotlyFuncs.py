import plotly.graph_objects as go
colors_hex = [
    "#FF5733",  # Rojo anaranjado
    "#33FF57",  # Verde claro
    "#3357FF",  # Azul brillante
    "#FF33A1",  # Rosa fuerte
    "#FFC300",  # Amarillo dorado
    "#DAF7A6",  # Verde menta
    "#900C3F",  # Borgoña
    "#581845",  # Morado oscuro
    "#C70039",  # Rojo fuerte
    "#1F618D",  # Azul oscuro
    "#27AE60",  # Verde bosque
    "#F39C12",  # Naranja suave
    "#8E44AD",  # Púrpura
    "#2E86C1",  # Azul medio
    "#F1948A",  # Rosa claro
    "#D5DBDB",  # Gris claro
    "#17202A",  # Negro azulado
    "#A93226",  # Rojo ladrillo
    "#E74C3C",  # Rojo brillante
    "#5D6D7E",  # Gris azulado
    "#82E0AA",  # Verde pastel
    "#F0B27A",  # Durazno
    "#566573",  # Gris plomo
    "#BDC3C7",  # Gris plata
]



def plot_line_from_df(df, x_col, y_col, title="Gráfico de líneas", x_label="Eje X", y_label="Eje Y", line_color="blue"):
    """
    Crea un gráfico de líneas usando Plotly a partir de un DataFrame, con opción de color.
    
    Parámetros:
        df (pd.DataFrame): DataFrame con los datos.
        x_col (str): Nombre de la columna para el eje X.
        y_col (str): Nombre de la columna para el eje Y.
        title (str): Título del gráfico.
        x_label (str): Etiqueta del eje X.
        y_label (str): Etiqueta del eje Y.
        line_color (str): Color de la línea (nombre o código hexadecimal).
        
    Retorna:
        fig (plotly.graph_objects.Figure): Objeto figura con el gráfico.
    """
    fig = go.Figure()

    # Añade el gráfico de línea con color personalizado
    fig.add_trace(go.Scatter(
        x=df[x_col], 
        y=df[y_col], 
        mode='lines', 
        name=f'{y_col} en función de fechas',
        line=dict(color=line_color)
    ))

    # Configuración de diseño
    fig.update_layout(
        title=title,
        xaxis_title=x_label if x_label != "Eje X" else x_col,
        yaxis_title=y_label if y_label != "Eje Y" else y_col,
        template="plotly_white"
    )
    
    return fig
