import pandas as pd

def cargar_excel():
    path = "data/raw/Insumos.xlsx"
    df = pd.read_excel(path)

    df.columns = [col.strip() for col in df.columns]
    df["Fecha"] = pd.to_datetime(df["Fecha"])

    return df


def obtener_datos_mes(df, fecha):

    fecha = pd.to_datetime(fecha)

    df = df.sort_values("Fecha")

    df_filtrado = df[df["Fecha"] <= fecha]
    fila = df_filtrado.iloc[-1]

    fecha_real = fila["Fecha"]

    fecha_inicio = fecha_real - pd.DateOffset(months=24)
    historico = df[(df["Fecha"] >= fecha_inicio) & (df["Fecha"] <= fecha_real)]

    def variacion_anual(col):
        try:
            actual = fila[col]
            pasado = df[df["Fecha"] == fecha_real - pd.DateOffset(years=1)][col].values[0]
            return round(float(actual - pasado), 1)
        except:
            return None

    datos = {
        "fecha_real": fecha_real.date(),

        "ICC": {
            "valor": round(float(fila["Índice de confianza del consumidor - ICC"]), 1),
            "variacion_anual": variacion_anual("Índice de confianza del consumidor - ICC")
        },

        "PMI": round(float(fila["índice de gestión de compras - PMI"]), 1),

        "IPEC": {
            "valor": round(float(fila["Índice de Incertidumbre de la Política Económica en Colombia - IPEC"]), 1)
        },

        "ISE": {
            "valor": round(float(fila["Indicador de Seguimiento a la Economía - ISE"]), 1),
            "crecimiento": round(float(fila["Tasa de crecimiento anual - ISE"]), 1)
        },

        "historico": historico
    }

    return datos