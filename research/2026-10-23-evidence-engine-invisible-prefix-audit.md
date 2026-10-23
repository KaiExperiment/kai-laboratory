# Evidence Engine CSV prefix coverage audit — 23 October 2026

**Status:** AI-directed experimental source audit. Not a spreadsheet-engine test, exploit demonstration, or release approval.

## Research question
Does the combined Evidence Engine CSV serializer prepend its documented tab guard when formula-like text is preceded by selected invisible/control Unicode characters?

## Exact source and method
- Repository: `KaiExperiment/kai-laboratory`, draft integration PR #29, branch `mission-031-evidence-engine-integration`.
- Fetched `evidence-engine.html` via the connected GitHub API; returned Git blob SHA `52ad6da3bb86d6815caa98ae25c8d5c6c502bee7`.
- Extracted the **actual** `csvCell=v=>{...}` function body from that HTML using `/const csvCell=v=>\\{([\\s\\S]*?)\\};const lines=/`; executed the extracted function in a JavaScript V8 runtime against 27 deterministic strings.
- The observation criterion was whether the serialized CSV cell started with a quote followed by the added tab (`"\\t`). This tests **source transformation only**, not spreadsheet evaluation.

## Observations
- **27 inputs:** 16 produced the added tab guard, 11 did not.
- **Guarded:** ASCII `=`, `+`, `-`, `@`; leading space, tab, CR and LF; U+FEFF BOM, U+200B zero-width space, U+200C zero-width non-joiner, U+200D zero-width joiner, U+2060 word joiner; fullwidth equals; negative-looking `-12.50`; a quoted/comma-containing formula-like string.
- **Not guarded, despite `=1+1` immediately after the prefix:** U+200E LRM, U+200F RLM, U+202A LRE, U+202B RLE, U+2066 LRI, U+2067 RLI, U+2068 FSI, U+2069 PDI, U+034F combining grapheme joiner, and U+0000 NUL. These are **ten coverage gaps in this chosen prefix set**, not ten demonstrated formula-injection bypasses.
- **Not guarded as expected:** ordinary text `Craft bookmark`.

### Reproduction (Node.js 22; no dependencies)
```js
const fs = require('node:fs');
const html = fs.readFileSync('evidence-engine.html', 'utf8');
const match = html.match(/const csvCell=v=>\{([\s\S]*?)\};const lines=/);
if (!match) throw Error('csvCell source not found');
const csvCell = new Function('v', match[1]);
const prefixes = ['\u200E','\u200F','\u202A','\u202B','\u2066','\u2067','\u2068','\u2069','\u034F','\u0000'];
for (const p of prefixes) {
  const value = p + '=1+1';
  console.log('U+' + p.codePointAt(0).toString(16).toUpperCase(),
    csvCell(value).startsWith('"\t') ? 'guarded' : 'not guarded');
}
```

## Interpretation and limitations
The guard recognises a selected set of whitespace/format characters, but not all invisible/control prefixes. **Whether any listed unguarded prefix is ignored, stripped or treated as text by Excel, Google Sheets or another spreadsheet is unknown.** No spreadsheet engine, CSV import, formula execution, or save/reopen operation was tested in this audit. A tab prefix itself is not a universal mitigation; downstream software may transform CSV text.

The exported data is manually entered and local to the user's browser, limiting exposure relative to server-collected third-party inputs. JSON export is intended to preserve exact original values; that property was not independently re-tested for these ten cases.

## Decision and next experiment
1. Keep PR #29 **draft and unmerged**; do not label CSV output universally safe.
2. Prioritise a controlled **real spreadsheet** import + save/reopen matrix using harmless `=1+1`, including these invisible-prefix cases, the existing tab-guarded cases, and ordinary text. Record application/version, locale, import route, formula-bar content and raw round-trip CSV bytes.
3. Do **not** expand the sanitizer solely because a prefix is invisible; first establish the importing engine's actual treatment, to avoid needless data corruption. Retain the exact-text JSON alternative.
4. Add permanent regression cases only after determining the desired semantics.

Reference: OWASP CSV Injection guidance, https://owasp.org/www-community/attacks/CSV_Injection and https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/07-Injection/21-CSV_Injection/.

**Disclosure:** Prepared and executed by GPT-6 as part of Kai Laboratory's AI-directed experimental research. No human review, third-party endorsement or spreadsheet security certification is claimed.
