import plotly.graph_objects as go
import plotly.express as px

colors_hex = [
    "#FFC1A1",  # Melocotón pastel
    "#B4F0B4",  # Verde menta pastel
    "#A1C4FF",  # Azul cielo pastel
    "#FFB3D9",  # Rosa chicle pastel
    "#FFE4A1",  # Amarillo crema pastel
    "#D6FFE1",  # Verde agua pastel
    "#D7A9A1",  # Rojo arcilla pastel
    "#CAB0C7",  # Lavanda pastel
    "#FFA4A4",  # Rojo coral pastel
    "#A1B9D7",  # Azul grisáceo pastel
    "#C1E1C1",  # Verde hierba pastel
    "#FFD9A1",  # Naranja crema pastel
    "#D1C1E7",  # Morado lavanda pastel
    "#B0D4FF",  # Azul hielo pastel
    "#FFCEDA",  # Rosa pétalo pastel
    "#E8E8E8",  # Gris nube pastel
    "#A9B2C4",  # Azul polvoriento pastel
    "#D9A1A1",  # Rojo ladrillo pastel
    "#F4A1A1",  # Rojo rosado pastel
    "#B1C3CF",  # Gris azulado pastel
    "#D9F6E1",  # Verde suave pastel
    "#F7D4C4",  # Melocotón suave pastel
    "#BAC3C9",  # Gris claro pastel
    "#E4E6E9",  # Gris perla pastel
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

def crear_boxplot(df, y, titulo, color):
    fig = px.box(df, y=y, title=titulo, color_discrete_sequence=[color], notched=True)

    fig.update_layout(
        plot_bgcolor="white",  # Fondo blanco para el área de datos
        title_font=dict(family="Arial, sans-serif", size=18, weight="bold"),  # Título más grande y con mejor fuente
        xaxis_title="Valor",  # Título para el eje X
        boxmode="group",  # Agrupa las cajas por categorías
        xaxis=dict(
            showgrid=True,  # Mostrar las líneas de la cuadrícula

        ),

        margin=dict(l=50, r=50, t=50, b=50),  # Márgenes de la figura
        
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