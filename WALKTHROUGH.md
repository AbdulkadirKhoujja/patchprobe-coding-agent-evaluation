# 45-second demo walkthrough for a hiring manager

**Open `index.html` in Chrome, Edge, Firefox or Safari.** No installs, network connection, credentials, server or API account needed.

1. **0–10 sec**: Start at the headline: "The patch passed. The system was still wrong." Explain that all four public checks pass for a deliberately flawed *synthetic* implementation.
2. **10–25 sec**: Select **Cross-tenant collision**. Two unrelated tenants share an event ID; the candidate silently loses one event, while the corrected reference keeps both.
3. **25–33 sec**: Select **Newer event**, then **Invalid input**, to show stale data and fail-closed validation.
4. **33–42 sec**: Scroll to **Executed evidence**. Cite actual Python results: public 4/4; held-out 2/12 (8 fails, 2 errors); reference 16/16.
5. **42–45 sec**: Show `python evaluate.py` for reproducibility and point to `REVIEW.md` for the evidence-backed PR review.

Do not say a real AI agent generated the deliberately flawed code. In this demo the patch was seeded intentionally to demonstrate evaluation methodology. The JavaScript browser simulator is an explanatory layer; real scores were computed independently by Python unittest.

## Proposal attachment options

- **Best:** publish the `index.html` as a single-page website (GitHub Pages or Cloudflare Pages) after deciding what to disclose. Link to the live URL and a repository containing the raw Python implementation.
- **No hosting:** attach the ZIP and give a one-line instruction: "Unzip, open `index.html`, select Cross-tenant collision. For original test evidence run `python evaluate.py`."
- **Optional:** record the 45-second walkthrough using screen capture for fast viewing inside Upwork.
