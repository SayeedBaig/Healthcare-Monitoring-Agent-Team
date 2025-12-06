# agents/report_generator.py
from datetime import datetime

def build_report(user_id=1, meds=None, fitness=None, conflicts=None, risk=None):
    meds = meds or []
    fitness = fitness or {}
    conflicts = conflicts or []
    risk = risk or {"level":"Unknown","reason":""}

    summary_lines = []
    summary_lines.append(f"Report for user {user_id} - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    summary_lines.append(f"Risk level: {risk.get('level')} ({risk.get('reason')})")
    if conflicts:
        summary_lines.append("Medication Conflicts:")
        for c in conflicts:
            summary_lines.append(f" - {c}")
    else:
        summary_lines.append("No medication conflicts detected.")
    summary_lines.append(f"Latest fitness: steps={fitness.get('steps')}, calories={fitness.get('calories')}, hr={fitness.get('heart_rate')}")
    report = {
        "summary": "\n".join(summary_lines),
        "medications": meds,
        "fitness": fitness,
        "conflicts": conflicts,
        "risk": risk
    }
    return report
