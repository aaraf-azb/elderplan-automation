from playwright.sync_api import sync_playwright
from setup import Setup
from search import SearchPage
from result import ResultPage
from save_csv import CSVSaver
import os
import subprocess
import time
import requests
import random


from datetime import datetime

EMPTY_RESULT = {
    "Claim ID/TRN": "N/A",
    "Check Number": "N/A",
    "Status": "N/A",
    "Billed Amount": "N/A",
    "Paid Amount": "N/A",
    "Denial Reason": "N/A",
}


# ============================================================
# ENSURE EDGE CDP
# ============================================================


def ensure_edge_cdp(log=None):

    try:
        response = requests.get("http://127.0.0.1:9222/json/version", timeout=2)

        if response.status_code == 200:
            if log:
                log("✅ Existing Edge browser detected")
            return

    except:
        pass

    if log:
        log("🚀 Launching Edge browser...")

    edge_cmd = [
        "cmd",
        "/c",
        "start",
        "msedge",
        "--remote-debugging-port=9222",
        "--user-data-dir=C:\\edge-debug",
    ]

    subprocess.Popen(edge_cmd)

    time.sleep(5)


def run(
    input_file,
    output_folder=None,
    entry_size=None,
    stop_flag=None,
    progress_callback=None,
    log_callback=None,
):
    setup = Setup(input_file)
    data = setup.load_data()
    if entry_size is not None:
        data = data[:entry_size]

    # ============================================================
    # OUTPUT FILE SETUP
    # ============================================================

    base_name = os.path.splitext(os.path.basename(input_file))[0]
    if output_folder:
        output_file = os.path.join(
            output_folder,
            f"{base_name}_Automation_output_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv",
        )
    else:
        output_file = f"{base_name}_Automation_output_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

    saver = CSVSaver(output_file, input_file)

    invoice_cache = {}

    with sync_playwright() as p:

        # logging instead of print
        def log(msg):
            if log_callback:
                log_callback(msg)
            else:
                print(msg)

        ensure_edge_cdp(log)
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]

        log("\n🔍 Available tabs:")
        for i, pg in enumerate(context.pages):
            log(f"{i} {pg.url}")

        # ============================================================
        # ATTACH TO PORTAL TAB
        # ============================================================

        page = None
        for pg in context.pages:
            if "epportal.mjhs.org" in pg.url:
                log(f"🌐 Current Tab: {pg.url}")
                page = pg
                break

        while not page:
            log("⌛ Waiting for portal login...")

            time.sleep(15)
            context = browser.contexts[0]
            for pg in context.pages:
                if "epportal.mjhs.org" in pg.url:
                    log(f"🌐 Current Tab: {pg.url}")
                    page = pg
                    break

        page.wait_for_load_state("domcontentloaded")
        log(f"✅ Attached to: {page.url}")

        search_page = SearchPage(page, log)
        result_page = ResultPage(page, log)

        total = len(data)

        # enumerate for progress + stop support
        for i, row in enumerate(data, start=1):

            log(f"📄 Processing CSV Row: " f"{row['Main CSV Row No.']}")
            log("\n----------------------------")

            # STOP BUTTON
            if stop_flag and stop_flag.get("stop"):
                log("⛔ Stopped by user")
                break

            # PROGRESS UPDATE
            if progress_callback:
                progress_callback(i, total)

            member_id = row["AltPatientID"]
            raw_dos = row["VisitDate"]
            invoice_no = row["InvoiceNumber"]

            # ============================================================
            # CACHE CHECK
            # ============================================================

            if invoice_no in invoice_cache:
                log(f"⚡ Skipping invoice {invoice_no} (cached)")
                row["Automation Status"] = "DONE"
                saver.save_row({**row, **invoice_cache[invoice_no]})
                continue

            # ============================================================
            # SEARCH CLAIM WITH RETRY + JITTER
            # ============================================================

            max_retries = 2

            for attempt in range(1, max_retries + 1):

                try:

                    log(f"🔄 Attempt " f"{attempt}/{max_retries}")

                    search_page.search(row)

                    page.wait_for_timeout(3000)

                    table = page.locator("#ctl00_MainContent_uxClaimControl_uxListGrid")

                    if table.is_visible(timeout=10000):

                        log("✅ Table loaded with results")

                        result = result_page.process_results(member_id)

                        break

                    else:

                        raise Exception("Search result table not visible")

                except Exception as e:

                    log(f"⚠ Retry {attempt} failed: {e}")

                    if attempt == max_retries:

                        log("❌ Max retries reached")

                        result = EMPTY_RESULT

                    else:

                        jitter = random.uniform(2, 5)

                        log(f"⏳ Retrying in " f"{jitter:.1f} seconds...")

                        time.sleep(jitter)

            # ============================================================
            # SAVE OUTPUT
            # ============================================================

            invoice_cache[invoice_no] = result
            row["Automation Status"] = "DONE"
            saver.save_row({**row, **result})
            saver.mark_row_done(invoice_no)

    log("========================✅ Completed========================")
    return output_file


if __name__ == "__main__":
    input_file = (
        input("Enter full path of CSV file: ").strip().replace('"', "").replace("'", "")
    )
    run(input_file)
