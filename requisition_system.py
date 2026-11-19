from constants import (
    FIRST_REQUISITION_ID,
    STATUS_APPROVED,
    STATUS_NOT_APPROVED,
    STATUS_PENDING,
)
from requisition import Requisition


class RequisitionSystem:

    def __init__(self):
        self.requisitions = []
        self._next_requisition_id = FIRST_REQUISITION_ID

    def create_requisition(self, date, staff_id, staff_name, items):
        requisition = Requisition(
            date, staff_id, staff_name, self._next_requisition_id
        )
        requisition.add_items(items)
        requisition.apply_automatic_approval()

        self.requisitions.append(requisition)
        self._next_requisition_id += 1
        return requisition

    def find_requisition(self, requisition_id):
        try:
            target_id = int(requisition_id)
        except (TypeError, ValueError) as error:
            raise ValueError("Enter a valid requisition ID.") from error

        for requisition in self.requisitions:
            if requisition.requisition_id == target_id:
                return requisition

        raise ValueError(f"Requisition {target_id} was not found.")

    def respond_to_requisition(self, requisition_id, decision, manager_name):
        requisition = self.find_requisition(requisition_id)
        requisition.record_manager_decision(decision, manager_name)
        return requisition

    def get_pending_requisitions(self):
        return [
            requisition
            for requisition in self.requisitions
            if requisition.status == STATUS_PENDING
        ]

    def get_requisition_records(self):
    
        return [requisition.to_record() for requisition in self.requisitions]

    def get_statistics(self):
        statuses = [requisition.status for requisition in self.requisitions]
        return {
            "Total submitted": len(statuses),
            "Approved": statuses.count(STATUS_APPROVED),
            "Pending": statuses.count(STATUS_PENDING),
            "Not approved": statuses.count(STATUS_NOT_APPROVED),
        }
