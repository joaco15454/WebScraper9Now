import pandas as pd  
import time  

def limpiar_csv(archivo_entrada, archivo_salida):  
    start_time = time.time()  # Iniciar el temporizador  

    # Intentar cargar el CSV y manejar errores  
    try:  
        df = pd.read_csv(archivo_entrada, skiprows=1, names=["Fecha", "Canal", "Titulo", "Nombre Capitulo", "Descripcion", "Info adicional", "Horario"])  
    except Exception as e:  
        print(f"Error al leer el archivo: {e}")  
        return  
    
    # Eliminar filas vacías  
    df.dropna(subset=["Fecha", "Canal", "Titulo", "Horario"], inplace=True)  

    # Convertir "Fecha" a datetime  
    df["Fecha"] = pd.to_datetime(df["Fecha"], format="%Y-%m-%d", errors="coerce")  

    # Convertir "Horario" a formato de tiempo  
    def extraer_horario(horario):  
        try:  
            # Extraer la primera parte del rango horario  
            hora_inicio = horario.split(" - ")[0]  # Toma la parte antes del guion  
            return pd.to_datetime(hora_inicio, format="%I:%M%p").time()  # Convierte a objeto de tiempo  
        except Exception as e:  
            print(f"Error al convertir horario '{horario}': {e}")  
            return None  # Devuelve None si hay un error  

    df["Horario"] = df["Horario"].apply(extraer_horario)  

    # 🔹 Identificar el programa con más emisiones  
    titulo_mas_emisiones = df["Titulo"].value_counts().idxmax()  
    cantidad_titulo = df["Titulo"].value_counts().max()  

    # 🔹 Identificar el canal con más emisiones  
    canal_mas_emisiones = df["Canal"].value_counts().idxmax()  
    cantidad_canal = df["Canal"].value_counts().max()  

    # 🔹 Agregar filas con los datos analizados  
    nuevas_filas = pd.DataFrame([  
        {"Fecha": "Programa con más emisiones", "Canal": titulo_mas_emisiones, "Titulo": cantidad_titulo},  
        {"Fecha": "Canal con más emisiones", "Canal": canal_mas_emisiones, "Titulo": cantidad_canal}  
    ])  

    df = pd.concat([df, nuevas_filas], ignore_index=True)  

    # 📌 Top 10 programas más transmitidos  
    top_programas = df["Titulo"].value_counts().head(10).reset_index()  
    top_programas.columns = ["Titulo", "Emisiones"]  
    top_programas.insert(0, "Fecha", "Top 10 Programas")  

    # 📌 Cantidad de programas por canal  
    programas_por_canal = df["Canal"].value_counts().reset_index()  
    programas_por_canal.columns = ["Canal", "Cantidad de Programas"]  
    programas_por_canal.insert(0, "Fecha", "Programas por Canal")  

    # 📌 Distribución de programas por franja horaria  
    def categorizar_horario(hora):  
        if pd.isna(hora):  # Verifica si hora es NaN  
            return "Desconocido"  
        if hora < pd.to_datetime("12:00 PM", format="%I:%M %p").time():  
            return "Mañana"  
        elif hora < pd.to_datetime("06:00 PM", format="%I:%M %p").time():  
            return "Tarde"  
        else:  
            return "Noche"  

    df["Franja_Horaria"] = df["Horario"].apply(categorizar_horario)  
    franja_counts = df["Franja_Horaria"].value_counts().reset_index()  
    franja_counts.columns = ["Franja Horaria", "Cantidad de Programas"]  
    franja_counts.insert(0, "Fecha", "Distribución Horaria")  


    # Concatenar todos los análisis en un solo dataframe  
    df_final = pd.concat([df, top_programas, programas_por_canal, franja_counts], ignore_index=True)  

    # 🔹 Guardar el CSV limpio con análisis  
    df_final.to_csv(archivo_salida, index=False)    

    execution_time = time.time() - start_time  # Calcular el tiempo de ejecución  
    print(f"✅ Limpieza y análisis completados en {execution_time:.2f} segundos. Datos guardados en '{archivo_salida}'.")  

# Archivos de entrada y salida  
txt_entrada = "tv_guide_data_ultimate.csv"  
txt_salida = "clean_tv_guide_data_ultimate.csv"  

# Ejecutar la función  
limpiar_csv(txt_entrada, txt_salida)
