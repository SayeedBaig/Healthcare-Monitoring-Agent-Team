import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.db_operations import fetch_fitness
from agents.langgraph_workflow import run_workflow


def test_csv_and_goals():
    # basic smoke tests
    out = run_workflow(1)
    assert "risk" in out
    assert isinstance(fetch_fitness(), dict)

if __name__ == "__main__":
    print("Workflow sample:", run_workflow(1))
    print("Latest fitness:", fetch_fitness())
