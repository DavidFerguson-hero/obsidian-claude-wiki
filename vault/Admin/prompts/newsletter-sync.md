# Newsletter sync (optional input feed)

Copies the newsletters you subscribe to from your email into `00 Inbox/`, one note per issue, so the daily ingest picks them up. Most people's best reading arrives by email — this gets it into the vault without forwarding anything by hand.

- **Writes only to `00 Inbox/`.** It never touches the wiki; the daily ingest does that.
- **Never copies an issue twice.** Each note records the email's ID, and the task checks the inbox and the archive before writing.

**Needs:** the **Gmail** connector in Claude (Settings → Connectors). If you use Outlook, the same prompt works with an Outlook connector — change "Gmail" to "Outlook".

**Schedule:** daily, an hour **before** the daily ingest (e.g. 04:30 if the ingest runs at 05:30). Weekly works too if you only follow weekly newsletters.

Copy everything below the line into a scheduled task, and fill in the two lines marked ←.

---

Copy my newsletters from Gmail into my Obsidian vault at `PATH/TO/YOUR/VAULT` ← replace this.

NEWSLETTERS: `newsletter@example.com, digest@another-example.org` ← the sender addresses to copy (find them on any issue you've received)

Write only to `00 Inbox/`. Never edit any other part of the vault, never delete anything, never reply to or change any email (read only — don't mark as read, label, archive or delete).

1. **Find new issues.** Search Gmail for messages from the NEWSLETTERS senders received in the last 8 days. Get each message's ID.
2. **Skip ones already copied.** Look for that ID in the `email_id:` field of notes in `00 Inbox/` and `40 Archive/Processed captures/`. If it's there, skip the message.
3. **Write one note per issue** to `00 Inbox/`, named `Newsletter name - Issue title (YYYY-MM-DD).md` using the date it was sent. File names must not contain `: ? * " < > | / \` — use a dash instead of a colon — and keep them under about 120 characters. Frontmatter:

   ```yaml
   ---
   title: "Newsletter name - Issue title"
   type: capture
   newsletter: "Newsletter name"
   from: "sender@example.com"
   sent: YYYY-MM-DD
   email_id: "the Gmail message ID"
   source_url: "the issue's 'view in browser' link, if there is one"
   tags: ["newsletter"]
   ---
   ```

4. **Body:** the issue's content as clean Markdown — headings, paragraphs and every article link, kept as `[text](url)`. Remove tracking pixels, unsubscribe and preference links, ads, sponsor blocks and the email footer. Where a link is a tracking redirect and the real address is visible, use the real address. Don't summarise or rewrite: this is a capture, and the ingest relies on the original wording and links.
5. **Report** in one line per newsletter: how many issues were copied and how many skipped as already copied. If nothing new arrived, say so in one line.

If an issue is mostly images with almost no text, write the note with the text you have and add a line saying "Mostly images — open the original" with the `source_url`.
