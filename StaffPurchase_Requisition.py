

from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

APPROVAL_LIMIT = Decimal("500.00")
FIRST_REQUISITION_ID = 10001

APPROVED = "Approved"
PENDING = "Pending"
NOT_APPROVED = "Not approved"
NOT_ISSUED = "Not issued"

def check_text(value, field_name):
    value = str(value).strip()

    if not value:
        raise ValueError(field_name + " is required.")
    return value


def check_date(value):
    value = str(value).strip()

    try:
        datetime.strptime(value, "%d/%m/%Y")
    except ValueError:
        raise ValueError("Enter date as DD/MM/YYYY")

    return value


def check_money(value):
    try:
        amount = Decimal(str(value)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("Enter a valid price, for example 25.50.")

    if not amount.is_finite() or amount < 0:
        raise ValueError("Price must be zero or greater.")

    return amount



class Requisition:

    def __init__(self, date, staff_id, staff_name, requisition_id):
        self.date = check_date(date)
        self.staff_id = check_text(staff_id, "Staff ID")
        self.staff_name = check_text(staff_name, "Staff name")
        self.requisition_id = requisition_id
        self.items = []
        self.total = Decimal("0.00")
        self.status = PENDING
        self.approval_reference = NOT_ISSUED
        self.decision_by = "Awaiting manager"

    def add_item(self, name, cost):
        name = check_text(name, "Item name")
        cost = check_money(cost)

        self.items.append({"name": name, "cost": cost})
        self.calculate_total()

    def calculate_total(self):
        self.total = sum(
            (item["cost"] for item in self.items),
            Decimal("0.00")
        )
        return self.total

    def make_reference(self):
        return self.staff_id + str(self.requisition_id)[-3:]

    def apply_approval_rule(self):
        if not self.items:
            raise ValueError("Add at least one item.")

        self.calculate_total()

        if self.total < APPROVAL_LIMIT:
            self.status = APPROVED
            self.approval_reference = self.make_reference()
            self.decision_by = "Automatic approval rule"
        else:
            self.status = PENDING
            self.approval_reference = NOT_ISSUED
            self.decision_by = "Awaiting manager"

    def manager_decision(self, decision, manager_name):
        if self.status != PENDING:
            raise ValueError("Only pending requests can be updated.")

        manager_name = check_text(manager_name, "Manager name")
        decision = str(decision).strip().lower()

        if decision in ("approve", "approved", "yes"):
            self.status = APPROVED
            self.approval_reference = self.make_reference()
        elif decision in ("reject", "rejected", "not approved", "no"):
            self.status = NOT_APPROVED
            self.approval_reference = NOT_ISSUED
        else:
            raise ValueError("Enter Approved or Not approved.")

        self.decision_by = manager_name


class RequisitionSystem:

    def __init__(self):
        self.requisitions = []
        self.next_id = FIRST_REQUISITION_ID

    def create_requisition(self, date, staff_id, staff_name, items):
        request = Requisition(
            date, staff_id, staff_name, self.next_id
        )

        for name, cost in items:
            request.add_item(name, cost)

        request.apply_approval_rule()
        self.requisitions.append(request)
        self.next_id += 1

        return request

    def find_requisition(self, requisition_id):
        try:
            requisition_id = int(requisition_id)
        except (ValueError, TypeError):
            raise ValueError("Enter a valid requisition ID.")

        for request in self.requisitions:
            if request.requisition_id == requisition_id:
                return request

        raise ValueError("Requisition not found.")

    def manager_response(self, requisition_id, decision, manager_name):
        request = self.find_requisition(requisition_id)
        request.manager_decision(decision, manager_name)
        return request

    def show_all(self):
        if not self.requisitions:
            print("\nNo requisitions have been submitted.")
            return

        print("\nALL REQUISITIONS")
        print("-" * 75)

        for request in self.requisitions:
            print(
                "ID:", request.requisition_id,
                "| Date:", request.date,
                "| Staff:", request.staff_name,
                "| Staff ID:", request.staff_id
            )

            for item in request.items:
                print("   ", item["name"], "- $", format(item["cost"], ".2f"))

            print(
                "Total: $" + format(request.total, ".2f"),
                "| Status:", request.status,
                "| Reference:", request.approval_reference
            )
            print("Decision by:", request.decision_by)
            print("-" * 75)

    def show_pending(self):
        pending_requests = [
            request for request in self.requisitions
            if request.status == PENDING
        ]

        if not pending_requests:
            print("\nThere are no pending requisitions.")
            return False

        print("\nPENDING REQUISITIONS")
        for request in pending_requests:
            print(
                request.requisition_id,
                "|", request.staff_name,
                "| $" + format(request.total, ".2f")
            )

        return True

    def show_statistics(self):
        total = len(self.requisitions)
        approved = 0
        pending = 0
        not_approved = 0

        for request in self.requisitions:
            if request.status == APPROVED:
                approved += 1
            elif request.status == PENDING:
                pending += 1
            elif request.status == NOT_APPROVED:
                not_approved += 1

        print("\nREQUISITION STATISTICS")
        print("----------------------")
        print("Total submitted:", total)
        print("Approved:", approved)
        print("Pending:", pending)
        print("Not approved:", not_approved)

def submit_request(system):
    print("\nSUBMIT A REQUISITION")

    date = input("Date (DD/MM/YYYY): ")
    staff_id = input("Staff ID: ")
    staff_name = input("Staff name: ")

    items = []

    while True:
        print("\nEnter purchase item details")
        item_name = input("Item name: ")
        item_cost = input("Item cost ($): ")
        items.append((item_name, item_cost))

        another = input("Add another item? (yes/no): ").strip().lower()

        if another not in ("yes", "y"):
            break

    request = system.create_requisition(
        date, staff_id, staff_name, items
    )

    print("\nRequisition submitted successfully.")
    print("Requisition ID:", request.requisition_id)
    print("Total: $" + format(request.total, ".2f"))
    print("Status:", request.status)
    print("Approval reference:", request.approval_reference)


def manager_update(system):
    if not system.show_pending():
        return

    requisition_id = input("\nEnter requisition ID: ")
    decision = input("Decision (Approved/Not approved): ")
    manager_name = input("Manager name: ")

    request = system.manager_response(
        requisition_id, decision, manager_name
    )

    print("Updated status:", request.status)


def run_program():
    system = RequisitionSystem()

    while True:
        print("\nSTAFF PURCHASE REQUISITION SYSTEM")
        print("1. Submit a requisition")
        print("2. Manager response")
        print("3. Display all requisitions")
        print("4. Display statistics")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                submit_request(system)
            elif choice == "2":
                manager_update(system)
            elif choice == "3":
                system.show_all()
            elif choice == "4":
                system.show_statistics()
            elif choice == "5":
                print("Thank you. Goodbye.")
                break
            else:
                print("Invalid option. Please choose 1 to 5.")

        except ValueError as error:
            print("Error:", error)


if __name__ == "__main__":
    run_program()
