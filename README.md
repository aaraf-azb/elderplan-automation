# Elderplan Claim Automation

## Overview

Elderplan Claim Automation is a Python + Playwright based healthcare automation framework designed to automate claim lookup and extraction from the Elderplan portal.

The automation supports:
- Automated claim searching.
- Claim detail extraction.
- CSV output generation.
- GUI-based execution.
- Auto resume capability.
- Retry logic with jitter.
- Real-time logging and progress tracking.

The project is designed to improve operational efficiency, reduce repetitive manual work, and provide resilient healthcare portal automation.

---

# Core Features

## Claim Automation
- Automated claim lookup using Member ID and DOS.
- Multi-claim extraction support.
- Denial reason extraction.
- Aggregated claim result handling.

---

## GUI Application
- CSV file selection.
- Output folder selection.
- Entry size control.
- Live logging window.
- Progress tracking.
- Stop button support.

---

## Auto Resume Capability
The automation supports resumable execution.

Features:
- Automatically creates the `Automation Status` column.
- Marks completed rows as `DONE`.
- Skips completed rows during rerun.
- Continues processing remaining rows automatically.

---

## Retry Logic with Jitter
The automation includes retry protection for unstable portal behavior.

Features:
- Automatic retry attempts.
- Randomized retry delay (jitter).
- Graceful fallback handling.

This improves resilience against:
- Temporary portal failures.
- Delayed page loads.
- Intermittent timeouts.

---

## Browser Automation
- Automatic Microsoft Edge launch
- Automatic portal tab detection
- CDP-based browser connection
- Manual login workflow support

---

# Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Browser Automation | Playwright |
| GUI Framework | Tkinter |
| Browser | Microsoft Edge |
| Data Handling | CSV |

---


# Portal Navigation

Before starting automation:

1. Login to the Elderplan portal.
2. Open the "View Member Info" page.
3. Keep the tab open.
4. Start automation from the GUI.

---

# Expected Workflow

1. Launch the application.
2. Select input CSV file.
3. Select output folder.
4. Click **Start** to begin automation.
5. Automation checks if Microsoft Edge with CDP connection is already open and the portal is logged in with the claims search interface active,
   - If yes, automation connects to the existing browser session.
   - If no, Microsoft Edge launches automatically and the user logs in to the Elderplan portal.
6. Navigate to the claims search interface/tab if not already open.
7. Click **Start** again from the GUI to resume automation.
8. Automation detects the portal automatically.
9. Claim processing begins.
10. Monitor live progress and logs from the GUI.
11. Automation completes processing.
12. Output CSV is generated.

---

# Workflow Diagram

```text
+-------------------+
| Launch GUI        |
+-------------------+
          |
          v
+-------------------+
| Select CSV/Input  |
+-------------------+
          |
          v
+-------------------+
| Start Automation  |
+-------------------+
          |
          v
+------------------------------------------------------+ 
| Is Edge Browser with CDP Connected & Portal Logged In|
| with Claims Search Interface Active?                  |  <-- Decision node
+------------------------------------------------------+ 
         |                              |
         | Yes                          | No
         v                              v
+-------------------+            +-------------------+
| Portal Detection  |            | Launch Edge       |
+-------------------+            +-------------------+
         |                              |
         v                              v
+-------------------+            +-------------------+
| Claim Processing  |            | Login to Portal   |
+-------------------+            +-------------------+
         |                              |
         v                              v
+-------------------+            +-------------------+
| Save CSV Output   |            | Portal Detection  |
+-------------------+            +-------------------+
         |                              |
         |                              v
         |                       +-------------------+
         |                       | Claim Processing  |
         |                       +-------------------+
         |                              |
         v                              v
+-------------------+            +-------------------+
| Automation Done   |            | Save CSV Output   |
+-------------------+            +-------------------+
                                    |
                                    v
                           +-------------------+
                           | Automation Done   |
                           +-------------------+
```

---

# Project Structure

```text

enderplan-automation/
│
├── gui.py
├── main.py
├── search.py
├── result.py
├── setup.py
├── save_csv.py
├── README.md

```
---

## Image

![GUI](images/gui.png)

![Login](images/login.png)

![First Page](images/first_page.png)

![Start Automation](images/start_automation.png)

![Output](images/output.png)

---

## Output

The output CSV will contain enriched rows with these extracted columns for each claim:

- Automation Status
- Main CSV Row No.
- Claim ID/TRN
- Check Number
- Status (Complete/In Process)
- Billed Amount
- Paid Amount
- Denial Reason (Decline reason if any)

---

## Notes

- Ensure the input CSV is closed in other applications during automation.
- Login to the portal manually first and keep the claims search interface tab active.
- The automation connects to the browser tab for query execution.
- Supports resumable execution by skipping already done rows.

---