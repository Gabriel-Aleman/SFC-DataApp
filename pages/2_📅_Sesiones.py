from headers import *
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if "df" not in st.session_state:
    st.session_state.df = None

st.set_page_config(
    page_icon=image_path
)
st.logo("https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Sporting_Football_Club_2019.png/157px-Sporting_Football_Club_2019.png")
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

df=myData.infFilteredSesions_comp()

selected = option_menu(
    menu_title=None,  # required
    options=["Sesión", "Gráficos", "Estadísticas"],  # required
    icons=["calendar-event-fill", "graph-up", "calculator-fill"],  # optional
    menu_icon="cast",  # optional
    default_index=0,  # optional
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#1e1e1e"},  # Fondo oscuro
        "icon": {"color": "#f39c12", "font-size": "25px"},  # Icono naranja vibrante
        "nav-link": {
            "font-size": "25px",
            "text-align": "left",
            "margin": "0px",
            "--hover-color": "#2c3e50",  # Color oscuro para hover
            "color": "#ecf0f1",  # Texto blanco claro
        },
        "nav-link-selected": {"background-color": "#e74c3c"},  # Rojo brillante para selección
    }
)

if selected=="Sesión":
    st.markdown("----")
    ses=st.selectbox("", myData.session_nr)
   
    
    with st.expander("### • Filtros"):

        col1, col2 = st.columns(2)
        with col1: 
            with st.popover("⏰ X duración"):
                t = st.slider("Filtrar por duración:", myData.df_st["Duración"].min(), myData.df_st["Duración"].max(), (myData.df_st["Duración"].min(),myData.df_st["Duración"].max()))
        with col2:
            ops_Pos=pd.unique(myData.players["Posición"])
            with st.popover("📍 X Posición"):
                pos = st.multiselect("Qué posisición le interesa",ops_Pos, default=ops_Pos)
    st.session_state.df = df.query("Sesión == @ses ")
    st.session_state.df = myData.getSesInTimeRange(valores=t, d=st.session_state.df)
    st.session_state.df = myData.getJugsInPos(valores=pos, d=st.session_state.df)


    st.session_state.df = myData.df_st.iloc[st.session_state.df.index]
    st.dataframe(st.session_state.df.reset_index(drop=True))

else:
    # Selección de tipo de gráfico
    plot_type = st.radio("Selecciona el tipo de gráfico:", ["Barra", "Histograma", "Box Plot"])

    d=st.session_state.df.drop(columns=["Fecha", "Duración"])
    # Abreviar nombres (e.g., Alejandro Feoli -> Alejandro F.)
    def abreviar_nombres(nombre):
        partes = nombre.split()
        if len(partes) > 1:
            return f"{partes[0]} {partes[1][0]}."
        return nombre

    d["Jugador"] = d["Jugador"].apply(abreviar_nombres)
    if plot_type == "Histograma":
    
        bins = st.slider("Selecciona el número de bins", min_value=5, max_value=50, value=10)
    col1, col2 =st.columns(2)

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

    def crear_boxplot(df, y, titulo, color):
        fig = px.box(df, y=y, title=titulo, color_discrete_sequence=[color])
        fig.update_layout(
            plot_bgcolor="white",  # Fondo blanco para el área de datos
            title_font_size=16,
        )
        return fig
    



    # Gráficos dinámicos según el tipo seleccionado
    with col1:
        ys=["acc", "dec", "HSR"] #TODO
        if plot_type == "Barra":
            st.plotly_chart(crear_grafico_barra(d, x="Jugador", y="acc", titulo="Aceleración", color="blue"))
            st.plotly_chart(crear_grafico_barra(d, x="Jugador", y="dec", titulo="Desaceleración", color="green"))
            st.plotly_chart(crear_grafico_barra(d, x="Jugador", y="HSR", titulo="High-Speed Running", color="purple"))
        elif plot_type == "Histograma":
    # Slider para seleccionar el número de bins
            st.plotly_chart(crear_histograma(d, x="acc", titulo="Histograma de Aceleración", color="blue", bins=bins))
            st.plotly_chart(crear_histograma(d, x="dec", titulo="Histograma de Desaceleración", color="green", bins=bins))
            st.plotly_chart(crear_histograma(d, x="HSR", titulo="Histograma de High-Speed Running", color="purple", bins=bins))
        
        elif plot_type == "Box Plot":
            st.plotly_chart()
            st.plotly_chart(crear_boxplot(d, y="dec", titulo="Box Plot de Desaceleración", color="green"))
            st.plotly_chart(crear_boxplot(d, y="HSR", titulo="Box Plot de High-Speed Running", color="purple"))

    with col2:
        ys=["acc", "dec", "HSR"]
        if plot_type == "Barra":
            st.plotly_chart(crear_grafico_barra(d, x="Jugador", y="SPRINT", titulo="Sprints", color="orange"))
            st.plotly_chart(crear_grafico_barra(d, x="Jugador", y="Distancia total", titulo="Distancia Total", color="red"))
            st.plotly_chart(crear_grafico_barra(d, x="Jugador", y="Velocidad máxima", titulo="Velocidad Máxima", color="teal"))
        elif plot_type == "Histograma":
            st.plotly_chart(crear_histograma(d, x="SPRINT", titulo="Histograma de Sprints", color="orange", bins=bins))
            st.plotly_chart(crear_histograma(d, x="Distancia total", titulo="Histograma de Distancia Total", color="red", bins=bins))
            st.plotly_chart(crear_histograma(d, x="Velocidad máxima", titulo="Histograma de Velocidad Máxima", color="teal", bins=bins))
        elif plot_type == "Box Plot":
            st.plotly_chart(crear_boxplot(d, y="SPRINT", titulo="Box Plot de Sprints", color="orange"))
            st.plotly_chart(crear_boxplot(d, y="Distancia total", titulo="Box Plot de Distancia Total", color="red"))
            st.plotly_chart(crear_boxplot(d, y="Velocidad máxima", titulo="Box Plot de Velocidad Máxima", color="teal"))

