from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
from src.graph.MyLLM import MyLLM
from src.graph.tools.graph_tool import CustomGraphTool

serper_tool = SerperDevTool ()
serper_tool.n_results = 50
load_dotenv()
llm = MyLLM.gpt4o_mini

# Uncomment the following line to use an example of a custom tool
# from graph.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class Graph():
	"""Graph crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def researcher_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher_agent'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			allow_delegation=False,
			llm=llm,
		)

	@agent
	def graph_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['graph_agent'],
			tools=[CustomGraphTool()],
   			verbose=True,
			allow_delegation=False,	
			llm=llm,	
		)

	@task
	def energy_research_task(self) -> Task:
		return Task(
			config=self.tasks_config['energy_research_task'],
		)

	@task
	def graph_creation_task(self) -> Task:
		return Task(
			config=self.tasks_config['graph_creation_task'],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Graph crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
