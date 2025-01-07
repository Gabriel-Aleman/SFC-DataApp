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




st.markdown("----")
sesiones=list(myData.session_nr["Nombre"].to_list())


with st.expander("### • Comparar sesiones"):
    ses0=st.selectbox("Sesión #1", sesiones)
    ses1=st.selectbox("Sesión #2", sesiones)
    
st.markdown("------------")

df0= df.query("Sesión == @ses0 ")
df1= df.query("Sesión == @ses1 ")

jugadoresEnComun= np.intersect1d(df0["Jugador"], df1["Jugador"])
arrValues=["Duración","Distancia total", "Velocidad máxima", "HSR", "SPRINT", "acc", "dec"]

for jug in jugadoresEnComun:
    df0j = df0.query("Jugador == @jug ")
    df1j = df1.query("Jugador == @jug ")
    st.subheader(jug, divider=True)
    with st.container(height=150):

        cols =st.columns(7)
    

        for i,crit in enumerate(arrValues):
            CritLabel= crit
            CritValue= round(df0j[crit], 1)



