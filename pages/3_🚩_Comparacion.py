from headers import *
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if "df" not in st.session_state:
    st.session_state.df = None

if "df1" not in st.session_state:
    st.session_state.df1 = None

if "df2" not in st.session_state:
    st.session_state.df2 = None

st.set_page_config(
    page_icon=image_path
)
st.logo("https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Sporting_Football_Club_2019.png/157px-Sporting_Football_Club_2019.png")
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 

selected = option_menu(
    menu_title=None,  # required
    options=["Comparación", "Gráficos"],  # required
    icons=["rulers", "graph-up"],  # optional
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
arrValues=["Duración","Distancia total", "Velocidad máxima", "HSR", "SPRINT", "acc", "dec"]


df=myData.infFilteredSesions_comp()


if selected == "Comparación":

    st.markdown("----")
    sesiones=list(myData.session_nr["Nombre"].to_list())
    

    with st.expander("### • Comparar sesiones"):
        ses0=st.selectbox("Sesión #1", sesiones)
        ses1=st.selectbox("Sesión #2", sesiones)
        
    st.markdown("------------")

    df0= df.query("Sesión == @ses0 ")
    df1= df.query("Sesión == @ses1 ")
    st.session_state.df1=df0
    st.session_state.df2=df1
    jugadoresEnComun= np.intersect1d(df0["Jugador"], df1["Jugador"])

    for jug in jugadoresEnComun:
        df0j = df0.query("Jugador == @jug ")
        df1j = df1.query("Jugador == @jug ")
        st.subheader(jug, divider=True)
        with st.container(height=150):

            cols =st.columns(7)
        

            for i,crit in enumerate(arrValues):
                CritLabel= crit
                CritValue= round(df0j[crit], 1)
                Delta= round(float(df1j[crit])- float(df0j[crit]),1)

                cols[i].metric(CritLabel, CritValue, Delta)

else:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    def superponer_barras(df1, df2, id_col="Jugador", title="Comparación por ID"):
        """
        Crea un gráfico de subplots con barras agrupadas por una columna 'id' de dos DataFrames.
        Cada subplot utiliza un esquema de colores diferente.
        
        Args:
            df1 (pd.DataFrame): Primer DataFrame.
            df2 (pd.DataFrame): Segundo DataFrame.
            id_col (str): Nombre de la columna que agrupa los datos (debe estar en ambos DataFrames).
            title (str): Título del gráfico.
        
        Returns:
            go.Figure: Figura con los subplots.
        """
        import plotly.express as px
        
        # Validar que ambos DataFrames tengan la columna de agrupación y las mismas columnas
        if id_col not in df1.columns or id_col not in df2.columns:
            raise ValueError(f"Ambos DataFrames deben tener la columna '{id_col}'.")
        if not df1.drop(columns=id_col).columns.equals(df2.drop(columns=id_col).columns):
            raise ValueError("Ambos DataFrames deben tener las mismas columnas (excepto el ID).")
        
        # Obtener las columnas numéricas (excluyendo id_col)
        columns = [col for col in df1.columns if col != id_col]
        num_cols = len(columns)
        
        # Crear subplots
        fig = make_subplots(rows=num_cols, cols=1, shared_xaxes=True, subplot_titles=columns)
        
        # Paletas de colores predefinidas
        color_schemes = px.colors.qualitative.Set1 + px.colors.qualitative.Set2 + px.colors.qualitative.Set3
        color_schemes = color_schemes[:num_cols * 2]  # Ajustar si hay más columnas
        
        # Agregar barras para cada columna con diferentes colores
        for i, column in enumerate(columns):
            fig.add_trace(
                go.Bar(
                    x=df1[id_col],
                    y=df1[column],
                    name=f"DF1 - {column}",
                    marker=dict(color=color_schemes[i * 2])
                ),
                row=i + 1, col=1
            )
            fig.add_trace(
                go.Bar(
                    x=df2[id_col],
                    y=df2[column],
                    name=f"DF2 - {column}",
                    marker=dict(color=color_schemes[i * 2 + 1])
                ),
                row=i + 1, col=1
            )
        
        # Configurar diseño
        fig.update_layout(
            height=300 * num_cols,  # Ajusta el tamaño del gráfico
            title_text=title,
            showlegend=True,
            barmode='group'  # Barras agrupadas
        )
        return fig
    arr=arrValues
    arr.append("Jugador")
    df1= st.session_state.df1[arr]
    df2= st.session_state.df2[arr]
    # Llamar la función y mostrar el gráfico
    fig = superponer_barras(df1, df2, title="Comparación de DF1 y DF2")
    st.plotly_chart(fig)
