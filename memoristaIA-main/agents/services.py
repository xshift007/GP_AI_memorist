# agents/services.py

import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

LMSTUDIO_API_URL = os.getenv("LMSTUDIO_API_URL", "http://34.136.0.55:12434/engines/llama.cpp/v1/chat/completions")

def llamar_gemini(prompt: str, retries=3, delay=5) -> str:
    """
    Función para llamar a LM Studio con modelo Mistral (API estilo OpenAI).
    """
    print(f"Usando URL: {LMSTUDIO_API_URL}")
    headers = {
        "Content-Type": "application/json"
    }

    body = {
        "model": "mistral",  # nombre simbólico, LM Studio usará el que esté activo
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    for attempt in range(retries):
        try:
            response = requests.post(LMSTUDIO_API_URL, headers=headers, json=body)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error en el intento {attempt + 1}/{retries}: {e}")
            if attempt < retries - 1:
                print(f"Reintentando en {delay} segundos...")
                time.sleep(delay)
            else:
                print("Error: Se superó el número máximo de reintentos.")
                return None

class AgenteFormulacionContextualizacion:
    """
    Agente 0: Responsable de la Introducción y elementos iniciales de la tesis
    Misión: Generar la Introducción, Planteamiento del Problema, Justificación,
             Definición de Objetivos (Generales y Específicos) y Delimitación del Alcance.
    """

    def generar_esquema(self, tema_tesis: str) -> str:
        """Genera el esquema estructurado para los elementos iniciales de la tesis."""
        print("AIP: Solicitando esquema para Introducción y elementos iniciales.")
        prompt = f"""
        Rol: Eres AFC, un agente experto en redacción académica de tesis relacionadas al área de la informática.

        Tarea: Genera un esquema detallado para el Capítulo 1: 'Introducción y elementos iniciales'.
        Tema de la Tesis: '{tema_tesis}'.

        Instrucciones:
        - Debe incluir las siguientes secciones como títulos numerados:
          1. Introducción
          2. Planteamiento del Problema
          3. Justificación
          4. Objetivos
            4.1 Objetivo General
            4.2 Objetivos Específicos
          5. Delimitación del Alcance
        - Estructura como lista de títulos (ej. 1, 2, 3, etc.).
        - No generar contenido, solo los títulos del esquema.
        """
        esquema = llamar_gemini(prompt)
        return esquema

    def generar_contenido(self, esquema: str, tema_tesis: str, contexto_adicional: str = "") -> str:
        """Genera el contenido completo sección por sección basado en el esquema dado."""
        print("AIP: Iniciando generación de contenido para cada sección.")
        partes = [line.strip() for line in esquema.strip().split('\n') if line.strip()]
        contenido_completo = []

        for titulo in partes:
            print(f"AIP: Generando sección '{titulo}'...")
            contexto_previo = "\n\n".join(contenido_completo)
            prompt = f"""
            Rol: Eres un agente especializado en redacción de tesis.

            Tarea: Redacta la sección '{titulo}'.
            Tema de la Tesis: '{tema_tesis}'.
            Esquema Capítulo 1: {esquema}
            Contexto adicional: '{contexto_adicional}'
            Contenido previo generado: '{contexto_previo[:2000]}...'

            Instrucciones de redacción:
            - Extensión: 1500 palabras mínimas.
            - Estilo: Formal, académico y preciso.
            - Incluye citas en formato APA (placeholder: [Autor, Año]).
            """
            texto_seccion = llamar_gemini(prompt)
            if texto_seccion:
                contenido_completo.append(f"## {titulo}\n\n{texto_seccion}")

        return "\n\n".join(contenido_completo)

    def extraer_programa_obetivos(self, contenido: str) -> tuple[str, list[str]]:
        """Extrae y valida los objetivos generales y específicos del contenido generado."""
        print("AIP: Extrayendo y validando objetivos.")
        prompt = f"""
        Rol: Eres un asistente de investigación.

        Tarea: Del siguiente texto, identifica y retorna:
        1. El enunciado del Objetivo General.
        2. Una lista de Objetivos Específicos.

        Texto:
        {contenido}
        """
        respuesta = llamar_gemini(prompt)
        # Se asume respuesta en un formato parseable, por ejemplo:
        # Objetivo General: ...\nObjetivos Específicos:\n- ...\n- ...
        return respuesta
    
    def generar_resumen(self, contenido_capitulo: str) -> str:
        """Genera un resumen conciso del contenido completo de un capítulo."""
        print("AIP: Generando resumen del capítulo.")
        prompt = f"""
        Rol: Eres un asistente académico.

        Tarea: Lee el contenido completo de un capítulo y genera un resumen claro y conciso de 2-3 párrafos,
        enfatizando los puntos clave y la estructura general.

        Contenido del capítulo:
        {contenido_capitulo}
        """
        resumen = llamar_gemini(prompt)
        return resumen

class AgenteRevisorArte:
    """
    Agente 1: Revisor del Estado del Arte (ARA)
    Misión: Mapear la investigación existente e identificar el 'gap' o vacío.
    """

    def generar_esquema(self, tema_tesis: str, resumen_cap1: str) -> str:
        """Genera el esquema para el capítulo del Estado del Arte."""
        print("ARA: Solicitando esquema del Estado del Arte.")
        prompt = f"""
        Rol: Eres ARA, un Agente experto en redacción de revisiones de literatura para tesis doctorales.

        Tarea: Genera un esquema detallado y bien estructurado para el Capítulo 2: 'Revisión del Estado del Arte'. La tesis trata sobre '{tema_tesis}'.

        Contexto del Capítulo 1 (Formulación y Contextualización):
        {resumen_cap1}

        Instrucciones para el Esquema:
        - El esquema debe estructurar una revisión exhaustiva de la literatura.
        - Divídelo en al menos 5-7 secciones y subsecciones principales lógicas (ej. 2.1, 2.1.1, 2.2, etc.).
        - El objetivo final es construir un argumento que culmine en la identificación clara de un vacío de investigación (research gap).
        - Estructura la salida como una lista de títulos de sección. No generes el contenido, solo los títulos del esquema.
        """
        esquema = llamar_gemini(prompt)
        return esquema

    def generar_capitulo_completo(self, esquema: str, tema_tesis: str, resumen_cap1: str) -> tuple[str, str]:

        """
        Genera el contenido completo del capítulo sección por sección y extrae el 'gap'.
        Devuelve una tupla: (texto_completo_capitulo, resumen_del_gap)
        """
        print("ARA: Iniciando generación del capítulo completo por secciones.")
        capitulo_completo = []
        # Asumimos que el esquema viene como una lista de títulos, uno por línea.
        secciones = [sec for sec in esquema.strip().split('\n') if sec.strip()]
        
        for i, seccion_titulo in enumerate(secciones):
            print(f"ARA: Generando sección '{seccion_titulo}'...")
            contexto_previo = "\n\n".join(capitulo_completo)
            
            prompt = f"""
            Rol: Eres ARA, un experto en redacción de revisiones de literatura.

            Tarea: Redacta la sección '{seccion_titulo}' del Capítulo 2: 'Revisión del Estado del Arte'.

            Contexto General:
            - Tema de Tesis: '{tema_tesis}'
            - Resumen del Capítulo 1: '{resumen_cap1}'
            - Esquema General del Capítulo 2: {esquema}
            - Contenido de secciones anteriores ya redactadas: '{contexto_previo[:2000]}...'

            Objetivo de esta Sección:
            Desarrolla el contenido para '{seccion_titulo}' de manera formal, técnica y académica. Asegúrate de que fluya lógicamente desde las secciones anteriores y construya hacia el objetivo final del capítulo.

            Instrucciones de Redacción:
            - Extensión aproximada para esta sección: 800-1200 palabras.
            - Estilo: Formal, técnico y académico. Utiliza un lenguaje preciso.
            - Citas: Incluye citas relevantes en formato APA 7. Puedes usar placeholders como [Cita: autor, año] para ser verificados luego.
            """
            contenido_seccion = llamar_gemini(prompt)
            if contenido_seccion:
                capitulo_completo.append(f"## {seccion_titulo}\n\n{contenido_seccion}")

        texto_final_capitulo = "\n\n".join(capitulo_completo)
        
        print("ARA: Extrayendo el resumen del 'gap' de investigación.")
        prompt_gap = f"""
        Rol: Eres un asistente de investigación.
        Tarea: Lee el siguiente capítulo de 'Revisión del Estado del Arte' y extrae un resumen conciso y claro (2-3 párrafos) del 'vacío de investigación' (research gap) que se identifica al final del capítulo. Este resumen será el input para el siguiente agente.

        Capítulo completo:
        {texto_final_capitulo}
        """
        resumen_gap = llamar_gemini(prompt_gap)
        
        return texto_final_capitulo, resumen_gap


class AgenteFundamentadorTeorico:
    """
    Agente 2: Fundamentador Teórico (AFT)
    Misión: Construir el andamiaje teórico para la investigación, basado en el gap identificado.
    """

    def generar_esquema(self, tema_tesis: str, resumen_cap1: str, gap_identificado: str) -> str:
        """Genera el esquema para el capítulo de Fundamentación Teórica."""
        print("AFT: Solicitando esquema de la Fundamentación Teórica.")
        prompt = f"""
        Rol: Eres AFT, un Agente experto en el desarrollo de marcos teóricos para tesis.

        Tarea: Genera un esquema detallado para el Capítulo 3: 'Fundamentación Teórica'.

        Contexto General:
        - Tema de Tesis: '{tema_tesis}'
        - Resumen del Capítulo 1: '{resumen_cap1}'
        - **Vacío de Investigación Identificado (Resultado del Agente anterior):**
          '{gap_identificado}'

        Instrucciones para el Esquema:
        - El esquema debe proponer teorías, modelos y conceptos que sean directamente relevantes para abordar el 'gap' identificado.
        - Justifica la elección de cada componente teórico.
        - Divídelo en secciones lógicas (ej. 3.1 Teoría Principal, 3.2 Modelos Aplicables, 3.3 Definición de Constructos).
        - Estructura la salida como una lista de títulos de sección.
        """
        esquema = llamar_gemini(prompt)
        return esquema

    def generar_capitulo_completo(self, esquema: str, tema_tesis: str, resumen_cap1: str, gap_identificado: str) -> str:
        """Genera el contenido completo del capítulo sección por sección."""
        print("AFT: Iniciando generación del capítulo completo por secciones.")
        capitulo_completo = []
        secciones = [sec for sec in esquema.strip().split('\n') if sec.strip()]

        for seccion_titulo in secciones:
            print(f"AFT: Generando sección '{seccion_titulo}'...")
            contexto_previo = "\n\n".join(capitulo_completo)
            
            prompt = f"""
            Rol: Eres AFT, un experto en marcos teóricos.

            Tarea: Redacta la sección '{seccion_titulo}' del Capítulo 3: 'Fundamentación Teórica'.

            Contexto General:
            - Tema de Tesis: '{tema_tesis}'
            - Resumen del Capítulo 1: '{resumen_cap1}'
            - Vacío de Investigación que se debe abordar: '{gap_identificado}'
            - Esquema General del Capítulo 3: {esquema}
            - Contenido de secciones anteriores ya redactadas: '{contexto_previo[:2000]}...'

            Objetivo de esta Sección:
            Desarrolla el contenido para '{seccion_titulo}', explicando las teorías/conceptos y argumentando su relevancia para resolver el 'gap' de investigación.

            Instrucciones de Redacción:
            - Extensión aproximada para esta sección: 800-1200 palabras.
            - Estilo: Formal y académico.
            - Citas: Cita a los autores fundacionales de las teorías. Formato APA 7, usando placeholders.
            """
            contenido_seccion = llamar_gemini(prompt)
            if contenido_seccion:
                capitulo_completo.append(f"## {seccion_titulo}\n\n{contenido_seccion}")

        return "\n\n".join(capitulo_completo)


# --- Lógica del Orquestador (Simulación) ---
if __name__ == '__main__':
    # 1. Definir los inputs iniciales
    TEMA_TESIS = "Impacto de la Inteligencia Artificial Generativa en la Educación Superior: Un Análisis de Nuevas Metodologías de Enseñanza y Evaluación."
    RESUMEN_CAPITULO_1 = "El Capítulo 1 introduce el auge de la IA generativa (IAG) y su rápida adopción en diversos sectores. Se plantea como problema de investigación la falta de marcos pedagógicos estructurados para integrar eficazmente estas herramientas en la educación superior, generando incertidumbre en docentes y estudiantes sobre su uso y evaluación. Las preguntas de investigación se centran en: ¿Qué metodologías de enseñanza se pueden desarrollar con IAG? y ¿Cómo se pueden diseñar sistemas de evaluación justos y eficaces en este nuevo contexto?"


    print("===== INICIANDO PROCESO DE GENERACIÓN DE TESIS =====")
    
    # 2. Instanciar Agentes
    afc = AgenteFormulacionContextualizacion()
    ara = AgenteRevisorArte()
    aft = AgenteFundamentadorTeorico()
    
	# 3. FASE 0: Ejecutar Agente Formulador y Contextualizador (AFC)
    print("\n===== FASE 0: AGENTE FORMULADOR Y CONTEXTUALIZADOR (AFC) =====")
    esquema_inicial = afc.generar_esquema(TEMA_TESIS)
    if esquema_inicial:
        print("\n**Esquema del Capítulo 1 generado por AFC:**")
        print(esquema_inicial)
        				
        capitulo_1_texto = afc.generar_contenido(esquema_inicial, TEMA_TESIS)
        				
        print("\n**Capítulo 1 (Formulación y Contextualización) - Primeros 500 caracteres:**")
        print(capitulo_1_texto[:500] + "...")
        				
        # Generar resumen del capítulo 1
        resumen_capitulo_1 = afc.generar_resumen(capitulo_1_texto)
        print("\n**Resumen del Capítulo 1:**", resumen_capitulo_1)
        
        # 3. FASE I: Ejecutar Agente Revisor del Arte (ARA)
        print("\n===== FASE I: AGENTE REVISOR DEL ESTADO DEL ARTE (ARA) =====")
        esquema_arte = ara.generar_esquema(TEMA_TESIS, RESUMEN_CAPITULO_1)
    if esquema_arte:
        print("\n**Esquema del Estado del Arte generado por ARA:**")
        print(esquema_arte)
        
        capitulo_2_texto, gap_identificado = ara.generar_capitulo_completo(esquema_arte, TEMA_TESIS, RESUMEN_CAPITULO_1)
        
        print("\n**Capítulo 2 (Estado del Arte) - Primeros 500 caracteres:**")
        print(capitulo_2_texto[:500] + "...")
        
        print("\n**GAP DE INVESTIGACIÓN (extraído por ARA para AFT):**")
        print(gap_identificado)
        
        # 4. FASE II: Ejecutar Agente Fundamentador Teórico (AFT)
        print("\n===== FASE II: AGENTE FUNDAMENTADOR TEÓRICO (AFT) =====")
        esquema_teorico = aft.generar_esquema(TEMA_TESIS, RESUMEN_CAPITULO_1, gap_identificado)
        if esquema_teorico:
            print("\n**Esquema de Fundamentación Teórica generado por AFT:**")
            print(esquema_teorico)

            capitulo_3_texto = aft.generar_capitulo_completo(esquema_teorico, TEMA_TESIS, RESUMEN_CAPITULO_1, gap_identificado)
            
            print("\n**Capítulo 3 (Fundamentación Teórica) - Primeros 500 caracteres:**")
            print(capitulo_3_texto[:500] + "...")

    print("\n===== PROCESO FINALIZADO =====")