# agents/interaction_checker.py
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

    return conflicts
