# ============================================================
# IMPORTS
# ============================================================

import csv


# ============================================================
# SETUP
# ============================================================

class Setup:

    def __init__(self, input_file):

        self.input_file = input_file

    # ============================================================
    # ENSURE REQUIRED COLUMNS
    # ============================================================

    def ensure_columns(self):

        with open(self.input_file, newline="", encoding="utf-8") as f:

            reader = csv.DictReader(f)

            data = list(reader)

            fieldnames = reader.fieldnames

        updated = False

        required_columns = [
            "Automation Status"
        ]

        for col in required_columns:

            if col not in fieldnames:

                fieldnames.append(col)

                updated = True

        if updated:

            with open(
                self.input_file,
                "w",
                newline="",
                encoding="utf-8"
            ) as f:

                writer = csv.DictWriter(
                    f,
                    fieldnames=fieldnames
                )

                writer.writeheader()

                writer.writerows(data)

    # ============================================================
    # LOAD DATA
    # ============================================================

    def load_data(self):

        self.ensure_columns()

        with open(
            self.input_file,
            newline="",
            encoding="utf-8"
        ) as f:

            reader = csv.DictReader(f)

            data = []

            for idx, row in enumerate(reader, start=2):

                status = row.get(
                    "Automation Status",
                    ""
                ).strip().upper()

                # Skip completed rows
                if status == "DONE":

                    continue

                row["Row No. From Main File"] = idx

                data.append(row)

        print(f"📂 Loaded {len(data)} pending rows")

        return data