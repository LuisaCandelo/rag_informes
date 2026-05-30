import google.generativeai as genai
from src.config import *
from src.ingest import cargar_excel, obtener_datos_mes
import mlflow

mlflow.set_experiment(MLFLOW_EXPERIMENT)

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(MODEL_NAME)


def generar_informe(fecha):

    df = cargar_excel()
    datos = obtener_datos_mes(df, fecha)

    fecha_real = datos["fecha_real"]

    prompt = f"""
Eres un economista senior especializado en análisis macroeconómico de Colombia.

Tu tarea es elaborar un informe técnico, interpretativo y analítico, similar a los realizados por Fedesarrollo o entidades económicas.

NO debes limitarte a describir cifras. Debes analizar, interpretar y explicar las dinámicas económicas detrás de los indicadores.

=====================
DATOS DEL PERIODO
=====================

Fecha: {fecha_real}

ICC:
Valor: {datos["ICC"]["valor"]}
Variación anual: {datos["ICC"]["variacion_anual"]}

PMI:
Valor: {datos["PMI"]}

IPEC:
Valor: {datos["IPEC"]["valor"]}

ISE:
Valor: {datos["ISE"]["valor"]}
Crecimiento anual: {datos["ISE"]["crecimiento"]}

=====================
CRITERIOS ECONÓMICOS
=====================

ICC:
- Mide confianza del consumidor
- Valores positivos → optimismo
- Valores negativos → pesimismo
- Analizar consumo de hogares

PMI:
- > 50 → expansión
- < 50 → contracción
- Analizar producción, empleo, demanda e inventarios

IPEC:
- Base 100
- > 100 → alta incertidumbre
- Relacionar con decisiones de inversión, riesgo y política económica

ISE:
- Refleja actividad económica
- Analizar dinámica de crecimiento y ciclos económicos

=====================
INSTRUCCIONES DE REDACCIÓN
=====================

Debes redactar un informe estructurado así:

## Informe Económico – {fecha_real}

### 1. Análisis técnico

Para cada indicador:

- Menciona el valor exacto
- Explica su variación (cuando aplique)
- Interpreta el resultado en términos económicos

IMPORTANTE:
- NO listar datos sin análisis
- Explicar el comportamiento del indicador

Ejemplo de estilo esperado:
"El ISE registró un crecimiento de X%, reflejando una aceleración en la actividad económica, posiblemente asociada a..."

---

### 2. Interpretación económica

Aquí debes hacer el análisis más importante:

- Relaciona los indicadores entre sí
- Explica coherencias o contradicciones
- Analiza efectos en:
    • consumo
    • inversión
    • producción
    • confianza

Incorpora análisis como:

- debilitamiento de la demanda
- presiones inflacionarias
- ajuste de inventarios
- incertidumbre económica
- comportamiento empresarial

---

### 3. Conclusión

- Resume la situación económica del periodo
- Identifica riesgos o señales clave
- Evalúa el momento del ciclo económico

=====================
ESTILO
=====================

- Profesional
- Analítico
- Interpretativo
- Claro
- Sin redundancias
- Similar a informes económicos institucionales

IMPORTANTE FINAL:
No inventes datos ni menciones otros periodos.
"""

    mlflow.log_metric("longitud_prompt", len(prompt))

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.2,
            "top_p": 0.9
        }
    )

    texto = response.text

    mlflow.log_metric("longitud_respuesta", len(texto))

    return texto, datos, prompt