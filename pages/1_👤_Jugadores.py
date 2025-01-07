from headers import *
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if "df" not in st.session_state:
    st.session_state.df = None

st.set_page_config(
    page_icon=image_path
)
st.logo("https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Sporting_Football_Club_2019.png/157px-Sporting_Football_Club_2019.png")
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


selected = option_menu(
    menu_title=None,  # required
    options=["Jugador", "Gráficos"],  # required
    icons=["person-circle", "graph-up"],  # optional
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

if selected=="Jugador":
    st.markdown("----")

    play=st.selectbox("", sorted(pd.unique(myData.df["Jugador"])))


    
    with st.expander("### • Filtros"):

        col1, col2, col3 = st.columns(3)
        with col1: 
            with st.popover("⏰ X duración"):
                t = st.slider("Filtrar por duración:", myData.df_st["Duración"].min(), myData.df_st["Duración"].max(), (myData.df_st["Duración"].min(),myData.df_st["Duración"].max()))
                #limInf,limSup = t
        with col2:
            with st.popover("📅 X fecha"):

                # Selector de rango de fechas
                date_range = st.date_input(
                    "Seleccione un rango de fechas:",
                    value=(fr, lr), # Valores por defecto
                    min_value=fr,   # Fecha mínima
                    max_value=lr    # Fecha máxima
                )
                try:
                    bd=date_range[0]
                    ed=date_range[1]

                except:
                    pass

            

        with col3:
            ops_MD=pd.unique(myData.session["matchDay"])
            with st.popover("⚽ X MD"):
                md = st.multiselect("Qué MD le interesa", ops_MD, default=ops_MD)
    st.markdown("------------")

    st.session_state.df=myData.df_st.query("Jugador == @play").drop(columns=["Jugador"]).copy()
    d_s=myData.df.iloc[st.session_state.df.index]["Sesión"]
    st.write(len(d_s))
    #st.session_state.df=myData.getSesInMD(valores=md, d=st.session_state.df)   
    myData.getSesInMD(valores=md, d_sec=d_s, d=st.session_state.df)
    myData.getSesInTimeRange(valores=t, trydf_f=True)
    try:
        myData.getSesInDateRange(valores=date_range, trydf_f=True)
    except:
        pass
    st.session_state.df=myData.df_f
    st.dataframe(st.session_state.df.reset_index(drop=True))
else:
    y=[]
    col1, col2 =st.columns(2)
    with col1:
        if st.checkbox("Aceleraciones"):
            y.append("acc")
        if st.checkbox("Desaceleraciones"):
            y.append("dec")

        if st.checkbox("HSR"):
            y.append("HSR")
    
    with col2:
        if st.checkbox("SPRINT"):
            y.append("SPRINT")

        if st.checkbox("Velocidad máxima"):
            y.append("Distancia total")

        if st.checkbox("Distancia total"):
            y.append("Distancia total")


    d=st.session_state.df.drop(columns=["Sesión", "Duración"])
    if y!=[]:
        st.line_chart(d, y=y, x="Fecha")


