# agents/langgraph_workflow.py
from scripts.db_operations import fetch_medications, fetch_fitness
from agents.interaction_checker import check_med_interaction
from agents.risk_ml import predict_risk  # rule-based in your repo
from agents.report_generator import build_report


class HealthWorkflow:
    """
    Simple orchestrator: fetch -> check interactions -> predict risk -> report
    """
    def __init__(self, user_id: int = 1):
        self.user_id = user_id

    def fetch(self):
        # now pass user_id into DB functions
        meds = fetch_medications(self.user_id)      # list of meds for this user
        fitness = fetch_fitness(self.user_id)       # fitness dict for this user
        return {"medications": meds, "fitness": fitness}

    def check_interactions(self, medications):
        # returns list of conflicts (empty if none)
        return check_med_interaction(medications)

    def compute_risk(self, fitness):
        # fitness expected dict with steps, calories, heart_rate
        return predict_risk(fitness)

    def run(self):
        data = self.fetch()
        meds = data.get("medications", [])
        fitness = data.get("fitness", {})
        conflicts = self.check_interactions(meds)
        risk = self.compute_risk(fitness)

        report = build_report(
            user_id=self.user_id,
            meds=meds,
            fitness=fitness,
            conflicts=conflicts,
            risk=risk,
        )

        return {
            "medications": meds,
            "fitness": fitness,
            "conflicts": conflicts,
            "risk": risk,
            "report": report,
        }


# convenience function
def run_workflow(user_id: int = 1):
    wf = HealthWorkflow(user_id=user_id)
    return wf.run()
