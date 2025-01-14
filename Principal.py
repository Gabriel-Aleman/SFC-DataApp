from headers import *

#Variables globales
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if "inf" not in st.session_state: #Filtrado simple o complejo
    st.session_state.inf = 'Filtrado tradicional'

if "df" not in st.session_state:
    st.session_state.df = None


st.set_page_config(
    page_title="SFC DATA APP",
    page_icon=image_path
)
st.logo("https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Sporting_Football_Club_2019.png/157px-Sporting_Football_Club_2019.png")



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


with st.sidebar:

    selected = option_menu("Filtrado", ['Filtrado tradicional',"Filtrado complejo"], 
        icons=['file-earmark-text', 'file-earmark-text-fill'], menu_icon="gear", default_index=0)
    st.session_state.inf = selected
    add_vertical_space(1)

    # Logo
    html_code = f"""
    <style>
    img {{
        border-radius: 15px;
    }}
    </style>
    <img src="{image_path}" width="100">
    """
    st.link_button("🔗 Visita la página principal", "https://sporting.cr/")

    badge(type="twitter", name="SportingCP")

    add_vertical_space(2)
    
    
    st.markdown(html_code, unsafe_allow_html=True)

# Título de la aplicación
#--------------------------------------------------------------------------
st.header("SPORTING-FC :blue[Data App] :soccer:", divider=True)

add_vertical_space(1)
#--------------------------------------------------------------------------



tab1, tab2, tab3, tab4 = st.tabs(["📄Informe", "🖩Estadísticas", "Z-Score", "📊Gráficos"])
col1, col2, col3, col4 = st.columns(4)


#Informe:
with tab1:
    if st.session_state.inf == 'Filtrado complejo':
        st.session_state.df = dataframe_explorer(myData.df_st, case=False)

    else:
        with st.expander("### • Filtros"):

            col1, col2, col3, col4 = st.columns(4)
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
                    
            with col4:
                ops_Pos=pd.unique(myData.players["Posición"])
                with st.popover("📍 X Posición"):
                    pos = st.multiselect("Qué posisición le interesa",ops_Pos, default=ops_Pos)
        
        myData.getSesInMD(valores=md)
        myData.getJugsInPos(valores=pos, trydf_f=True)
        myData.getSesInTimeRange(valores=t, trydf_f=True)
        try:
            myData.getSesInDateRange(valores=date_range, trydf_f=True)
        except:
            pass
        
        st.session_state.df = myData.df_f

    st.dataframe(st.session_state.df.reset_index(drop=True))
    st.info(f"📝 {len(st.session_state.df)} datos en la busqueda") 
    
    des=myData.getStad(d=st.session_state.df).round(4)

    d=st.session_state.df[st.session_state.df.columns[4:]].copy()
    sum=myData.getSum(d).round(4)

    z=myData.getZScore(d=st.session_state.df)
    zn=z.copy()
    try:
        zn.drop("Duración")
    except:
        pass
#Estadísticas:
with tab2:
    from plotlyFuncs import plotTable
    st.subheader("Descripción general", divider=True)
    with stylable_container(
        key="std",
        css_styles=css_p
    ):
        st.write(des.drop(columns=["Duración"]).to_html(), unsafe_allow_html=True)

    st.subheader("Suma", divider=True)
    with stylable_container(
        key="sum",
        css_styles=css_p
    ):
        st.write(sum.to_html(), unsafe_allow_html=True)

#Z SCORE
with tab3:
    with st.expander("Tabla", expanded=True):
        st.dataframe(zn)
    with st.expander("Gráfico", expanded=True):
        st.scatter_chart(zn.reset_index(drop=True), y_label="Z-Scores")
st.markdown("---")
#----------------------------------------------------------------------------------------------------------------------
col1, col2, col3 = st.columns([2,2,1])

inf={"Informe":st.session_state.df,
     "Estadísticas":des.drop(columns=["Duración"]),
     "Z-Scroes":z.reset_index(drop=True),
     "Suma": sum}
exc=create_excel_file(inf)
with col1:
    st.download_button(label="Descargar archivo Excel",data=exc,file_name=f'informeCompleto_{datetime.now()}.xlsx', type="secondary", icon=":material/download:")


#Gráficos
with tab4:
    from plotlyFuncs import *
    with st.container(border=True):
        plot_type = st.radio("Selecciona el tipo de gráfico:", ["Histograma","Distribución", "Box Plot", "Matriz-correlación"], horizontal=True)
    d=st.session_state.df
    arrValues=["Distancia total", "Velocidad máxima", "HSR", "SPRINT", "acc", "dec"]


    if plot_type=="Histograma":
        bins = st.slider("Selecciona el número de bins", min_value=5, max_value=50, value=10)
    
    if plot_type=="Matriz-correlación":
            st.plotly_chart(mapa_correlacion_todas_las_columnas(d.drop(columns=["Fecha", "Sesión", "Jugador", "Duración"]),"Matriz de correlación"), key="mat")
    else: #TODO: ARREGLAR EN JUGADOR
        for i,y in enumerate(arrValues):
            
            if plot_type=="Box Plot":
                st.plotly_chart(crear_boxplot(d, y=y, titulo="Box Plot "+str(y), color=colors_hex[i]))
            elif plot_type=="Histograma":
                st.plotly_chart(crear_histograma(d, x=y, titulo="Histograma "+str(y), color=colors_hex[i], bins=bins))
            elif plot_type=="Distribución":
                st.plotly_chart(crear_Dist(d, x=y, titulo="Histograma "+str(y), color=colors_hex[i]))
