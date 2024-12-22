class ReportTemplates:
    @staticmethod
    def daily_report_template():
        return {
            "date": None,
            "repositories": {},
            "summary": {"total_commits": 0, "total_issues": 0, "total_prs": 0},
            "highlights": [],
            "concerns": [],
            "next_steps": [],
        }

    @staticmethod
    def weekly_report_template():
        return {
            "period": {"start": None, "end": None},
            "progress": {
                "completed_tasks": [],
                "ongoing_tasks": [],
                "blocked_tasks": [],
            },
            "metrics": {"velocity": 0, "completion_rate": 0, "bug_rate": 0},
            "analysis": {"achievements": [], "challenges": [], "risks": []},
            "recommendations": [],
        }

    @staticmethod
    def status_report_template():
        return {
            "timestamp": None,
            "projects": {},
            "overall_health": "green",  # green, yellow, red
            "active_tasks": 0,
            "blocked_tasks": 0,
            "resource_utilization": 0,
            "key_metrics": {"sprint_progress": 0, "bug_count": 0, "technical_debt": 0},
        }
