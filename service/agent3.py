from service.base import Agent


class DesignMethodologyAgent(Agent):
    """Agent responsible for methodological design and technical development."""

    def __init__(self):
        super().__init__(
            name="Agente del Diseño Metodológico y Desarrollo Técnico"
        )

    def run(self, project_description: str) -> str:
        """Generate a basic methodological plan given a project description."""
        steps = [
            "1. Identificar los requerimientos técnicos y objetivos del proyecto.",
            "2. Proponer un enfoque metodológico adecuado al alcance.",
            "3. Definir la arquitectura de desarrollo y herramientas a emplear.",
            "4. Establecer un plan de pruebas y evaluación técnica.",
            "5. Documentar el proceso y resultados.",
        ]
        if project_description:
            steps.insert(0, f"Proyecto: {project_description}")
        return "\n".join(steps)
