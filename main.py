from requisition_system import RequisitionSystem

def build_demo_system():
    system = RequisitionSystem()

    system.create_requisition(
        "03/04/2026", "0009", "Alex Green",
        [("Keyboard", "20.00"), ("Mouse", "14.00")],
    )
    system.create_requisition(
        "04/04/2026", "FN19", "Sam Patel", [("Office chair", "499.99")]
    )
    exact_limit = system.create_requisition(
        "05/04/2026", "FN20", "Tracy Brown", [("Monitor", "500.00")]
    )
    over_limit = system.create_requisition(
        "06/04/2026", "FN21", "Jordan Lee", [("Laptop", "790.00")]
    )
    system.create_requisition(
        "07/04/2026", "FN22", "Morgan Smith", [("Printer", "650.00")]
    )

    system.respond_to_requisition(
        exact_limit.requisition_id, "Approved", "Taylor Manager"
    )
    system.respond_to_requisition(
        over_limit.requisition_id, "Not approved", "Taylor Manager"
    )
    return system


def run_demo():
    
    system = build_demo_system()
    print("STAFF PURCHASE REQUISITION SYSTEM - ASSESSMENT 2")
    print("Automatic approval: total below $500.00")
    print("Manager decision required: total of $500.00 or more")
    print("\nSAMPLE REQUISITIONS")
    print("=" * 88)

    for record in system.get_requisition_records():
        print(
            f"{record['requisition_id']} | {record['staff_name']:<15} | "
            f"${record['total']:>8.2f} | {record['status']:<12} | "
            f"{record['approval_reference']}"
        )

    print("\nFINAL STATISTICS")
    print("=" * 32)
    for label, value in system.get_statistics().items():
        print(f"{label:<18}: {value}")


if __name__ == "__main__":
    run_demo()
