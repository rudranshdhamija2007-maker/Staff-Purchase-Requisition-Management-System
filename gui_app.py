import tkinter as tk
from tkinter import messagebox, ttk

from requisition_system import RequisitionSystem


class RequisitionGUI:
    

    def __init__(self, root):
        self.root = root
        self.root.title("Staff Purchase Requisition Management System")
        self.root.geometry("1120x820")
        self.root.minsize(980, 720)

        self.system = RequisitionSystem()
        self.current_items = []

        self._create_variables()
        self._configure_style()
        self._build_layout()
        self._refresh_dashboard()

    def _create_variables(self):
        self.date_var = tk.StringVar()
        self.staff_id_var = tk.StringVar()
        self.staff_name_var = tk.StringVar()
        self.item_name_var = tk.StringVar()
        self.item_cost_var = tk.StringVar()
        self.requisition_id_var = tk.StringVar()
        self.manager_name_var = tk.StringVar(value="Manager")
        self.decision_var = tk.StringVar(value="Approved")
        self.message_var = tk.StringVar(value="Enter staff details and add items.")
        self.stat_vars = {
            "Total submitted": tk.StringVar(value="0"),
            "Approved": tk.StringVar(value="0"),
            "Pending": tk.StringVar(value="0"),
            "Not approved": tk.StringVar(value="0"),
        }

    def _configure_style(self):
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("Section.TLabelframe.Label", font=("Segoe UI", 10, "bold"))
        style.configure("StatValue.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("StatName.TLabel", font=("Segoe UI", 9))
        style.configure("Treeview", rowheight=27, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

    def _build_layout(self):
        outer = ttk.Frame(self.root, padding=16)
        outer.pack(fill="both", expand=True)
        outer.columnconfigure(0, weight=1)
        outer.columnconfigure(1, weight=1)
        outer.rowconfigure(3, weight=1)

        ttk.Label(
            outer,
            text="Staff Purchase Requisition Management System",
            style="Title.TLabel",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 4))
        ttk.Label(
            outer,
            text="Submit requests, review manager decisions and monitor requisition totals.",
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 14))

        self._build_submission_panel(outer)
        self._build_manager_panel(outer)
        self._build_statistics_panel(outer)
        self._build_records_panel(outer)
        ttk.Label(
            outer, textvariable=self.message_var, anchor="w", wraplength=1050
        ).grid(row=5, column=0, columnspan=2, sticky="ew", pady=(10, 0))

    def _build_submission_panel(self, parent):
        """Create the staff and item entry panel."""
        panel = ttk.LabelFrame(
            parent, text="  1. Staff and requisition details  ",
            style="Section.TLabelframe", padding=12,
        )
        panel.grid(row=2, column=0, sticky="nsew", padx=(0, 8), pady=(0, 10))
        panel.columnconfigure(1, weight=1)
        panel.columnconfigure(3, weight=1)

        self._add_field(panel, "Date (DD/MM/YYYY)", self.date_var, 0, 0)
        self._add_field(panel, "Staff ID", self.staff_id_var, 0, 2)
        self._add_field(panel, "Staff name", self.staff_name_var, 1, 0, span=3)
        ttk.Separator(panel).grid(row=2, column=0, columnspan=4, sticky="ew", pady=10)
        self._add_field(panel, "Item name", self.item_name_var, 3, 0)
        self._add_field(panel, "Item cost ($)", self.item_cost_var, 3, 2)

        ttk.Button(panel, text="Add item", command=self._add_item).grid(
            row=4, column=0, sticky="ew", padx=4, pady=8
        )
        ttk.Button(panel, text="Remove selected", command=self._remove_item).grid(
            row=4, column=1, sticky="ew", padx=4, pady=8
        )

        self.item_list = tk.Listbox(panel, height=5, activestyle="none")
        self.item_list.grid(row=5, column=0, columnspan=4, sticky="ew", padx=4, pady=4)
        ttk.Button(panel, text="Submit requisition", command=self._submit_requisition).grid(
            row=6, column=0, columnspan=2, sticky="ew", padx=4, pady=(8, 2)
        )
        ttk.Button(panel, text="Clear form", command=self._clear_form).grid(
            row=6, column=2, columnspan=2, sticky="ew", padx=4, pady=(8, 2)
        )

    def _build_manager_panel(self, parent):
        panel = ttk.LabelFrame(
            parent, text="  2. Manager response  ",
            style="Section.TLabelframe", padding=12,
        )
        panel.grid(row=2, column=1, sticky="nsew", padx=(8, 0), pady=(0, 10))
        panel.columnconfigure(1, weight=1)

        self._add_field(panel, "Requisition ID", self.requisition_id_var, 0, 0, span=2)
        self._add_field(panel, "Manager name", self.manager_name_var, 1, 0, span=2)
        ttk.Label(panel, text="Decision").grid(
            row=2, column=0, sticky="w", padx=4, pady=7
        )
        ttk.Combobox(
            panel, textvariable=self.decision_var,
            values=["Approved", "Not approved"], state="readonly",
        ).grid(row=2, column=1, sticky="ew", padx=4, pady=7)
        ttk.Button(
            panel, text="Save manager decision", command=self._save_manager_decision
        ).grid(row=3, column=0, columnspan=2, sticky="ew", padx=4, pady=8)
        ttk.Label(
            panel,
            text="Only requests with Pending status can be updated by a manager.",
            wraplength=430,
        ).grid(row=4, column=0, columnspan=2, sticky="w", padx=4, pady=(8, 0))
        ttk.Label(
            panel,
            text="Approval rule: totals below $500 are approved automatically.",
            wraplength=430,
        ).grid(row=5, column=0, columnspan=2, sticky="w", padx=4, pady=5)

    def _build_statistics_panel(self, parent):
        panel = ttk.LabelFrame(
            parent, text="  3. Requisition statistics  ",
            style="Section.TLabelframe", padding=10,
        )
        panel.grid(row=3, column=0, columnspan=2, sticky="new", pady=(0, 10))
        for column in range(4):
            panel.columnconfigure(column, weight=1, uniform="stats")

        for column, (label, variable) in enumerate(self.stat_vars.items()):
            card = ttk.Frame(panel, padding=8, relief="groove")
            card.grid(row=0, column=column, sticky="ew", padx=5, pady=3)
            ttk.Label(card, textvariable=variable, style="StatValue.TLabel").pack()
            ttk.Label(card, text=label, style="StatName.TLabel").pack()

    def _build_records_panel(self, parent):
        panel = ttk.LabelFrame(
            parent, text="  4. Requisition records  ",
            style="Section.TLabelframe", padding=10,
        )
        panel.grid(row=4, column=0, columnspan=2, sticky="nsew")
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(0, weight=1)

        columns = (
            "requisition_id", "date", "staff_id", "staff_name",
            "total", "status", "reference",
        )
        self.records_table = ttk.Treeview(
            panel, columns=columns, show="headings", height=8
        )
        headings = {
            "requisition_id": "Requisition ID",
            "date": "Date",
            "staff_id": "Staff ID",
            "staff_name": "Staff name",
            "total": "Total ($)",
            "status": "Status",
            "reference": "Approval reference",
        }
        widths = {
            "requisition_id": 110, "date": 95, "staff_id": 90,
            "staff_name": 150, "total": 90, "status": 115,
            "reference": 150,
        }
        for column in columns:
            self.records_table.heading(column, text=headings[column])
            self.records_table.column(
                column, width=widths[column], anchor="center"
            )

        self.records_table.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(
            panel, orient="vertical", command=self.records_table.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.records_table.configure(yscrollcommand=scrollbar.set)

    @staticmethod
    def _add_field(parent, label, variable, row, column, span=1):
        """Place a consistently spaced label and entry field."""
        ttk.Label(parent, text=label).grid(
            row=row, column=column, sticky="w", padx=4, pady=6
        )
        ttk.Entry(parent, textvariable=variable).grid(
            row=row, column=column + 1, columnspan=span,
            sticky="ew", padx=4, pady=6,
        )

    def _add_item(self):
        """Validate and add an item to the current form."""
        try:
            from validation import to_money, validate_text
            name = validate_text(self.item_name_var.get(), "Item name")
            cost = to_money(self.item_cost_var.get())
        except ValueError as error:
            messagebox.showwarning("Check item details", str(error))
            return

        self.current_items.append((name, cost))
        self.item_list.insert(tk.END, f"{name:<30} ${cost:>8.2f}")
        self.item_name_var.set("")
        self.item_cost_var.set("")
        self.message_var.set(f"Added item: {name}")

    def _remove_item(self):
        selection = self.item_list.curselection()
        if not selection:
            self.message_var.set("Select an item before removing it.")
            return
        index = selection[0]
        self.item_list.delete(index)
        self.current_items.pop(index)
        self.message_var.set("Selected item removed.")

    def _submit_requisition(self):
        try:
            request = self.system.create_requisition(
                self.date_var.get(), self.staff_id_var.get(),
                self.staff_name_var.get(), self.current_items,
            )
        except ValueError as error:
            messagebox.showerror("Cannot submit requisition", str(error))
            return

        self.message_var.set(
            f"Requisition {request.requisition_id} submitted: "
            f"{request.status} | Total ${request.total:.2f}"
        )
        self._clear_form(keep_message=True)
        self._refresh_dashboard()

    def _save_manager_decision(self):
        """Save the selected manager decision."""
        try:
            request = self.system.respond_to_requisition(
                self.requisition_id_var.get(), self.decision_var.get(),
                self.manager_name_var.get(),
            )
        except ValueError as error:
            messagebox.showerror("Manager response", str(error))
            return

        self.message_var.set(
            f"Requisition {request.requisition_id} updated to {request.status}."
        )
        self._refresh_dashboard()

    def _clear_form(self, keep_message=False):
        for variable in (
            self.date_var, self.staff_id_var, self.staff_name_var,
            self.item_name_var, self.item_cost_var,
        ):
            variable.set("")
        self.current_items.clear()
        self.item_list.delete(0, tk.END)
        if not keep_message:
            self.message_var.set("Form cleared. You can start another requisition.")

    def _refresh_dashboard(self):
        for row in self.records_table.get_children():
            self.records_table.delete(row)

        for record in self.system.get_requisition_records():
            self.records_table.insert(
                "", tk.END,
                values=(
                    record["requisition_id"], record["date"],
                    record["staff_id"], record["staff_name"],
                    f"{record['total']:.2f}", record["status"],
                    record["approval_reference"],
                ),
            )

        for label, value in self.system.get_statistics().items():
            self.stat_vars[label].set(str(value))


def run_gui_app():
    root = tk.Tk()
    RequisitionGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui_app()
