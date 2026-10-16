# Cloud connectivity probe (stage 1)

This is a minimal GitHub Actions test, **not** the full author-tracking app.
It requests only one public artist-tag listing page and stops on HTTP 403/429.
It does not use account cookies, access Favorites, or store artwork.

## Setup

1. Create a **private** GitHub repository.
2. Upload `probe.py` and `.github/workflows/probe.yml` with their paths preserved.
3. In the repository, open **Actions → Cloud connectivity probe → Run workflow**.
4. Enter one numeric **artist tag ID** (not a gallery ID) from your existing script's exported JSON (`data.authors` keys).
5. Read the run log or download the `probe-result` artifact.

Expected success: `status: 200`, `valid_json: true`, `item_count` is a number.
A 403/429 or schema mismatch means we should not scale to 199 artists yet.

## Next step

If the probe succeeds, import the exported Tampermonkey backup and build a daily scheduled scanner with cautious rate limits, state persistence, and a private mobile feed.

Do not upload cookies, passwords, or session tokens.
