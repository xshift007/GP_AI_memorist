from django.shortcuts import render

# Create your views here.
# agents/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import AgenteRevisorArte, AgenteFundamentadorTeorico

class IniciarTesisAPIView(APIView):
    """
    Esta vista actúa como el Orquestador. Recibe los datos iniciales
    y coordina a los agentes para generar los primeros capítulos.
    """
    def post(self, request, *args, **kwargs):
        tema_tesis = request.data.get('tema_tesis')
        resumen_cap1 = request.data.get('resumen_capitulo_1')

        if not tema_tesis or not resumen_cap1:
            return Response(
                {"error": "Los campos 'tema_tesis' y 'resumen_capitulo_1' son requeridos."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # --- El Orquestador en acción ---
            print("ORQUESTADOR: Iniciando proceso...")
            ara = AgenteRevisorArte()
            aft = AgenteFundamentadorTeorico()

            # FASE I: ARA
            print("ORQUESTADOR: Llamando a Agente Revisor del Arte (ARA).")
            esquema_arte = ara.generar_esquema(tema_tesis, resumen_cap1)
            capitulo_2, gap = ara.generar_capitulo_completo(esquema_arte, tema_tesis, resumen_cap1)

            # FASE II: AFT
            print("ORQUESTADOR: Llamando a Agente Fundamentador Teórico (AFT).")
            esquema_teorico = aft.generar_esquema(tema_tesis, resumen_cap1, gap)
            capitulo_3 = aft.generar_capitulo_completo(esquema_teorico, tema_tesis, resumen_cap1, gap)

            # Devolvemos el resultado al frontend
            return Response({
                "mensaje": "Proceso completado exitosamente.",
                "capitulo_2_estado_del_arte": capitulo_2,
                "capitulo_3_fundamentacion_teorica": capitulo_3,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # Manejo de errores durante la generación
            print(f"ERROR EN EL ORQUESTADOR: {e}")
            return Response(
                {"error": f"Ocurrió un error inesperado durante la generación: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )