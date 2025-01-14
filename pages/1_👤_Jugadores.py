from headers import *
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if "df" not in st.session_state:
    st.session_state.df = None
if "df_d" not in st.session_state:
    st.session_state.d = None

st.set_page_config(
    page_icon=image_path
)
st.logo("https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Sporting_Football_Club_2019.png/157px-Sporting_Football_Club_2019.png")
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


selected = option_menu(
    menu_title=None,  # required
    options=["Jugador", "Gráficos",  "Estadísticas"],  # required
    icons=["person-circle", "graph-up", "calculator-fill"],  # optional
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

try:
    st.session_state.d=st.session_state.df.drop(columns=["Sesión", "Duración"])
except:
    pass

match selected:
    case "Jugador":
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
        #st.session_state.df=myData.getSesInMD(valores=md, d=st.session_state.df)   
        myData.getSesInMD(valores=md, d_sec=d_s, d=st.session_state.df)
        myData.getSesInTimeRange(valores=t, trydf_f=True)
        try:
            myData.getSesInDateRange(valores=date_range, trydf_f=True)
        except:
            pass
        st.session_state.df=myData.df_f
        st.dataframe(st.session_state.df.reset_index(drop=True))
    
    case "Gráficos":
        from plotlyFuncs import *
        with st.container(border=True):
            plot_type = st.radio("Selecciona el tipo de gráfico:", ["Linea", "Histograma","Distribución", "Box Plot", "Matriz-correlación"], horizontal=True)

        arrValues=["Distancia total", "Velocidad máxima", "HSR", "SPRINT", "acc", "dec"]

        d=st.session_state.d
        if plot_type=="Histograma":
            bins = st.slider("Selecciona el número de bins", min_value=5, max_value=50, value=10)

        if plot_type=="Matriz-correlación":
            st.plotly_chart(mapa_correlacion_todas_las_columnas(d.drop(columns="Fecha"),"Matriz de correlación"))
        else:
            for i,y in enumerate(arrValues):
                if plot_type=="Linea":
                    st.line_chart(d, y=y, x="Fecha", color=colors_hex[i])
                elif plot_type=="Box Plot":
                    st.plotly_chart(crear_boxplot(d, y=y, titulo="Box Plot "+str(y), color=colors_hex[i]))
                elif plot_type=="Histograma":
                    st.plotly_chart(crear_histograma(d, x=y, titulo="Histograma "+str(y), color=colors_hex[i], bins=bins))
                elif plot_type=="Distribución":
                    st.plotly_chart(crear_Dist(d, x=y, titulo="Histograma "+str(y), color=colors_hex[i]))
                
    case "Estadísticas":
    
        des=myData.getStad(d=st.session_state.d)

        sum=myData.getSum(d=st.session_state.d).drop(columns="Fecha")

        st.subheader("- Estadísticas", divider=True)
        with stylable_container(
            key="std",
            css_styles=css_p
        ):
            st.write(des.to_html(), unsafe_allow_html=True)

        st.subheader("- Suma", divider=True)
        with stylable_container(
            key="sum",
            css_styles=css_p
        ):
            st.write(sum.to_html(), unsafe_allow_html=True)
