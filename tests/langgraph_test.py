# tests/langgraph_test.py
from agents.langgraph_workflow import run_workflow

def test_workflow_runs():
    out = run_workflow(user_id=1)
    assert isinstance(out, dict)
    assert "risk" in out
    assert "report" in out

if __name__ == "__main__":
    print("Workflow output:", run_workflow(1))
