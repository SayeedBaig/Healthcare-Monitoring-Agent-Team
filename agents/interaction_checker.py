from agents.indian_health_db_tool import check_interaction


def check_med_interaction(med_list):
    """
    med_list: list of medication names OR list of tuples (med_name, schedule)
    Returns: list of conflict messages (empty if none)
    """
    # normalize to names
    names = []
    for m in med_list or []:
        if isinstance(m, (list, tuple)) and len(m) > 0:
            names.append(str(m[0]).lower())
        else:
            names.append(str(m).lower())

    # simple known-conflicts (example)
    conflicts = []
    KNOWN_CONFLICTS = [
        ("warfarin", "aspirin"),
        ("amoxicillin", "methotrexate"),
        ("ibuprofen", "aspirin")
    ]
    for a, b in KNOWN_CONFLICTS:
        if a in names and b in names:
            conflicts.append(f"Interaction detected between '{a}' and '{b}'")

    # duplicate medicine check
    seen = set()
    for n in names:
        if n in seen:
            conflicts.append(f"Duplicate medication entry: '{n}'")
        seen.add(n)

    # --- Indian medicine DB interaction check ---
    n = len(names)
    for i in range(n):
        for j in range(i + 1, n):
            med1 = names[i]
            med2 = names[j]
            desc = check_interaction(med1, med2)
            if desc:
                conflicts.append(
                    f"Indian DB: Interaction between '{med1}' and '{med2}' – {desc}"
                )

    return conflicts
