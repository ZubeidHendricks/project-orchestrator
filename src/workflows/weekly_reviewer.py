import json
import os
from datetime import datetime, timedelta

from crewai import Agent, Crew, Process, Task
from langchain.llms import LlamaCpp


class WeeklyReviewer:
    def __init__(self):
        model_path = os.getenv("LLAMA_MODEL_PATH", "models/llama-2-7b-chat.gguf")
        self.llm = LlamaCpp(
            model_path=model_path,
            temperature=0.7,
            max_tokens=2000,
            n_ctx=4096,
        )
        self.setup_agents()

    def setup_agents(self):
        self.reviewer = Agent(
            role="Project Reviewer",
            goal="Analyze weekly project progress and generate insights",
            backstory="Senior technical analyst with expertise in project evaluation",
            llm=self.llm,
        )

    def generate_weekly_review(self):
        reports = self.collect_weekly_reports()
        analysis = self.analyze_reports(reports)
        self.save_weekly_review(analysis)

    def collect_weekly_reports(self):
        reports = []
        status_path = "status"
        week_ago = datetime.now() - timedelta(days=7)

        for filename in os.listdir(status_path):
            if filename.startswith("status_"):
                file_date = datetime.strptime(filename[7:15], "%Y%m%d")
                if file_date >= week_ago:
                    with open(os.path.join(status_path, filename)) as f:
                        reports.append(json.load(f))

        return reports

    def analyze_reports(self, reports):
        return {
            "period": {
                "start": (datetime.now() - timedelta(days=7)).isoformat(),
                "end": datetime.now().isoformat(),
            },
            "summary": self.generate_summary(reports),
            "recommendations": self.generate_recommendations(reports),
        }

    def save_weekly_review(self, review):
        weekly_path = "reports/weekly"
        if not os.path.exists(weekly_path):
            os.makedirs(weekly_path)

        filename = f"{weekly_path}/review_{datetime.now().strftime('%Y%m%d')}.json"
        with open(filename, "w") as f:
            json.dump(review, f, indent=2)
