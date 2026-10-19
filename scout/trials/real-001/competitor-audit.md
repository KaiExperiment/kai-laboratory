# SCOUT preliminary competitor audit — 19 October 2026

**Research question:** Is another basic UK Etsy fee or handmade pricing calculator a defensible new product?

**Status (19 October 2026):** Public competitor pages and Etsy's primary policy were reviewed. This is a **published-feature audit only**: we did not enter scenarios into competitors' tools, independently execute their calculations, measure usability, interview sellers or verify adoption. Public feature descriptions are not proof that a tool works as advertised or that sellers need another product.

| Existing alternative | Published capability | Source |
| --- | --- | --- |
| ProfitHatch | Free UK Etsy fee calculator; says it accounts for UK fee VAT, regulatory fee and offsite ads | https://profithatch.co.uk/etsy-fee-calculator/ |
| Haul by Huskai | Free handmade pricing calculator covering materials, labour, overhead, shipping and marketplace fees | https://huskai.co.uk/tools/profit-calculator |
| Specifek | Free 2026 Etsy fee and profit calculator with country selection, material and labour inputs | https://www.specifek.co.uk/etsy-calculator/ |
| Crafters Vinyl | Free craft pricing calculator including batch setup time, wastage, margin versus markup, VAT and platform presets | https://www.craftersvinyl.co.uk/craft-pricing-calculator/ |
| Free Etsy Calculator | Free UK seller fee calculator with materials, shipping, labour, packaging and ad costs | https://freeetsycalculator.com/uk/etsy-fee-calculator/ |

**Finding:** Several public tools already advertise substantial overlap with a basic UK fee or handmade-pricing calculator. The existence of these alternatives weakens any unqualified novelty or differentiation claim. It does **not** establish which tools are accurate, widely used, or adequate for a particular seller.

**Primary-source fee check (19 October 2026):** Etsy's current regulatory operating fee help page explicitly lists the **United Kingdom at 0.48%**, charged on item price plus postage and relevant extras: https://help.etsy.com/hc/en-gb/articles/1500011073202-What-is-a-Regulatory-Operating-Fee . Etsy's announcement says the UK rate rose **from 0.32% to 0.48% on 22 June 2026**: https://community.etsy.com/forum/announcements-290/topic/regulatory-operating-fee-updates-for-some-markets-181930/ . Its primary fees policy confirms the **6.5% transaction fee** and **US$0.20 listing fee**, with country-specific payment processing and conditional charges: https://www.etsy.com/uk/legal/fees . Do not present the old 0.32% rate as a current alternative or silently assume that all fee types have the same base. Some calculators explicitly display 0.48%; this audit has **not** established that any named competitor currently uses the outdated rate.

**Feature-overlap observation:** Crafters Vinyl publicly lists quantity, batch setup time, wastage, VAT status and margin/markup controls. Free Etsy Calculator publicly lists material, labour, packaging, advertising and sensitivity calculations. These advertised features already overlap several proposed W01–W06 scenarios; actual numerical accuracy remains untested. The current Kai calculator requires manual allocation for batches and does not model VAT or separate marketplace fee bases. See `workflow-test-plan.md` and `tests/maker-workflow-scenarios.test.cjs` for reproducible *synthetic* internal tests (not competitor tests).

**SCOUT decision:** No evidence yet of willingness to pay, unmet needs, or sufficient differentiation. Do not shortlist a new generic calculator or claim a validated market. Our existing Maker Profit Calculator remains an experimental free tool, not proven competitive advantage.

**Next falsification experiment:** Test a small representative set of real maker workflows against these alternatives and our existing tool. Record tasks, completion failures, actual seller feedback and evidence of paid willingness-to-pay separately. Obtain consent before contacting people; avoid mass outreach.
