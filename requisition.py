from decimal import Decimal
from constants import (
    APPROVAL_LIMIT,
    REFERENCE_NOT_ISSUED,
    STATUS_APPROVED,
    STATUS_NOT_APPROVED,
    STATUS_PENDING,
)
from validation import to_money, validate_date, validate_text


class Requisition:

    def __init__(self, date, staff_id, staff_name, requisition_id):
        self.date = validate_date(date)
        self.staff_id = validate_text(staff_id, "Staff ID")
        self.staff_name = validate_text(staff_name, "Staff name")
        self.requisition_id = int(requisition_id)
        self.items = []
        self.total = Decimal("0.00")
        self.status = STATUS_PENDING
        self.approval_reference = REFERENCE_NOT_ISSUED
        self.decision_by = "Awaiting manager"
        self._submitted = False

    def add_item(self, item_name, item_cost):
        if self._submitted:
            raise ValueError("Items cannot be changed after the requisition is submitted.")

        name = validate_text(item_name, "Item name")
        cost = to_money(item_cost)
        self.items.append({"name": name, "cost": cost})
        self.calculate_total()
        return self.total

    def add_items(self, items):
        if self._submitted:
            raise ValueError("Items cannot be changed after the requisition is submitted.")

        validated_items = []
        for item in items:
            try:
                item_name, item_cost = item
            except (TypeError, ValueError) as error:
                raise ValueError("Each item must contain a name and a cost.") from error
            name = validate_text(item_name, "Item name")
            cost = to_money(item_cost)
            validated_items.append({"name": name, "cost": cost})

        if not validated_items:
            raise ValueError("Add at least one item before submitting.")

        self.items.extend(validated_items)
        return self.calculate_total()

    def calculate_total(self):
        self.total = sum(
            (item["cost"] for item in self.items), Decimal("0.00")
        )
        return self.total

    def _make_approval_reference(self):
        final_three_digits = str(self.requisition_id)[-3:]
        return f"{self.staff_id}{final_three_digits}"

    def apply_automatic_approval(self):
        if not self.items:
            raise ValueError("A requisition must contain at least one item.")

        self.calculate_total()
        if self.total < Decimal(str(APPROVAL_LIMIT)):
            self.status = STATUS_APPROVED
            self.approval_reference = self._make_approval_reference()
            self.decision_by = "Automatic approval rule"
        else:
            self.status = STATUS_PENDING
            self.approval_reference = REFERENCE_NOT_ISSUED
            self.decision_by = "Awaiting manager"

        self._submitted = True
        return self.status

    def record_manager_decision(self, decision, manager_name):
        if self.status != STATUS_PENDING:
            raise ValueError("Only pending requisitions can receive a manager decision.")

        normalised_decision = str(decision).strip().lower()
        validated_manager = validate_text(manager_name, "Manager name")

        if normalised_decision in {"approve", "approved", "yes"}:
            new_status = STATUS_APPROVED
            new_reference = self._make_approval_reference()
        elif normalised_decision in {
            "reject", "rejected", "not approved", "no"
        }:
            new_status = STATUS_NOT_APPROVED
            new_reference = REFERENCE_NOT_ISSUED
        else:
            raise ValueError("Choose either Approved or Not approved.")

        self.status = new_status
        self.approval_reference = new_reference
        self.decision_by = validated_manager
        return self.status

    def to_record(self):
        item_summary = ", ".join(
            f"{item['name']} (${item['cost']:.2f})" for item in self.items
        )
        return {
            "date": self.date,
            "requisition_id": self.requisition_id,
            "staff_id": self.staff_id,
            "staff_name": self.staff_name,
            "items": item_summary,
            "total": self.total,
            "status": self.status,
            "approval_reference": self.approval_reference,
            "decision_by": self.decision_by,
        }
