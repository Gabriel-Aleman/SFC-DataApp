#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import plotly
from io import BytesIO

def addMDCOLinf(func): #Decorador para añadir una columna con el md a cualquier informe
    def wrap(self, *args, **kwargs):
        resFunc=func(self, *args, **kwargs)
        resFunc["MD"]=[self.session.loc[i]["matchDay"] for i in self.df["Sesión"].to_list()]
        return resFunc
    return wrap

class myData():
    def __init__(self, df=pd.DataFrame(np.nan, index=range(3), columns=range(3))):
        self.df = df
        self.players        = None
        self.session        = None

    #INICIALIZADOR DE "d":
    def inicializar_d(func):
        def wrapper(self, d=None, trydf_f=False, *args, **kwargs):
            if d is None:
                d = self.df_st.copy() if not trydf_f else self.df_f.copy()
            return func(self, d=d, trydf_f=trydf_f, *args, **kwargs)
        return wrapper

    #Cargar data frame de un archivo excel:
    def loadDf_fromExcel(self, fileName="informe.xlsx"):
        self.df = pd.read_excel(fileName, sheet_name="informe")
        self.players = pd.read_excel(fileName, sheet_name="jugadores")
        self.players =self.players.set_index("id")

        self.session = pd.read_excel(fileName, sheet_name="sesiones")
        self.session = self.session.set_index("id")
    
    #DF con la información más normaliza
    def getStyledInf(self):
        self.df_st=self.df.copy()
        self.df_st["Sesión"] = self.session.loc[self.df["Sesión"].to_list()]["Nombre"] .to_list()
        self.df_st = self.df_st[self.df.columns[1:]] #Omitir la columna de id

    #Diccionario con los jugadores x posición
    def jugXpos(self):
        self.jugxPos={}
        for pos in self.players["Posición"]:
            jugNom=self.players.query("Posición == @pos")[["Nombre", "Apellido"]]
            jugNom["Nombre completo"] = jugNom["Nombre"]+" "+jugNom["Apellido"] 
            jugNom=jugNom["Nombre completo"].to_list()
            self.jugxPos[pos]=jugNom

    #SESIONES REPETIDAS:
    #Encontrar las sesiones cuyo nombre se repite en una lista:
    def repeatedSes(self):
        sesSiones=[]
        repetidas=[]

        for indx in self.session.index:
            sesName = self.session.loc[indx]["Nombre"]
            if sesName in sesSiones:
                repetidas.append(sesName)
            sesSiones.append(sesName)
        return repetidas

    #Crear un listado de sesiones donde la columna de nombre ahora es irrepetible:
    #inputs:    -Lista de sesiones repetidas
    #           -Boleano para saber si todas las columnas se les debe hacer un append de fecha
    def filtSes(self, repetidas=[], all=False):
        sesSiones=self.session["Nombre"].to_list()

        for i,indx  in enumerate(self.session.index):
            sesName = self.session.loc[indx]["Nombre"]

            if sesName  in repetidas or all:
                sesSiones[i]=sesName+f" ({self.session.loc[indx]["Creado"].strftime("%Y-%m-%d %H:%M:%S")})"

        sessionF=self.session.copy()
        sessionF["Nombre"] = sesSiones
        self.session_nr = sessionF # Sesiones con nombre que no se repite

        return sessionF
    
    #Crear un informe donde la columna de sesión ahora es irrepetible:
    #inputs:    -df de sesiones donde ya el nombre es irrepetible
    
    def infFilteredSesions(self, sessionF):
        #----------------------------------------------------------------------------
        df=self.df.copy()
        ses=[sessionF.loc[indx]["Nombre"] for indx in df["Sesión"].to_list()]

        df=self.df_st.copy()
        df["Sesión"]=ses
        return df
        #----------------------------------------------------------------------------
    
    #Informe con informe sin sesiones repetidas en formato completo
    @addMDCOLinf
    def infFilteredSesions_comp(self, all=True):
        if not(all):
            repetidas= self.repeatedSes()
            sessionF=self.filtSes(repetidas)
        else:
            sessionF=self.filtSes(all=True)
        self.infFilteredSesionsDF =self.infFilteredSesions(sessionF)
        return self.infFilteredSesionsDF 
    


    #FILTROS:
    #--------------------------------------------------------------------------------------------------------------------------------------------
    #   -- df_f: df filtrado

    #Obtener los jugadores de determindada posición:
    @inicializar_d
    def getJugsInPos(self, valores,  d=None, trydf_f=False):
        if type(valores) is None:
            valores = pd.unique(self.players["Posición"])

        p=self.players.copy()

        posXJugComp={} #Posición de cada jugador

        for i in p.index: #Iterar sobre cada jugador
            nombre=p.loc[i]["Nombre"]+" "+p.loc[i]["Apellido"]
            posicion=p.loc[i]["Posición"]
            posXJugComp[nombre] = posicion

        #Posiciones de cada jugador        
        posiciones=[]
        for i in d.index:
            jug=d.loc[i]["Jugador"]
            try:
                posJug=posXJugComp[jug]
            except:
                posJug="Sin datos de posicicón"
            posiciones.append(posJug)
            
        d["Posiciones"]=posiciones
        try:
            d=d[d["Posiciones"].isin(valores)].drop(columns="Posiciones")
        except TypeError:
            return None
        
        self.df_f = d
        return d
    
    #Obtener las sesiones para un(os) determinados MD:
    @inicializar_d
    def getSesInMD(self, valores,  d=None, trydf_f=False, d_sec=None):
        if valores is None:
            valores = pd.unique(self.players["Posición"])
        md=[]

    
        ds = self.df["Sesión"] if(d_sec is None) else d_sec

        for i in ds:
            sesion=self.session.loc[i]
            md.append(sesion["matchDay"])
        d["MD"]=md
        
        d=d[d["MD"].isin(valores)].drop(columns="MD")
        self.df_f = d
        return d
    
    @inicializar_d
    def getSesInTimeRange(self, valores,  d=None, trydf_f=False):
        limInf,limSup = valores
        d=d.query("Duración <=@limSup and Duración >=@limInf")
        self.df_f = d
        return d
    
    @inicializar_d
    def getSesInDateRange(self, valores,  d=None, trydf_f=False):
        limInf,limSup = valores
        d['f'] = pd.to_datetime(d['Fecha'])
        d=d.query("f  <=@limSup and f  >=@limInf").drop(columns="f")
        self.df_f = d
        return d
    #--------------------------------------------------------------------------------------------------------------------------------------------
    # Estadísticas:
    @inicializar_d
    def getStad(self, d=None, trydf_f=False):
        
        estadisticas = d.describe()
        estadisticas.index = [
            "Cantidad",       # count
            "Promedio",       # mean
            "Desviación Estándar", # std
            "Mínimo",         # min
            "25% Percentil",  # 25%
            "Mediana (50%)",  # 50%
            "75% Percentil",  # 75%
            "Máximo"          # max
        ]
        return estadisticas
    #Suma:
    @inicializar_d
    def getSum(self, d=None, trydf_f=False):
        df_sum=d.sum().round(2)
        df_sum.name ="Suma"
        df_sum=pd.DataFrame(df_sum).T
        return df_sum
    
    @inicializar_d
    def getZScore(self, d=None, trydf_f=False, of=True):
        # Filtrar solo las columnas de tipo float
        float_columns =d.copy()
        float_columns.set_index(["Fecha", "Sesión","Jugador"], inplace=True)
        # Calcula el promedio y la desviación estándar de cada columna
        mean = float_columns.mean()
        std = float_columns.std()

        # Calcula el Z-Score
        zscore_df = (float_columns - mean) / std
        
        return zscore_df
    
# Descargar el informe:
def create_excel_file(dfs):
    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        
        for i,df in dfs.items():  # df adicionales pasados por el usuario:
                        # 1er elemento: df - 2do elemento: label
            
            df.to_excel(writer, sheet_name=i)


    buffer.seek(0)
    return buffer.getvalue()
