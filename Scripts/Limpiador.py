import pandas as pd  
import time  
import os

def leer_csv(archivo_entrada):
    try:  
        df = pd.read_csv(archivo_entrada, skiprows=1, names=["Fecha", "Canal", "Titulo", "Nombre Capitulo", "Descripcion", "Info adicional", "Horario"])  
        return df
    except Exception as e:  
        print(f"Error al leer el archivo: {e}")  
        return None  

def limpiar_datos(df):
    df.dropna(subset=["Fecha", "Canal", "Titulo", "Horario"], inplace=True)  
    df["Fecha"] = pd.to_datetime(df["Fecha"], format="%Y-%m-%d", errors="coerce")
    return df

def extraer_horario(horario):
    try:  
        hora_inicio = horario.split(" - ")[0]  
        return pd.to_datetime(hora_inicio, format="%I:%M%p").time()
    except Exception as e:  
        print(f"Error al convertir horario '{horario}': {e}")  
        return None  

def analizar_emisiones(df):
    titulo_mas_emisiones = df["Titulo"].value_counts().idxmax()  
    cantidad_titulo = df["Titulo"].value_counts().max()  

    canal_mas_emisiones = df["Canal"].value_counts().idxmax()  
    cantidad_canal = df["Canal"].value_counts().max()  

    nuevas_filas = pd.DataFrame([  
        {"Fecha": "Programa con más emisiones", "Canal": titulo_mas_emisiones, "Titulo": cantidad_titulo},  
        {"Fecha": "Canal con más emisiones", "Canal": canal_mas_emisiones, "Titulo": cantidad_canal}  
    ])  
    return nuevas_filas

def obtener_top_programas(df):
    top_programas = df["Titulo"].value_counts().head(10).reset_index()  
    top_programas.columns = ["Titulo", "Emisiones"]  
    top_programas.insert(0, "Fecha", "Top 10 Programas")  
    return top_programas

def obtener_programas_por_canal(df):
    programas_por_canal = df["Canal"].value_counts().reset_index()  
    programas_por_canal.columns = ["Canal", "Cantidad de Programas"]  
    programas_por_canal.insert(0, "Fecha", "Programas por Canal")  
    return programas_por_canal

def categorizar_horario(hora):
    if pd.isna(hora):  
        return "Desconocido"  
    if hora < pd.to_datetime("12:00 PM", format="%I:%M %p").time():  
        return "Mañana"  
    elif hora < pd.to_datetime("06:00 PM", format="%I:%M %p").time():  
        return "Tarde"  
    else:  
        return "Noche"  

def obtener_distribucion_franja_horaria(df):
    df["Franja_Horaria"] = df["Horario"].apply(categorizar_horario)  
    franja_counts = df["Franja_Horaria"].value_counts().reset_index()  
    franja_counts.columns = ["Franja Horaria", "Cantidad de Programas"]  
    franja_counts.insert(0, "Fecha", "Distribución Horaria")  
    return franja_counts

def guardar_csv(df_final, archivo_salida):
    df_final.to_csv(archivo_salida, index=False)  

def limpiar_csv(archivo_entrada, archivo_salida):
    archivo_entrada = os.path.join(".", "Files", archivo_entrada)
    archivo_salida = os.path.join(".", "Files", archivo_salida)
    start_time = time.time()  

    df = leer_csv(archivo_entrada)
    if df is None:
        return

    df = limpiar_datos(df)
    df["Horario"] = df["Horario"].apply(extraer_horario)

    nuevas_filas = analizar_emisiones(df)
    df = pd.concat([df, nuevas_filas], ignore_index=True)

    top_programas = obtener_top_programas(df)
    programas_por_canal = obtener_programas_por_canal(df)
    franja_counts = obtener_distribucion_franja_horaria(df)

    df_final = pd.concat([df, top_programas, programas_por_canal, franja_counts], ignore_index=True)
    guardar_csv(df_final, archivo_salida)

    execution_time = time.time() - start_time
    print(f"Limpieza y análisis completados en {execution_time:.2f} segundos.")

txt_entrada = "tv_guide_data_ultimate.csv"  
txt_salida = "clean_tv_guide_data_ultimate.csv"  

limpiar_csv(txt_entrada, txt_salida)
