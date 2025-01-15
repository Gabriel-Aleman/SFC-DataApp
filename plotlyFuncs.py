import plotly.graph_objects as go
import plotly.express as px

colors_hex = [
    "#FF5733",  # Rojo anaranjado fuerte
    "#28A745",  # Verde vibrante
    "#007BFF",  # Azul fuerte
    "#FF1493",  # Rosa intenso
    "#FFC107",  # Amarillo dorado
    "#20C997",  # Verde esmeralda
    "#C0392B",  # Rojo ladrillo intenso
    "#8E44AD",  # Morado brillante
    "#FF4500",  # Naranja fuerte
    "#1E90FF",  # Azul real
    "#2ECC71",  # Verde primavera
    "#FF8C00",  # Naranja oscuro
    "#9B59B6",  # Púrpura vibrante
    "#2980B9",  # Azul océano
    "#FF69B4",  # Rosa chicle intenso
    "#A9A9A9",  # Gris oscuro
    "#34495E",  # Azul grisáceo oscuro
    "#E74C3C",  # Rojo fuego
    "#FF6347",  # Tomate fuerte
    "#5D6D7E",  # Azul gris oscuro
    "#27AE60",  # Verde esmeralda oscuro
    "#E67E22",  # Naranja quemado
    "#7F8C8D",  # Gris medio oscuro
    "#BDC3C7",  # Gris claro vibrante
]



 # Función para crear un gráfico con Plotly
def crear_grafico_barra(df, x, y, titulo, color):
    fig = px.bar(df, x=x, y=y, title=titulo, text=y)
    fig.update_traces(marker_color=color, textposition="outside")
    fig.update_layout(
        xaxis_tickangle=-45,  # Ajusta las etiquetas del eje x
        plot_bgcolor="white",  # Fondo blanco para el área de datos
        title_font_size=16,
    )
    return fig

def crear_histograma(df, x, titulo, color, bins):
    fig = px.histogram(df, x=x, title=titulo, color_discrete_sequence=[color], nbins=bins)
    fig.update_layout(
        xaxis_tickangle=-45,  # Ajusta las etiquetas del eje x
        plot_bgcolor="white",  # Fondo blanco para el área de datos
        title_font_size=16,
    )
    return fig



def mapa_correlacion_todas_las_columnas(df, titulo):
    import plotly.figure_factory as ff
    # Calcular la matriz de correlación para todas las columnas
    correlacion = df.corr().round(3)

    # Crear el mapa de calor con la matriz de correlación
    fig = ff.create_annotated_heatmap(
        z=correlacion.values, 
        x=correlacion.columns.tolist(), 
        y=correlacion.columns.tolist(),
        colorscale='RdBu',  # Puedes usar diferentes colores, como 'RdBu', 'Blues', etc.
        showscale=True
    )

    # Actualizar el layout para ajustar la apariencia
    fig.update_layout(
        title=titulo,
        title_font_size=16,
        plot_bgcolor="white",
    )

    return fig


def crear_Dist(df, x, titulo, color):
    # Calcular el número de bins por default usando numpy.histogram
    from numpy import histogram
    _, bin_edges = histogram(df[x].dropna(), bins='auto')  # 'auto' permite a numpy elegir el número de bins
    bins = len(bin_edges) - 1  # El número de bins es el número de bordes menos uno

    import plotly.figure_factory as ff
    # Crear el histograma usando create_distplot
    fig = ff.create_distplot([df[x].dropna()], group_labels=[x], colors=[color], bin_size=bins)

    # Actualizar el layout del gráfico
    fig.update_layout(
        title=titulo,
        xaxis_title=x,
        title_font_size=16,
        plot_bgcolor="white",  # Fondo blanco para el área de datos
        xaxis_tickangle=-45,  # Ajusta las etiquetas del eje x
    )

    return fig

    return fig


def crear_boxplot(df, y, titulo, color):
    fig = px.box(df, y=y, title=titulo, color_discrete_sequence=[color], notched=True)

    fig.update_layout(
        plot_bgcolor="white",  # Fondo blanco para el área de datos
        title_font_size=16,
    )
    return fig





def plotTable(df):
    # Incluir el índice en la tabla
    df = df.reset_index()  # O puedes usar df.index directamente si no quieres reiniciarlo
    df.rename(columns={"index": "Índice"}, inplace=True)  # Renombrar la columna de índice

    # Crear una tabla con estilo mejorado
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=[f"<b>{col}</b>" for col in df.columns],  # Incluye encabezados
                    fill_color="#8B0000",  # Fondo rojo oscuro para los encabezados
                    font=dict(color="white", size=14),  # Texto blanco y tamaño más grande
                    align="center",  # Centrado
                    line_color="darkslategray",  # Color del borde
                ),
                cells=dict(
                    values=[df[col] for col in df.columns],  # Incluye todas las columnas
                    fill_color=[
                        ["#FFCCCC" if i % 2 == 0 else "#FF9999" for i in range(len(df))]  # Tonos de rojo para la columna del índice
                        if col == "Índice" else
                        ["#f2f2f2" if i % 2 == 0 else "white" for i in range(len(df))]  # Alternancia de colores en las demás columnas
                        for col in df.columns
                    ],
                    font=dict(color="black", size=12),  # Texto negro
                    align="center",  # Centrado
                    line_color="darkslategray",  # Color del borde
                    height=30,  # Altura de las celdas
                )
            )
        ]
    )

    # Personalizar el tamaño de la figura
    fig.update_layout(
        dragmode="zoom",  # Permite el zoom en la tabla
        margin=dict(l=20, r=20, t=30)  # Márgenes
        
    )
    return fig