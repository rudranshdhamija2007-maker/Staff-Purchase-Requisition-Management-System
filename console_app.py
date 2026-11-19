from requisition_system import RequisitionSystem


def collect_items():
    items = []
    while True:
        item_name = input("Item name: ").strip()
        item_cost = input("Item cost ($): ").strip()
        items.append((item_name, item_cost))

        answer = input("Add another item? (yes/no): ").strip().lower()
        if answer not in {"yes", "y"}:
            return items


def submit_requisition(system):
    date = input("Date (DD/MM/YYYY): ")
    staff_id = input("Staff ID: ")
    staff_name = input("Staff name: ")
    items = collect_items()

    request = system.create_requisition(date, staff_id, staff_name, items)
    print(f"\nRequisition ID: {request.requisition_id}")
    print(f"Total: ${request.total:.2f}")
    print(f"Status: {request.status}")
    print(f"Reference: {request.approval_reference}")


def manage_requisition(system):
    pending_requests = system.get_pending_requisitions()
    if not pending_requests:
        print("There are no pending requisitions.")
        return

    print("\nPENDING REQUISITIONS")
    for request in pending_requests:
        print(
            f"{request.requisition_id} | {request.staff_name} | "
            f"${request.total:.2f}"
        )

    requisition_id = input("Requisition ID: ")
    decision = input("Decision (Approved/Not approved): ")
    manager_name = input("Manager name: ")
    request = system.respond_to_requisition(
        requisition_id, decision, manager_name
    )
    print(f"Requisition {request.requisition_id}: {request.status}")


def display_requisitions(system):
    records = system.get_requisition_records()
    if not records:
        print("There are no requisitions to display.")
        return

    print("\nALL REQUISITIONS")
    print("-" * 88)
    for record in records:
        print(
            f"ID: {record['requisition_id']} | Date: {record['date']} | "
            f"Staff: {record['staff_name']} ({record['staff_id']})"
        )
        print(f"Items: {record['items']}")
        print(
            f"Total: ${record['total']:.2f} | Status: {record['status']} | "
            f"Reference: {record['approval_reference']}"
        )
        print(f"Decision by: {record['decision_by']}")
        print("-" * 88)


def display_statistics(system):
    statistics = system.get_statistics()
    print("\nREQUISITION STATISTICS")
    print("-" * 32)
    for label, value in statistics.items():
        print(f"{label:<18}: {value}")


def run_console_app():
    system = RequisitionSystem()
    menu_actions = {
        "1": submit_requisition,
        "2": manage_requisition,
        "3": display_requisitions,
        "4": display_statistics,
    }

    while True:
        print("\nSTAFF PURCHASE REQUISITION SYSTEM")
        print("1. Submit a requisition")
        print("2. Manager response")
        print("3. Display all requisitions")
        print("4. Display statistics")
        print("5. Exit")
        choice = input("Select an option: ").strip()

        if choice == "5":
            print("Thank you. Goodbye.")
            break
        if choice not in menu_actions:
            print("Please choose an option from 1 to 5.")
            continue

        try:
            menu_actions[choice](system)
        except ValueError as error:
            print(f"Input error: {error}")


if __name__ == "__main__":
    run_console_app()
