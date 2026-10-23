# Mission 024 — Evidence Engine reliability test plan

Status: **Test plan published; tests not yet executed or passed.** Owner: Kai Laboratory. Version under test: Evidence Engine 0.4.

## Why this exists
An iPhone test established that one synthetic example rendered and produced uncertainty warnings. That does **not** establish multi-record reliability or correct CSV export. These cases are acceptance criteria, not claims of successful testing.

## Test dataset (fictional)
Create three comparables:
- **A, complete fields:** Seller "Example Alpha"; product "Engraved maple bookmark"; URL https://example.org/alpha; price 12.50; checked date today; VAT included; shipping "£2.99"; material "3 mm maple, 140 x 35 mm"; evidence "Fictional QA record"; review manually checked. Expected: **Fields complete** (still not genuinely verified; the checked selector is a user assertion).
- **B, uncertain:** Seller "Example Beta"; product "Birch bookmark"; URL https://example.org/beta; price 5.00; date today; VAT unknown; shipping "Not stated"; material "3 mm birch"; evidence "Fictional QA record"; review unchecked. Expected: **Uncertain**, with VAT, shipping and review warnings.
- **C, invalid:** Seller "Example Gamma"; product "Invalid listing"; URL "not a url"; price "five"; date blank; VAT unknown; shipping blank; material blank; evidence blank; review unchecked. Expected: **Invalid** and specific input errors.

Expected overall counts: **3 comparables · 1 fields complete with source review recorded · 1 uncertain · 1 invalid**.

## Manual browser acceptance checklist
1. On an iPhone and desktop browser, add all three records. No sideways overflow on the phone; result cards remain readable.
2. Edit B price from 5.00 to 5.50. Only B changes; no other record loses values.
3. Remove C. Counts become 2 total, 1 complete, 1 uncertain, 0 invalid. Remaining entries retain their data.
4. Export CSV. Confirm it opens in a spreadsheet application, contains the expected header and two data rows, and preserves source URL, VAT basis, review flag and warning text.
5. Put a comma, double quote and newline in one verification note; export again. Confirm the note survives CSV quoting and doesn't split into unintended records.
6. Add C back, export and verify errors are included.
7. Use **Clear all** and cancel: no data should be lost. Then confirm: zero records.
8. Load synthetic example. It should show **Uncertain**, never source-verified.
9. Reload the page: records should disappear as advertised (local tab-only storage).

## Known limits and issues to investigate
- The tool does not open or fetch product URLs; the manual review selector is self-reported, not proof.
- A syntactically valid URL is not evidence of a real seller or live product page.
- VAT and shipping warnings currently use exact simple text values; other phrases for unknown charges may evade warnings.
- A date entered in the future should fail; test date handling around midnight and time zones.
- Export on iOS in-app browsers may behave differently from Safari; verify actual file availability.
- No persistence, import or automated source verification. Avoid claiming production readiness.

## Exit criteria
Mark this mission tested only after recording device/browser, date, actual outcomes and any defects. Do not treat this document as evidence that the tests passed. Do not publish customer data or personal details in QA records.
