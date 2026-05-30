import mlflow
from src.config import *

def evaluar(prompt, respuesta):

    mlflow.log_param("modelo", MODEL_NAME)

    mlflow.log_metric("longitud_respuesta", len(respuesta))
    mlflow.log_metric("longitud_prompt", len(prompt))
    mlflow.log_metric("ratio", len(respuesta)/len(prompt))

    contiene_numeros = sum(c.isdigit() for c in respuesta) > 5
    mlflow.log_metric("usa_datos_numericos", int(contiene_numeros))

    palabras_clave = ["ICC", "PMI", "IPEC", "ISE"]
    score_keywords = sum(1 for p in palabras_clave if p in respuesta)
    mlflow.log_metric("uso_indicadores", score_keywords)

    coherencia = 1 if "Conclusión" in respuesta else 0
    mlflow.log_metric("estructura_correcta", coherencia)

    mlflow.log_text(prompt, "prompt.txt")
    mlflow.log_text(respuesta, "respuesta.txt")