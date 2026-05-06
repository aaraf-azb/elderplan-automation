import csv
import os


# ============================================================
# CSV SAVER
# ============================================================

class CSVSaver:

    def __init__(self, output_file, input_file):

        self.output_file = output_file

        self.input_file = input_file

    # ============================================================
    # SAVE OUTPUT ROW
    # ============================================================

    def save_row(self, row):

        file_exists = os.path.exists(
            self.output_file
        )

        with open(
            self.output_file,
            "a",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.DictWriter(
                f,
                fieldnames=row.keys()
            )

            if not file_exists:

                writer.writeheader()

            writer.writerow(row)

        print("💾 Saved output row")

    # ============================================================
    # MARK INPUT ROW AS DONE
    # ============================================================

    def mark_row_done(self, invoice_number):

        with open(
            self.input_file,
            newline="",
            encoding="utf-8"
        ) as f:

            reader = csv.DictReader(f)

            rows = list(reader)

            fieldnames = reader.fieldnames

        for row in rows:

            if row["InvoiceNumber"] == invoice_number:

                row["Automation Status"] = "DONE"

        try:

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

                writer.writerows(rows)

        except PermissionError:

            raise Exception(
                "❌ Please close the input CSV file before running automation"
            )

        print(f"✅ Marked DONE: {invoice_number}")