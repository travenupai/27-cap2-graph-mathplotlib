from crewai.tools import BaseTool
import matplotlib.pyplot as plt
from pydantic import BaseModel, Field

# Input model para validar os dados recebidos pela ferramenta
class CustomGraphToolInput(BaseModel):
    values: list[float] = Field(..., description="Lista de valores para o gráfico.")
    labels: list[str] = Field(..., description="Lista de rótulos correspondentes aos valores.")
    chart_type: str = Field(..., description="Tipo de gráfico: 'linha', 'barras' ou 'pizza'.")
    title: str = Field(..., description="Título do gráfico.")

# Implementação da ferramenta personalizada
class CustomGraphTool(BaseTool):
    """
    Ferramenta de criação de gráficos
    """
    name: str = "Gerador de Gráficos"
    description: str = (
        "Gera um gráfico com base em uma lista de valores e um tipo de gráfico especificado "
        "(linha, barras ou pizza) e salva o gráfico como um arquivo PNG."
    )
    args_schema = CustomGraphToolInput

    def _run(self, values: list[float], labels: list[str], chart_type: str, title: str) -> str:
        """
        Gera um gráfico com base nos dados fornecidos e salva como um arquivo PNG.
        """
        # Valida os tipos de gráficos suportados
        plt.figure()
        if chart_type == "linha":
            plt.plot(values)
            plt.title(title)
        elif chart_type == "barras":
            plt.bar(range(len(values)), values, tick_label=labels)
            plt.title(title)
        elif chart_type == "pizza":
            plt.pie(values, labels=labels, autopct='%1.1f%%')
            plt.title(title)
        else:
            return "Erro: Tipo de gráfico inválido. Escolha entre 'linha', 'barras' ou 'pizza'."

        # Salva o gráfico como arquivo PNG
        file_name = f"{title.lower().replace(' ', '_')}.png"
        plt.savefig(file_name)
        plt.close()

        return f"Gráfico salvo como {file_name}"

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError("Esta ferramenta não suporta execução assíncrona.")
