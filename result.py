# --- Helper ---

def safe_text(locator):
    try:
        return locator.inner_text().strip()
    except:
        return "N/A"


def format_list(items):
    return "\n".join([f"{i+1}. {item}" for i, item in enumerate(items)])


class ResultPage:
    def __init__(self, page, log=None):
        self.page = page
        self.log = log if log else print

        self.table = "#ctl00_MainContent_uxClaimControl_uxListGrid"
        self.rows = "tbody tr.pagegrid_row, tbody tr.pagegrid_altrow"
        self.back_btn = "#ctl00_MainContent_uxClaimControl_uxBackToSearchLink"

    def empty_result(self):
        return {
            "Claim ID/TRN": "N/A",
            "Check Number": "N/A",
            "Status": "N/A",
            "Billed Amount": "N/A",
            "Paid Amount": "N/A",
            "Denial Reason": "N/A",
        }

    def process_results(self, member_id):
        page = self.page

        table = page.locator(self.table)
        table.wait_for(timeout=30000)

        rows = table.locator(self.rows)
        count = rows.count()

        print(f"📊 Found {count} claims")

        if count == 0:
            return self.empty_result()

        # --- Sorting Logic ---

        if count > 1:
            header = page.get_by_role("columnheader", name="Claim Number")
            header.wait_for(timeout=5000)
            print("🔄 Activating sort...")
            header.click()  # first click (activates sorting)

            # wait for icon to appear
            icon = header.locator("img")
            icon.wait_for(timeout=5000)
            src = icon.get_attribute("src")
            print("🔍 Sort icon after first click:", src)

            # If NOT ascending → click again
            if src and "arrow_down" in src:
                print("🔄 Switching to ascending order...")
                header.click()

        # --- lists for aggregation ---

        claim_ids = []
        check_list = []
        status_list = []
        billed_list = []
        paid_list = []
        reason_list = []

        for i in range(count):

            rows = table.locator(self.rows)
            row = rows.nth(i)

            claim_link = row.locator("td:nth-child(4) a")
            claim_link.wait_for(timeout=5000)

            claim_number = safe_text(claim_link)
            print(f"➡️ Opening row {i+1} | Claim: {claim_number}")

            claim_link.click()
            page.wait_for_timeout(1500)

            try:
                print("🔍 Extracting details...")
                self.log(f"🔍 Extracting details for Claim: {claim_number}...")

                claim_id = safe_text(
                    page.locator("td.label:has-text('Claim No:') + td")
                )

                check_no = safe_text(
                    page.locator("td.label:has-text('Check Number:') + td a")
                )

                status = safe_text(
                    page.locator("td.label:has-text('Claim Status:') + td")
                )
                print(
                    f"✅ Extracted: Claim ID: {claim_id} | Check No: {check_no} | Status: {status}"
                )
                # self.log(f"✅ Extracted: Claim ID: {claim_id} | Check No: {check_no} | Status: {status}")

                subtotal_row = page.locator("tr:has-text('Claim Sub Totals')")
                tds = subtotal_row.locator("td")
                td_count = tds.count()

                billed = safe_text(tds.nth(2))
                paid = safe_text(tds.nth(td_count - 2))

                print(f"✅ Extracted: Billed: {billed} | Paid: {paid}")

                tables = page.locator("table:has(th:has-text('Code Description'))")
                print("🔍 Tables found:", tables.count())

                reason = []
                reason_table = tables.last

                reason_table.wait_for(timeout=5000)

                tds = reason_table.locator("td")

                for i in range(tds.count()):

                    text = tds.nth(i).inner_text().strip()

                    if text:
                        reason.append(text)
                reason = "\n".join(reason)

                print("✅ Final Reason:", reason)

            except Exception as e:
                print(f"❌ Error: {e}")
                claim_id = check_no = status = billed = paid = reason = "N/A"

            self.log(
                f"✅ Extracted:\n"
                f"Claim ID: {claim_id}\n"
                f"Check No: {check_no}\n"
                f"Status: {status}\n"
                f"Billed: {billed}\n"
                f"Paid: {paid}\n"
                f"Reason: {reason}\n"
            )

            # --- store ---
            claim_ids.append(claim_id)
            check_list.append(check_no)
            status_list.append(status)
            billed_list.append(billed)
            paid_list.append(paid)
            reason_list.append(reason)

            # --- back ---
            back_btn = page.locator(self.back_btn)
            back_btn.wait_for(timeout=5000)
            back_btn.click()

        # --- aggregated output ---
        return {
            "Claim ID/TRN": format_list(claim_ids),
            "Check Number": format_list(check_list),
            "Status": format_list(status_list),
            "Billed Amount": format_list(billed_list),
            "Paid Amount": format_list(paid_list),
            "Denial Reason": format_list(reason_list),
        }
