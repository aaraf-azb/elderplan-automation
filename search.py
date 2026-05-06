# ============================================================
# IMPORTS
# ============================================================

from datetime import datetime


# ============================================================
# SEARCH PAGE
# ============================================================

class SearchPage:

    def __init__(self, page, log=None):

        self.page = page

        self.log = log if log else print

    # ============================================================
    # FORMAT MEMBER ID
    # ============================================================

    def format_member_id(self, member_id):

        return str(member_id).zfill(11)

    # ============================================================
    # FORMAT DATE
    # ============================================================

    def format_date(self, raw_date):

        for fmt in (
            "%Y-%m-%d",
            "%m/%d/%Y",
            "%d-%m-%Y",
            "%m/%d/%y"
        ):

            try:

                return datetime.strptime(
                    raw_date,
                    fmt
                ).strftime("%m/%d/%Y")

            except:

                continue

        raise ValueError(
            f"❌ Invalid date format: {raw_date}"
        )

    # ============================================================
    # SEARCH CLAIM
    # ============================================================

    def search(self, row):

        member_id = self.format_member_id(
            row["AltPatientID"]
        )

        visit_date = self.format_date(
            row["VisitDate"]
        )

        print(
            f"🔎 Searching: {member_id} | {visit_date}"
        )

        self.log(
            f"🔎 Searching: {member_id} | {visit_date}"
        )

        # ============================================================
        # OPEN MEMBER SEARCH
        # ============================================================

        self.page.get_by_text(
            "View Member Info"
        ).click()

        # ============================================================
        # MEMBER ID
        # ============================================================

        self.page.get_by_role(
            "textbox",
            name="ID Input"
        ).fill(member_id)

        # ============================================================
        # BEGIN DATE
        # ============================================================

        self.page.get_by_role(
            "textbox",
            name="Begin Date:"
        ).fill(visit_date)

        # ============================================================
        # END DATE
        # ============================================================

        self.page.get_by_role(
            "textbox",
            name="End Date:"
        ).fill(visit_date)

        # ============================================================
        # SEARCH BUTTON
        # ============================================================

        self.page.get_by_role(
            "button",
            name="Search"
        ).click()