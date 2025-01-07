#Importar librerías:
#---------------------------------------------------------

import hmac
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.let_it_rain import rain
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.badges import badge
from datetime import datetime
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_option_menu import option_menu
import plotly.express as px
from myDf import *
#CARGAR ARCHIVOS CSS:
#---------------------------------------------------------
f=open("css/tableInf.css")
css=f.read()
f.close()


f=open("css/table_play.css")
css_p=f.read()
f.close()


#---------------------------------------------------------

#Cargar datos
#-------------------------------------------------------------------------------------------
myData=myData()
myData.loadDf_fromExcel()
myData.getStyledInf()

#Primer registro en la historia:
fr= myData.df.sort_values(by="Fecha")["Fecha"].iloc[0]
fr = datetime.strptime(fr,  "%Y-%m-%d %H:%M")

#Último registro en la historia:
lr= myData.df.sort_values(by="Fecha")["Fecha"].iloc[-1]
lr = datetime.strptime(lr,  "%Y-%m-%d %H:%M")
#-------------------------------------------------------------------------------------------
image_path = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTD-ViQjMELIoVlV44DnXliYZoV2knLJ218zQ&s"

