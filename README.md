# Elderplan Claim Automation

## Overview

Elderplan Claim Automation is a Python + Playwright based healthcare automation framework designed to automate claim lookup and extraction from the Elderplan portal.

The automation supports:
- Automated claim searching
- Claim detail extraction
- CSV output generation
- GUI-based execution
- Auto resume capability
- Retry logic with jitter
- Real-time logging and progress tracking

The project is designed to improve operational efficiency, reduce repetitive manual work, and provide resilient healthcare portal automation.

---

# Core Features

## Claim Automation
- Automated claim lookup using Member ID and DOS
- Multi-claim extraction support
- Denial reason extraction
- Aggregated claim result handling

---

## GUI Application
- CSV file selection
- Output folder selection
- Entry size control
- Live logging window
- Progress tracking
- Stop button support

---

## Auto Resume Capability
The automation supports resumable execution.

Features:
- Automatically creates `Automation Status` column
- Marks completed rows as `DONE`
- Skips completed rows during rerun
- Continues processing remaining rows automatically

---

## Retry Logic with Jitter
The automation includes retry protection for unstable portal behavior.

Features:
- Automatic retry attempts
- Randomized retry delay (jitter)
- Graceful fallback handling

This improves resilience against:
- Temporary portal failures
- Delayed page loads
- Intermittent timeouts

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

# Project Structure

```text
project/
│
├── gui.py
├── main.py
├── search.py
├── result.py
├── setup.py
├── save_csv.py
├── README.md