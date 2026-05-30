import streamlit as st
import matplotlib.pyplot as plt
import mlflow
import tempfile
import time

from src.rag_chain import generar_informe
from src.evaluate import evaluar
from src.config import MLFLOW_EXPERIMENT, MLFLOW_TRACKING_URI

# =====================
# 🎨 ESTILOS CSS
# =====================
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}

.main {
    background-color: #ffffff;
    padding: 1rem;
    border-radius: 10px;
}

h1 {
    color: #1f3b4d;
}

h3 {
    color: #2c6e91;
}

.stMetric {
    background-color: #f0f4f8;
    padding: 10px;
    border-radius: 10px;
}

.block-container {
    padding-top: 2rem;
}

[data-testid="stSidebar"] {
    background-color: #1f3b4d;
    color: white;
}

[data-testid="stSidebar"] .stDateInput label {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# =====================
# CONFIG MLflow
# =====================
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment(MLFLOW_EXPERIMENT)

# =====================
# CONFIG STREAMLIT
# =====================
st.set_page_config(layout="wide", page_title="Informe Económico")

# =====================
# SIDEBAR
# =====================
st.sidebar.title("Panel de Control")
fecha = st.sidebar.date_input("Selecciona el mes del informe")

st.sidebar.markdown("---")
st.sidebar.write("Aplicación de análisis económico basada en IA")

# =====================
# HEADER
# =====================
st.markdown("## Informe Económico Inteligente")
st.markdown("Análisis automatizado de indicadores macroeconómicos")

# =====================
# BOTÓN
# =====================
if st.sidebar.button("Generar informe"):

    start_time = time.time()

    with mlflow.start_run(run_name="Pipeline"):

        informe, datos, prompt = generar_informe(fecha)

        evaluar(prompt, informe)

        tiempo_total = round(time.time() - start_time, 2)

        mlflow.log_param("fecha_input", str(fecha))
        mlflow.log_metric("tiempo_ejecucion", tiempo_total)
        mlflow.log_metric("check_run", 1)

        # =====================
        # 📊 TARJETAS DE MÉTRICAS
        # =====================
        st.markdown("### Métricas del sistema")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Tiempo (s)", tiempo_total)
        col2.metric("Prompt", len(prompt))
        col3.metric("Respuesta", len(informe))
        col4.metric("Indicadores", sum(i in informe for i in ["ICC", "PMI", "IPEC", "ISE"]))

        df_hist = datos["historico"]

        # =====================
        # 📈 GRÁFICOS
        # =====================
        st.markdown("### Evolución de indicadores")

        fig, axs = plt.subplots(2, 2, figsize=(14, 8))

        colores = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a"]

        indicadores = [
    ("ICC", "Índice de confianza del consumidor - ICC"),
    ("PMI", "índice de gestión de compras - PMI"),
    ("IPEC", "Índice de Incertidumbre de la Política Económica en Colombia - IPEC"),
    ("ISE", "Indicador de Seguimiento a la Economía - ISE")
]
        
        for ax, (titulo, col), color in zip(axs.flatten(), indicadores, colores):

            serie = df_hist[col]

            ax.plot(df_hist["Fecha"], serie, color=color, linewidth=2)

            ax.scatter(df_hist["Fecha"].iloc[-1], serie.iloc[-1], color=color)

            valor_final = round(float(serie.iloc[-1]), 1)

            ax.text(
                df_hist["Fecha"].iloc[-1],
                valor_final,
                f"{valor_final}",
                fontsize=10,
                color=color
            )

            ax.set_title(titulo)
            ax.set_xticks(df_hist["Fecha"][::3])
            ax.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        st.pyplot(fig)

        # guardar gráfica en MLflow
        temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        fig.savefig(temp_file.name)
        mlflow.log_artifact(temp_file.name, "graficas")

        # =====================
        # 📄 INFORME
        # =====================
        st.markdown("### Informe económico generado")

        st.container().markdown(f"""
<div style="background-color:#f0f4f8; padding:20px; border-radius:10px;">
{informe}
</div>
""", unsafe_allow_html=True)

        # =====================
        # 🧠 DEBUG (OCULTO)
        # =====================
        with st.expander("Ver prompt"):
            st.text(prompt)
