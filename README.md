# Staff Purchase Requisition Management System

A Python application for submitting and managing staff purchase requisitions. It provides a graphical interface (Tkinter), a console interface, and a small demonstration mode.

## Features

- Submit a requisition with a date, staff ID, staff name, and one or more items.
- Calculate the total cost of each requisition.
- Automatically approve requisitions with a total **below $500.00**.
- Send requisitions with a total of **$500.00 or more** to the manager decision process.
- Allow a manager to approve or reject pending requisitions.
- Generate an approval reference for approved requisitions.
- View requisition records and summary statistics.
- Validate dates, required text fields, and item prices.

## Project structure

```text
staff-purchase-requisition-system/
├── constants.py
├── console_app.py
├── gui_app.py
├── main.py
├── requisition.py
├── requisition_system.py
├── validation.py
└── README.md
```

### Module overview

| File | Responsibility |
|---|---|
| `main.py` | Creates sample requisitions and runs the demonstration. |
| `gui_app.py` | Provides the Tkinter graphical user interface. |
| `console_app.py` | Provides the menu-driven console interface. |
| `requisition.py` | Defines a requisition, its items, total, status, and approval decision. |
| `requisition_system.py` | Manages requisitions, IDs, manager responses, records, and statistics. |
| `validation.py` | Validates dates, text fields, and monetary values. |
| `constants.py` | Stores shared settings such as the approval limit and status labels. |

## Requirements

- Python 3.9 or later is recommended.
- Tkinter is required for the graphical interface. It is included with many standard Python installations. On some Linux distributions, it may need to be installed separately.
- No third-party Python packages are required by the supplied source files.

Check your Python version:

```bash
python --version
```

On some systems, use `python3` instead of `python`.

## How to run

Download or clone this repository, then open a terminal in the project folder.

### 1. Graphical application

```bash
python gui_app.py
```

This opens the Staff Purchase Requisition Management System window.

### 2. Console application

```bash
python console_app.py
```

Follow the numbered menu to submit requisitions, enter manager decisions, display records, or view statistics.

### 3. Demonstration

```bash
python main.py
```

This runs a demonstration using sample requisitions and prints their statuses and summary statistics. It does not open the graphical interface.

If `python` is not recognised, try replacing it with `python3`.

## Approval rules

The application uses an approval limit of **$500.00**:

| Requisition total | Initial status | Next step |
|---|---|---|
| Below $500.00 | Approved | An approval reference is generated automatically. |
| $500.00 or above | Pending | A manager must approve or reject the requisition. |

A manager can only make a decision on a requisition that is currently pending. Approved requisitions receive an approval reference; rejected requisitions do not.

## Input validation

- Dates must use the `DD/MM/YYYY` format.
- Staff ID, staff name, manager name, and item name cannot be blank.
- A requisition must contain at least one item.
- Item costs must be valid, non-negative monetary amounts.
- Items cannot be changed after a requisition has been submitted.

## Testing

You can check the main application behaviour by running the demonstration:

```bash
python main.py
```

For additional manual checks, try the following cases through the GUI or console application:

1. Submit a requisition with a total below $500.00 and confirm that it is automatically approved.
2. Submit a requisition with a total of exactly $500.00 and confirm that it becomes pending.
3. Submit a requisition above $500.00 and confirm that it becomes pending.
4. Approve a pending requisition and check that an approval reference is generated.
5. Reject a pending requisition and check that its status becomes `Not approved`.
6. Try an invalid date, blank required field, negative cost, or invalid cost and check that validation prevents the invalid submission.

Record the actual results of your tests before reporting them in an assessment.

## Design and implementation

The project separates the user interfaces from the requisition rules and data handling:

- `gui_app.py` and `console_app.py` handle user interaction.
- `requisition.py` represents an individual requisition and applies its approval rules.
- `requisition_system.py` manages the collection of requisitions.
- `validation.py` centralises input checks.
- `constants.py` keeps shared values in one place.

This modular structure makes the application easier to read, maintain, and extend.

## Current limitations

- Requisition records are held in memory while the application is running. The supplied code does not save records to a database or file.
- Closing the application clears the in-memory requisition records.
- The application is a local demonstration and does not include user accounts, authentication, or a network-based manager workflow.

## Future improvements

Possible future enhancements include persistent storage, automated unit tests, user authentication, role-based access, and exporting requisition reports.

## Author

Add your name and student details here if required by your course submission guidelines.

## Academic integrity

Make sure you understand the code, run the application yourself, and update this README to reflect any changes you make to the project. Follow your institution's requirements for acknowledging sources and collaboration.
