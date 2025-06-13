# GP_AI_memorist

This repository contains a simple prototype for a multi-agent system. The
current implementation focuses on **Agente 3** ("Agente del Diseño
Metodológico y Desarrollo Técnico"), which is responsible for generating a
methodological design plan for a given project description.

## Usage

```python
from service.agent3 import DesignMethodologyAgent

agent = DesignMethodologyAgent()
plan = agent.run("Desarrollo de una plataforma de IA para memoristas")
print(plan)
```

The `run` method returns a series of methodological steps to guide the
technical development of the project.
