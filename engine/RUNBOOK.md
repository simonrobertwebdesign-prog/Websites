# Runbook for automated runs

History: batch 1 (10 previews) was approved by Simon and sent on 18 Nov 2026.

Every scheduled run starts fresh. Read this whole file first and follow it exactly.

## The business

- Simon Robert Web Design. Simon is a college student in Oxfordshire. He reviews work; Claude does the rest.
- Offer (never change it without Simon): **Standard £400 / Premium £900**, one-off. 2 rounds of changes. Live within 7 days of the go-ahead. Client buys their own web address (~£10/yr). 50% upfront, 50% before go-live. Optional £30/month care plan.
- Gmail: simonrobert.webdesign@gmail.com (Gmail connector).
- Repo: `simonrobertwebdesign-prog/websites` (attach with add_repo, access "push"). Commit as `Simon Robert Web Design <simonrobert.webdesign@gmail.com>`; push with `git -c push.negotiate=true push origin HEAD:main`.
- Hosting: Netlify project `simonrobert-webdesign`, site id `e785ab4c-4176-49b8-b92b-d6099339a016`, live at https://simonrobert-webdesign.netlify.app. Every push = one deploy.
- Tracker: Sheets artifact `cc2b043c-fd2c-4b11-891a-160bec533506` (node `f0971686-24a8`, engine `workbook`). Tabs: **Email leads**, **Do not contact**, **Scripts**, Leads (old, ignore).

## Hard rules (never break these)

1. **Simon approves every email in the chat first.** Create each email as a Gmail draft, then show Simon in the chat (SendUserMessage) who it goes to, why, the preview link and the email text, and ask for his go-ahead. Send only after he says go (or names which ones), and send by draft id (`send_message` with `draftId`) so nothing can ever go twice. If he asks for a change, update the draft and ask again. If he doesn't answer, send nothing.
2. **Only limited companies.** Check each one is **Active** on Companies House (find-and-update.company-information.service.gov.uk) and record the company number. Never email sole traders or partnerships.
3. **Check the Do not contact tab and Gmail (search the address) before drafting.** Never contact anyone twice unless they replied.
4. The email address must be one the business publishes itself (its website, Which? Trusted Traders, etc.).
5. **Reviews:** only real 5-star reviews, word for word. Trim with "…" and never change words. Label them with where they came from (e.g. "Which? review"). Never invent a reviewer name.
6. **No invented facts.** Years trading, accreditations, insurance, areas, "free quotes" etc. must come from the business's own published info. If unsure, leave it out. Set `"free_quotes": true` only if the business says it offers free quotes.
7. The "what's wrong with your current site" line in each email must be something you saw on their site **today**. "No website" only if a web search finds none.
8. Photos: Unsplash only, `plus: "none"`, call `download_asset` for every photo used, and credit photographers in `credits`. Emails say the photos are stock.
9. **At most 10 new leads per day.**
10. Run `python3 engine/check.py --prune` before every push. **Never push if it fails.** One push per run.
11. Anything outside the standard offer (discounts, extra pages, deadlines, payments, logins, legal questions): don't agree. Draft a holding reply and tell Simon.
    **Price complaints** (agreed with Simon 18 Nov 2026), in this order and one step per reply: (1) don't cut the price, remind them what they get (already built, live in 7 days, 2 rounds of changes, they own it); (2) offer Standard £400 instead of Premium; (3) point out they only pay half (£200) to start; (4) last resort only: Standard for £300 if paid in full upfront. **Never offer less than £300.** Simon still approves every reply.
12. Never handle money, bank details, card details or passwords. Simon sends payment details himself.

## Run A: inbox check (9am and 5pm)

1. **Sent emails:** search Gmail `in:sent newer_than:3d`. For every lead email Simon sent, set the tracker Status to **Preview sent** and fill **Date emailed**.
2. **Replies:** search `in:inbox newer_than:3d -from:me`. For each reply from a lead:
   - "stop", "no thanks", unsubscribe, or annoyed → straight away (no approval needed): add to **Do not contact** (business, email, date, reason), set Status **Not interested**, and remove their preview (delete `engine/data/<slug>.json`, run `check.py --prune`, push). Draft the short "No problem, I won't email again" reply and ask Simon before sending it.
   - Interested or asking a question → draft a reply using the Scripts tab, set Status **Replied** (or **Said yes**), then show Simon in the chat what they said (short) and your suggested reply, and ask for his go-ahead before sending.
   - Out-of-office or bounce → note it in the tracker; do nothing else.
3. **Website enquiries:** read Netlify form submissions (`manage-form-submissions`, site id above). For each new one, add it to the tracker and draft a reply.
4. **One follow-up only:** if an email was sent 7+ days ago with no reply, draft one short, polite follow-up in the same thread (with the "reply stop" line) and ask Simon before sending. Never a second one. After 14 days with no reply set Status **No reply**.
5. **Clean-up:** previews for leads marked No reply or Not interested for 90+ days get removed (the privacy page promises this).
6. Message Simon only if something needs him (emails to approve, someone said yes, a question you couldn't answer). When he says go, send the approved drafts and update the tracker.

## Run B: new leads (once a day)

1. Read the tracker (Email leads + Do not contact) so you don't repeat anyone. If 10 or more leads are still **Draft ready** (Simon hasn't approved them yet), build nothing new: just remind him in one line that they're waiting.
2. **Find businesses.** Which? Trusted Traders listings work well: `https://trustedtraders.which.co.uk/<trade>-in-<town>/` (trades: electricians, plumbers, roofers, builders, landscape-gardeners, painters-and-decorators, carpenters-and-joiners, tree-surgeons, driveways-and-patios). In the browser, each listing card has a JSON-LD script with name, email, phone and rating. Keep names containing Ltd/Limited with 5+ reviews. Business pages (`/businesses/<slug>/`) list the website, about text, services and reviews (`.review.site-review`, each with `meta[itemprop=ratingValue]` scores).
3. **Check the current website** (or confirm there isn't one). Good reasons to contact: no website, not built for phones (no viewport meta), "Not secure" (no https), placeholder text, broken or missing phone number, spam links, no reviews shown, very thin content. If the site is already good, skip them.
4. **Companies House:** confirm Active, note the company number and directors' first names (use the right first name in the email).
5. **Write the data file** `engine/data/<slug>.json` with `"mode": "preview"`. Copy the pattern in `engine/batches/batch01_make.py` (save each day's script as `engine/batches/batchNN_make.py`).
6. `python3 engine/check.py --prune` → commit → push. Confirm the deploy is ready (Netlify MCP `get-project`), then confirm each new preview URL returns 200.
7. **Draft the emails** as Gmail drafts using the cold email in the Scripts tab. Each one must include: who Simon is, where you found them, the one honest problem, the Premium link `https://simonrobert-webdesign.netlify.app/p/<slug>/`, the Standard link `.../p/<slug>/standard/`, the prices, that photos are stock, and the last line: `If you'd rather not get emails from me, just reply "stop" and I won't contact you again.`
8. Add a row per lead to **Email leads** with Status **Draft ready**.
9. **Ask Simon for the go-ahead in the chat** (one SendUserMessage): a numbered list with, for each lead, the business, town, the one problem you found and the Premium preview link; then the email wording once (it's the same for everyone apart from the name and the problem line). End with: "Reply **go** to send them all, or tell me which numbers to skip or change."
10. When Simon replies go (or names numbers), send those drafts by draft id, set their Status to **Preview sent** with today's date, and confirm in one line. Leave skipped ones as drafts and mark them **To check**.

## When someone says yes

Stop and tell Simon. The first go-live is done together: collect their logo, photos and details, switch the data file to `"mode": "live"`, create their own Netlify project, connect their domain and add a form notification email for the client.

The "Powered by Netlify" badge can only be turned off on a paid Netlify plan (Simon will upgrade after the first sale). Until then `site.js` detects the badge and lifts the phone call bar above it, so nothing is covered.
