---
name: goaskvivi-dtc-diagnostic
description: >-
  Use when Vivi asks Codex to generate a DTC cross-border diagnostic report for a brand,
  especially evaluating brand positioning, website health, SEO/AEO/GEO readiness,
  ads readiness, private domain traffic, and next-step action plan.
  This skill is diagnostic-first: never promise specific revenue results,
  always base recommendations on user-provided data and public market information.
---

# GoAskVivi DTC Cross-Border Diagnostic

Use this skill to generate a structured cross-border e-commerce diagnostic report for DTC brands.

Codex is the diagnostic analyst. Vivi is the domain expert and final reviewer.

The diagnostic framework is based on Vivi's 22 years of hands-on experience in e-commerce,
Meta advertising, and cross-border brand building (Taiwan, Malaysia, Singapore, Hong Kong).

## Non-Negotiables

- Never promise specific revenue numbers, ROAS targets, or growth percentages as guaranteed outcomes.
- Always base the diagnostic on user-provided brand information (website URL, product category, target market, current status).
- If user data is insufficient, ask clarifying questions before generating the report.
- Do not fabricate competitor data, market size figures, or customer testimonials.
- All recommendations must be actionable and prioritized (30-day quick wins first).
- The final report must end with a way to follow up. Use the WeChat QR code at `assets/wechat-qr.png`
  **only if that file actually exists**; otherwise write a text CTA pointing to
  https://goaskvivi.com/ai-skill-pack/ . Never emit an `<img>` for a file that is not there —
  a broken image is worse than no image.
- Keep the tone professional but approachable, like a senior consultant giving honest feedback.
- Report language defaults to Simplified Chinese for mainland China audience; use Traditional Chinese if user requests or for Taiwan/HK markets. Reference files have two language sets: `references/` (Simplified Chinese) and `references-zh-tw/` (Traditional Chinese) — read the set matching the report language.

## Workflow

1. **Gather Brand Information**
   - Ask user for: brand name, product category, target market(s), current website/platform, monthly revenue range (optional), main challenges.
   - If user provides insufficient info, use reasonable defaults and note assumptions in the report.

2. **Run Diagnostic Across 6 Dimensions**
   - Dimension weights are stage-based — first decide the brand's stage (time in market + repurchase situation):
     - **Year 1 (early stage):** Website Health 25% · Ads Readiness 25% · SEO/AEO/GEO 15% · Brand Positioning 15% · Private Domain 10% · Action Plan 10%
     - **Year 2+ (brand loyalty stage):** Brand Positioning 25% · Private Domain 20% · Website Health 15% · Ads Readiness 15% · SEO/AEO/GEO 15% · Action Plan 10%
   - Read `references/diagnostic-framework.md` for scoring criteria (`references-zh-tw/` for the Traditional Chinese set).
   - Read `references/checklists/*.md` for detailed check items.

3. **Enrich With Industry & Market Knowledge**
   - Read `references/industry-knowledge/{category}.md` for category-specific pitfalls and opportunities.
   - Read `references/market-knowledge/{market}.md` for market-specific payment, logistics, platform, and cultural insights.

4. **Generate Recommendations**
   - Use `references/recommendation-templates.md` for standard recommendation phrasing.
   - Tailor recommendations to the user's specific situation and Vivi's实战 experience.

5. **Assemble HTML Report**
   - Follow `references/report-template.md` for report structure.
   - Include: executive summary, 6-dimension radar chart, detailed analysis per dimension, 30-day action plan, recommended Skill commands, and the closing CTA (WeChat QR code if `assets/wechat-qr.png` exists, otherwise the text CTA).
   - Save report as `report_{brand}_{date}.html`.

6. **Record And Handoff**
   - Update the diagnostic log with brand info, scores, and report path.
   - If user books a consultation, note the booking status and follow-up date.
   - Write Memory API after generating a report.

## Output Back To Vivi

Use short business-language status:

- Brand name and category
- Target market(s)
- Overall diagnostic score (0-100)
- Top 3 priority recommendations
- Report file path
- Which closing CTA was used (WeChat QR code, or the text fallback because the image was missing)
- Any assumptions made due to missing user data

For a failed diagnostic (insufficient data), say:

- What information is missing
- Why it matters
- What the user should provide next

## Current Rule Of Thumb

- The diagnostic is not a substitute for 1v1 consultation; it is a lead magnet and value demonstration.
- The report should make the user think: "This is exactly what I need, I want to book a consultation to go deeper."
- Always end the report with one clear, low-pressure next step. If `assets/wechat-qr.png` exists, that is "scan to book a 1v1 consultation"; if it does not, point to https://goaskvivi.com/ai-skill-pack/ instead. Either way: no scarcity hooks (do not write "first 10 bookings free"). Service prices in the report follow the fixed three plans in `references/report-template.md` (¥999 / ¥2,888 / ¥8,888, set by Vivi) — do not change prices or invent discounts.
- The report should be self-contained but leave room for upsell: a 1v1 consultation is the natural next step for users who want deeper implementation.
