from crewai import Agent


class PortfolioManager:
    def __init__(self, llm):
        self.llm = llm

    def create(self):
        return Agent(
            role="Portfolio Manager",
            goal="Manage and coordinate all development projects",
            backstory="Senior portfolio manager with expertise in multi-project coordination",
            llm=self.llm,
        )
