# CS50x Final Project — KJV Bible Web Application

## Master Development Roadmap

> **Small project. Real engineering. Deep understanding.**

---

### About this document

This is the master guide for building a small King James Version Bible reading web application with
accounts and personal verse notes. It teaches you *how to build it yourself*. It deliberately contains
**no copy-paste implementation** — no finished routes, no finished templates, no finished SQL, no
finished JavaScript, no finished authentication code. Everything here describes **requirements,
concepts, decisions, responsibilities, tests, and completion criteria** so that you can write the code
yourself and be able to defend it in your CS50x presentation.

### How to use it

1. Read sections 1–7 once, end to end, **before writing any code**. That is your design phase.
2. Then execute section 8 (the phased roadmap) **strictly in order**. One phase at a time.
3. Do not start a phase until the previous phase's **Completion Criteria** are all checked.
4. Every time you hit a **Checkpoint**, stop and answer the questions out loud (or in a notebook)
   before continuing. If you cannot answer, you do not yet own that part of the project.
5. Keep the file open while you code. Tick boxes as you go.

### Conventions used in this document

| Symbol | Meaning |
| --- | --- |
| `- [ ]` | A concrete task you must complete |
| **Gate** | A hard stop. Next phase is blocked until this is satisfied |
| **Checkpoint** | A comprehension stop, not a coding task |
| **Decide** | A design decision you must make (there is no single right answer) |
| **Trap** | A mistake that will cost you hours if you don't know about it |
| § | Reference to a section of this document |

### Your current environment (verified)

| Item | Value | Why it matters |
| --- | --- | --- |
| OS / IDE | Windows + VS Code | Activate your virtual environment with the Windows script path (`.venv\Scripts\activate`), not `bin/activate` |
| Python | 3.14.6 | Modern Python. F-strings, `pathlib`, `dataclasses`, `dict` ordering all available |
| Flask | 3.1.3 | Flask 3.x conventions apply. `before_first_request` **no longer exists** (removed in 2.3) — see §8 Phase 1 Trap |
| Werkzeug | 3.1.8 | Provides `generate_password_hash` / `check_password_hash`. Default hash is **scrypt** |
| SQLite | 3.50.4 | Ships with Python via the `sqlite3` module. No server to install |
| `cs50` library | importable | CS50's SQL helper is available. See the **Decide** in §8 Phase 5 about whether to use it |

### Table of contents

1. [Project Overview](#1-project-overview)
2. [Final Feature Specification](#2-final-feature-specification)
3. [User Flow](#3-user-flow)
4. [Application Architecture](#4-application-architecture)
5. [Recommended Project Structure](#5-recommended-project-structure)
6. [Database Design](#6-database-design)
7. [Bible Data Architecture](#7-bible-data-architecture)
8. [Development Roadmap](#8-development-roadmap)
9. [Learning Checkpoints](#9-learning-checkpoints)
10. [CS50 Concepts Mapping](#10-cs50-concepts-mapping)
11. [Testing Strategy](#11-testing-strategy)
12. [Security Checklist](#12-security-checklist)
13. [UI/UX Plan](#13-uiux-plan)
14. [JavaScript Plan](#14-javascript-plan)
15. [Git and Development Workflow](#15-git-and-development-workflow)
16. [Debugging Methodology](#16-debugging-methodology)
17. [Common Beginner Mistakes](#17-common-beginner-mistakes)
18. [Scope Control](#18-scope-control)
19. [Final Quality Checklist](#19-final-quality-checklist)
20. [CS50 Final Project Requirements](#20-cs50-final-project-requirements)
21. [Final Demonstration Plan](#21-final-demonstration-plan)
22. ["Before You Ask AI" Rule](#22-before-you-ask-ai-rule)
23. [Definition of Done](#23-final-definition-of-done)

---

## 1. Project Overview

### What the application is

A small server-rendered web application that lets a person read the King James Version of the Bible
book by book and chapter by chapter, search the entire text for words and phrases, create an account,
and attach private personal notes to individual verses. Every page is produced by Flask and Jinja from
data that lives in a local Bible file plus a small SQLite database that stores only *your users and
their notes*.

### What problem it solves

Reading and searching scripture in a plain text file or a PDF is clumsy: you cannot jump to a chapter
quickly, you cannot search, and you cannot keep your own thoughts attached to the verse that provoked
them. This application solves exactly three problems:

1. **Navigation** — get to any book/chapter/verse in a couple of clicks.
2. **Discovery** — find every verse containing a word or phrase.
3. **Reflection** — write and keep private notes anchored to specific verses, and find them again later.

It deliberately does **not** try to be a general-purpose Bible platform.

### Who it is for

* A single reader with an account (you, and anyone you share the link with).
* A grader/evaluator who must be able to register, log in, read, search, and manage notes in under
  two minutes of clicking.
* **Not** for: teams, congregations, public discussion, or anonymous mass traffic.

### The core user experience

```text
Open app ──► Browse books ──► Pick a chapter ──► Read verses
                                   │
                                   ├──► Search word/phrase ──► Matching verses ──► jump to chapter
                                   │
                                   └──► Click a verse ──► Write a note ──► Save (only I can see it)
```

In one sentence: *"Read the Bible by book and chapter, find any verse by search, and keep private
notes on the verses that matter to me."*

### Why this is appropriate for CS50x

| Aspect | Why it fits CS50x |
| --- | --- |
| Scope | Two database tables, ~8 pages, one data file. Finishable in a realistic timeframe |
| Demonstrates C-level thinking | Building a lookup/index structure over the Bible text instead of scanning blindly |
| Demonstrates Python | File handling, JSON parsing, string normalization, data structures, functions, error handling |
| Demonstrates SQL | Schema design, CRUD, JOINs, PRIMARY/FOREIGN KEY reasoning, filtering, ordering |
| Demonstrates web | Flask routing, request/response cycle, sessions, form handling, redirects, status codes |
| Demonstrates security | Password hashing, authorization checks, SQL parameterization, input validation |
| Demonstrates frontend | HTML semantics, Jinja templating, CSS/Bootstrap layout, purposeful JavaScript |
| Demonstrable | A grader can see every feature working live in a 5–8 minute video |

### What this project intentionally does NOT attempt

Multiple translations · original languages / Strong's concordance · audio · cross-references ·
commentaries · public sharing · social features · chat · AI assistants · notifications · streaks ·
gamification · mobile apps · offline sync · complex admin dashboards · recommendation engines ·
user-generated content beyond private notes.

### Project scope statement

> **This project is a single-translation (KJV) Bible reading web application. It provides book and
> chapter navigation, full-text search, optional user accounts, and private per-verse notes stored in
> SQLite. Bible text is read from a bundled JSON data file and is never modified at runtime. Users can
> only ever read and modify their own notes. Anything beyond these features is explicitly out of scope
> for this submission (§18).**

### In-scope success criteria (memorize these)

- [ ] Bible browsing works for **every** book and chapter in the dataset, including the first and last.
- [ ] Search returns correct matches and never crashes on weird input.
- [ ] A user can register, log out, and log back in.
- [ ] A logged-in user can create, read, edit, and delete notes.
- [ ] A logged-in user **cannot** read or modify another user's notes, even by editing the URL.
- [ ] No feature requires the user to know anything about the underlying files or database.

---

## 2. Final Feature Specification

### Required vs Optional at a glance

| ID | Feature | Priority | Depends on |
| --- | --- | --- | --- |
| F1 | Book index (list all 66 books) | **Required** | Bible data |
| F2 | Chapter reader (display verses) | **Required** | F1 |
| F3 | Chapter navigation (prev/next, jump to book/chapter) | **Required** | F2 |
| F4 | Search verses (word/phrase) | **Required** | Bible data |
| F5 | Registration | **Required** | Database |
| F6 | Login / Logout | **Required** | F5 |
| F7 | Create note on a verse | **Required** | F2 + F6 |
| F8 | View my notes (per chapter and/or a notes page) | **Required** | F7 |
| F9 | Edit my note | **Required** | F8 |
| F10 | Delete my note | **Required** | F8 |
| F11 | Authorization (notes are private to their owner) | **Required** | F6 + F7 |
| F12 | Graceful handling of bad input / not-found pages | **Required** | F2 |
| O1 | Notes list filtering/search | Optional | F8 |
| O2 | "Jump to my note" highlighting in a chapter | Optional | F8 |
| O3 | Copy-verse-to-clipboard button | Optional | F2 |
| O4 | "Remember my last reading position" | Optional | F1–F3 |
| O5 | Search result pagination | Optional | F4 |
| O6 | Public-domain commentary/reading plan | **Out of scope** | — |

The rules for building: **F1–F12 only.** Optional features are added only after §19 is fully checked.

---

### F1 — Book Index

**Purpose** — The entry point to reading. Gives the user an overview of the canon and a way in.

**Expected behavior** — Visiting the reading entry point lists every book in canonical order (Genesis
through Revelation). Each book is clearly selectable. The list must be complete and correctly ordered;
no book should be missing, duplicated, or misspelled.

**User interaction** — User opens the app, scans or scrolls the list, clicks a book.

**Backend responsibilities** — Load the Bible data (or its prebuilt index) and produce an ordered
collection of book display names plus their stable identifiers and chapter counts. It must not read the
whole Bible text into the response if a light-weight list is enough.

**Database responsibilities** — None. The Bible is not stored in SQLite (see §7).

**Frontend responsibilities** — Render the list in a readable, scannable layout (grouped by
Old/New Testament is a nice touch, not a requirement). Every item must be a real link so it works
without JavaScript.

**What needs to be tested** — Total book count is exactly 66; the first item is Genesis and the last is
Revelation; clicking any book leads to a valid chapter page.

---

### F2 — Chapter Reader

**Purpose** — The heart of the application: actually reading scripture.

**Expected behavior** — Given a valid book and chapter, the page displays that chapter's verses in
order, each verse labelled with its number. Verses are individually addressable (i.e. a verse's number
is visible next to the text) so notes can be attached to them. The page shows which book and chapter is
being read.

**User interaction** — User reads; user can click/hover a verse to reveal a "note" affordance.

**Backend responsibilities** — Validate the requested book and chapter against the dataset; if invalid,
respond with a "not found" style page and an appropriate HTTP status rather than a crash or a blank
page. Provide the chapter's verses (numbers + text) plus the reference metadata needed for navigation.

**Database responsibilities** — When the user is logged in, also fetch **that user's** notes for the
requested chapter so they can be displayed inline. Anonymous visitors get no note data.

**Frontend responsibilities** — Render verses as an ordered, readable list; visually distinguish a
verse that already has a note; provide the click target/affordance for creating a note.

**What needs to be tested** — Genesis 1 (first chapter), Revelation 22 (last chapter), a Psalm
(e.g. Psalm 119, the longest chapter), a chapter in a short book (e.g. 3 John), and a book with a
single chapter (Obadiah / Jude / Philemon).

---

### F3 — Chapter Navigation

**Purpose** — Without this the reader is a dead end and users will use the browser back button instead.

**Expected behavior** — From any chapter the user can move to the previous chapter, the next chapter,
another chapter of the same book, and another book, without going back to the index. At the boundaries
(first chapter of the Bible, last chapter of the Bible) navigation must not produce a broken link.

**User interaction** — Clickable Previous/Next controls plus a chapter picker (dropdown or number list).

**Backend responsibilities** — Compute neighbour references from the dataset so boundaries can be
detected server-side; never let the template invent a reference that does not exist.

**Database responsibilities** — None.

**Frontend responsibilities** — Show controls only when they make sense (or disable them at the
boundaries). Keep the controls in a consistent place on the page.

**What needs to be tested** — Previous on Genesis 1; Next on Revelation 22; Next at the end of every
book; Previous at the start of every book; the chapter picker contains exactly the number of chapters
that book has.

---

### F4 — Search

**Purpose** — Turn the whole Bible into something the user can interrogate.

**Expected behavior** — The user submits a word or phrase and receives a list of matching verses, each
showing the reference (book, chapter, verse), the verse text with the match visible, and a link that
opens the chapter containing it. Matching should be case-insensitive. An empty query must not crash or
return the whole Bible. A query with no matches must return a clear "no results" message, not an error.

**User interaction** — Type into a search box (available from the reader pages), submit, read results,
click a result to read it in context.

**Backend responsibilities** — Validate and normalize the query (trim, reject empty/oversized input),
search the Bible in memory, and return results in a deterministic order (canonical order, or by
relevance if you can justify it). Decide and document whether *all* matches are returned or a capped
number is returned.

**Database responsibilities** — None (search runs over the Bible data). Optionally, later, SQLite FTS5 —
but only as a stretch goal with a clear justification (§7).

**Frontend responsibilities** — Provide the form; render results compactly; show the total number of
matches; keep the query string visible after searching; make each result navigable.

**What needs to be tested** — A very common word (e.g. "the", "God", "love"), a word that appears
exactly once, a word that appears zero times, differing letter case ("Begat" vs "begat"), a
multi-word phrase, punctuation and apostrophes ("LORD's"), leading/trailing spaces, an empty query,
an absurdly long query, and HTML/`<script>` style input (must be escaped in the output, never executed).

---

### F5 — Registration

**Purpose** — Notes must belong to somebody, so the app needs identities.

**Expected behavior** — A visitor supplies a username and password, plus confirmation of the password.
Successful registration creates exactly one user, stores a **hash** of the password, and either logs
the user in or sends them to the login page with a success message. Duplicate usernames are rejected
with a clear, friendly error and the form's entered username preserved.

**User interaction** — Fill a form, submit, get feedback.

**Backend responsibilities** — Validate: required fields, username length/characters, password
confirmation match, password minimum length, username not already taken. Report **all** appropriate
errors at once where reasonable, re-rendering the form rather than throwing an error page.

**Database responsibilities** — Uniqueness of username enforced by the schema itself (a UNIQUE
constraint), not only by a "check then insert" in Python. Never store the plaintext password.

**Frontend responsibilities** — An accessible HTML form with labels, `required` attributes, sensible
`input` types, and a place to display errors.

**What needs to be tested** — Empty username; empty password; mismatched confirmation; too-short
password; duplicate username; username with surrounding whitespace; a username differing only by case;
very long username; successful registration followed immediately by login.

---

### F6 — Login / Logout

**Purpose** — Identify the current user on every request so notes can be private.

**Expected behavior** — A registered user can log in with username + password and is then recognised on
subsequent pages (their notes appear, navigation shows their identity). Logout ends the session
completely; after logging out, protected pages must not work.

**User interaction** — Log in from any page; log out from any page.

**Backend responsibilities** — Verify credentials by hashing the supplied password and comparing to the
stored hash (or using a verification helper). On success, record the identity server-side in the
session. On failure, return a single generic error message ("invalid username and/or password") that
does **not** reveal whether the username exists.

**Database responsibilities** — Look up the user by username; read the stored password hash and the
user's id.

**Frontend responsibilities** — Show login/logout state in the navigation ("Log In" vs "Log Out" +
username). Never expose the password hash or user id in the HTML.

**What needs to be tested** — Valid login; wrong password; nonexistent username; empty fields; login
with trailing spaces; logout then attempting to reach a protected page; visiting the login page while
already logged in; keeping the session across page visits; behaviour after clearing cookies.

---

### F7 — Create Note

**Purpose** — The feature that makes this project more than a static Bible viewer.

**Expected behavior** — A logged-in user, while reading a chapter, can select a verse and write note
text. Saving stores the note against that verse **and** that user. On redisplay, the verse shows that
the user has a note, and the note content is visible to that user only. Anonymous visitors who try to
create a note are redirected to login (with a message) instead of receiving an error.

**User interaction** — Click a verse (or its note control) → a note editor appears → type → save →
the note becomes visible attached to that verse.

**Backend responsibilities** — Require authentication; require a POST; validate the submitted reference
(book/chapter/verse must be real and must exist in the dataset — never trust a hidden form field);
validate the note body (non-empty after trimming, within a maximum length); then persist.

**Database responsibilities** — Insert a row in the notes table with the owner's user id, the verse
reference, the text, and a creation timestamp. Decide explicitly what happens when the user already has
a note on that verse (see **Decide** below) and enforce that decision consistently.

**Frontend responsibilities** — Provide the editor; prevent saving an empty body; give clear success
feedback after saving. JavaScript must be an *enhancement* — saving must still work if JavaScript fails.

**What needs to be tested** — Create a note as user A; attempt to create with an empty body; attempt a
very long body; attempt to create while logged out; submit a verse reference that does not exist
(tamper with the form value); create notes on two different verses; create a second note on the same
verse.

**Decide** — *One note per verse per user* (cleanest: a UNIQUE constraint on owner+reference) **or**
*many notes per verse per user*? Pick one, write it in your README, and make the UI consistent with it.
Recommendation: one note per verse per user — it matches the mental model of "my thought on this verse"
and makes edit/delete logic trivial.

---

## 3. User Flow

These are the journeys your routes and pages must support. Nothing here is code — it is the
*behaviour* you must be able to produce.

### 3.1 New user (first visit)

```text
Land on reading entry point (books list)
   │
   ├─► Click a book ──► chapter list/first chapter ──► read verses
   │
   └─► Click a verse's "note" control
          │
          ├─ not logged in ──► Redirect to Log In  (with a message: "log in to save notes")
          │                       │
          │                       └─► "Need an account?" ──► Register form
          │                                │
          │                                ├─ invalid input ──► redisplay form + errors (keep username)
          │                                └─ valid ──► account created ──► logged in ──► LOGIN succeeded
          │
          └─ logged in ──► note editor opens on that verse ──► save ──► note appears on the verse
```

**Key insight to implement:** the "log in first" detour is the moment most beginners get wrong. Decide
what the user should see *after* successfully logging in — the chapter they came from, or the books
list? Recommendation: send them back to the page they were on, and mention the original action.

### 3.2 Returning user

```text
Open app ──► Books list (or "My Notes" directly)
   │
   ├─► Search box ──► results ──► click result ──► chapter opens, target verse visible
   │                                             └─► note already shown on that verse (if it exists)
   │
   ├─► My Notes ──► list of my notes ──► edit / delete / click reference to jump to verse
   │
   └─► Log Out ──► reading still works, notes no longer appear, note controls now lead to Log In
```

### 3.3 Reading flow (anonymous is fine)

```text
Books list
   └─► Book selected ──► Chapter selected ──► Verses displayed
                                                   │
                                                   ├─► Previous chapter ─┐
                                                   ├─► Next chapter ─────┼─► stay in same book until
                                                   ├─► Same book, other ┤   boundary, then move to the
                                                   │   chapter (picker) │   neighbouring book
                                                   └─► Another book ────┘
```

The user must always be able to answer "where am I and how do I get somewhere else?" from the page
itself, without the browser Back button.

### 3.4 Search flow

```text
Any reading page ──► type query ──► submit
                                       │
                                       ├─ empty/invalid ──► message, no crash, form still usable
                                       ├─ no matches ──► "No verses found for 'x'" + suggestions
                                       └─ matches ──► results list (reference + text + link)
                                                          └─► click ──► chapter reader at that verse
```

### 3.5 Notes management flow

```text
My Notes page
   ├─► No notes ──► empty state explaining how to create one + link to books list
   └─► Notes exist
          ├─► Click reference ──► chapter reader, note visible inline
          ├─► Click Edit ──► editor prefilled ──► save ──► updated text + timestamp visible
          └─► Click Delete ──► confirmation ──► row disappears ──► success message
```

### 3.6 Error flows (must exist, must be friendly)

```text
Bad book      ──► "We couldn't find that book"        + link to Books list     (status: 404)
Bad chapter   ──► "That chapter doesn't exist"        + link to that book      (status: 404)
Bad verse     ──► "That verse doesn't exist"          + link to that chapter   (status: 404)
Unknown URL   ──► generic "Page not found" page                                (status: 404)
Server error  ──► "Something went wrong" page (no traceback shown)             (status: 500)
Not logged in ──► redirect to Log In + explanation                             (status: 302 → 200)
Wrong owner   ──► treated exactly like "not found" so nothing is leaked        (status: 404)
```

### 3.7 Flow-to-page mapping (fill this in yourself, then implement)

| User goal | Page the user sees | Type of request | Requires login? | Reads DB? | Reads Bible data? |
| --- | --- | --- | --- | --- | --- |
| See all books | Books list | GET | No | No | Yes |
| Read a chapter | Chapter reader | GET | No | Only for notes | Yes |
| Search | Search results | GET (query in URL) | No | No | Yes |
| Create an account | Register form | GET then POST | No | Yes (insert) | No |
| Sign in | Login form | GET then POST | No | Yes (select) | No |
| Sign out | — (redirect back) | POST | Yes | No | No |
| See my notes | My Notes | GET | **Yes** | Yes (filtered) | No |
| Save a note | — (redirect back to chapter) | POST | **Yes** | Yes (insert/update) | Yes (to validate) |
| Delete a note | — (redirect back) | POST | **Yes** | Yes (delete) | No |

**Checkpoint 3** — Before moving on, can you explain why "Create account" and "Sign in" are *two*
requests (GET then POST) while "Delete note" should only be one (POST)? If not, read §12 on
idempotency and method safety.

---

## 4. Application Architecture

### 4.1 The mental model

Your application is a **data-in, HTML-out machine**. A browser sends a request to a URL; Flask matches
that URL to a Python function; that function gathers data (from the Bible files, from SQLite, from the
session) and hands it to a Jinja template; the template renders HTML; the browser displays it.
Almost every bug you will encounter lives at one of exactly four seams:

```text
Browser ──(1)── Flask route ──(2)── Python logic ──(3)── Templates
                    │                                      ▲
                    │                                      │
                    └────────(4)──── SQLite / Bible data ───┘
```

1. **Request seam** — did the browser send what I thought it sent? (form fields, query params, cookies)
2. **Logic seam** — did my Python decide correctly? (validation, authorization, lookups)
3. **Template seam** — did the data I passed actually exist under the name the template expects?
4. **Data seam** — is the data in the shape I assumed? (SQL columns, JSON keys, variable types)

You will use this list constantly in §16 (Debugging Methodology).

### 4.2 Component architecture

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                              BROWSER                                         │
│  HTML pages (from Jinja)  +  CSS/Bootstrap  +  a little progressive JS       │
└───────────────▲──────────────────────────────────────────┬───────────────────┘
                │ HTML / redirects / status codes          │ GET & POST requests
                │                                          │ + session cookie
┌───────────────┴──────────────────────────────────────────▼───────────────────┐
│                              FLASK APPLICATION                               │
│                                                                              │
│  ┌──────────────┐   ┌────────────────────┐   ┌────────────────────────────┐  │
│  │ Route layer  │   │ Logic / helpers    │   │ Session (signed cookie)    │  │
│  │ (endpoints)  │──►│ - validation       │   │ holds "who is logged in"   │  │
│  │ - reader     │   │ - authorization    │   └────────────────────────────┘  │
│  │ - search     │   │ - search engine    │                                   │
│  │ - auth       │   │ - bible lookups    │                                   │
│  │ - notes      │   │ - db access funcs  │                                   │
│  └──────┬───────┘   └─────────┬──────────┘                                   │
│         │                     │                                              │
│         ▼                     ▼                                              │
│  ┌───────────────┐   ┌──────────────────┐   ┌─────────────────────────────┐  │
│  │ Jinja         │   │ SQLite           │   │ Bible data (read-only JSON) │  │
│  │ templates/    │   │ users + notes    │   │ loaded once, indexed in     │  │
│  │               │   │ (read/write)     │   │ memory for instant lookup   │  │
│  └───────┬───────┘   └──────────────────┘   └─────────────────────────────┘  │
│          │                                                                   │
│          ▼                                                                   │
│  ┌───────────────┐   ┌──────────────────┐                                    │
│  │ static/       │   │ config / secret  │                                    │
│  │ css, js, imgs │   │ key, db path     │                                    │
│  └───────────────┘   └──────────────────┘                                    │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Responsibilities, layer by layer

| Layer | Owns | Must never do |
| --- | --- | --- |
| **Routes** | Mapping URLs → functions; reading request data; calling validation/logic; returning a rendered template or redirect; choosing status codes | Contain the whole application's logic; write raw HTML; trust unvalidated input |
| **Logic/helpers** | Validation rules, authorization checks, Bible lookups, search, DB queries wrapped in functions | Know about HTML; depend on specific URL paths where avoidable |
| **Templates** | Presentation: looping, conditionals, escaping, layout | Query the database; do heavy computation; make authorization decisions |
| **SQLite** | Users, notes, constraints, relational integrity | Store Bible text (see §7); store plaintext passwords |
| **Bible JSON** | Read-only scripture text and structure | Be modified at runtime; be copied into the database "just in case" |
| **Session** | The identity of the current user only | Hold passwords or note bodies; hold anything that must stay private between requests |
| **Static files** | CSS, JS, images, fonts | Contain secrets or protected data |
| **JavaScript** | Enhancing interaction (notes panel, verse selection, client-side hints) | Be required for core functionality; hold authoritative data |

---

### 4.4 Request lifecycle (memorize this)

```text
1.  Browser requests GET /some/url?x=1
2.  Flask matches the URL rule → runs your view function
3.  View function reads request.args / request.form / session / cookies
4.  View validates input; if invalid → render a template with an error (HTTP 400/404)
5.  If auth is required → check the session; if absent → redirect to login (HTTP 302)
6.  View asks helpers for data (Bible lookups, SQL queries)
7.  View passes a context (dict of variables) to render_template()
8.  Jinja renders the template using that context (auto-escaping is on by default)
9.  Flask returns HTML + headers + status code; the session cookie may be updated
10. Browser renders HTML, then requests /static/... files (CSS, JS) in separate requests
```

**Checkpoint 4.1** — Can you explain why step 10 is a *separate* set of requests, and how that explains
why JavaScript is a different programming environment from Python?

**Checkpoint 4.2** — In step 6, who decides whether the current user may see a note: the route, the
helper, the template, or SQL? (Answer: the route/helper must, and SQL should filter too. The template
must never be the only gate.)

### 4.5 Why two data stores?

You are deliberately using **two** sources of truth: a read-only Bible file and a read/write SQLite
database. This is not over-engineering — it is the correct split:

| Question | Bible text | User data |
| --- | --- | --- |
| Does it change? | Never | Constantly |
| Who writes it? | You, once (import/verify step) | The application, per user |
| Who may read it? | Everyone | Only its owner |
| Size | ~4–5 MB of text | Tiny |
| Committed to Git? | Yes (it is source content) | No (the `.db` file is generated at runtime) |

Your database file must **never** be committed (§15, §18).

### 4.6 How the components talk to each other (the only paths allowed)

```text
Route ──► helper / bible function ──► SQLite or JSON ──► return plain Python data ──► route ──► template
                                                                                             │
Template ──► can only use variables the route passed ────────────────────────────────────────┘

JavaScript ──► can only read the HTML/DOM it was given, or make its own HTTP request
               (it may NOT read the database directly)
```

Rules that follow from this picture:

- A template cannot "reach into" the database. If the data is missing, the **route** was wrong.
- JavaScript cannot fix a server-side authorization hole, and must never be the only place a rule
  lives.
- Helpers may be called by many routes; routes should not call each other.
- If two routes need the same data, extract a helper instead of duplicating a query.

---

## 5. Recommended Project Structure

### 5.1 The layout

```text
project/
│
├── app.py                     (or application.py)  ← Flask app + routes
├── helpers.py                 ← shared logic: validation, auth guard, db access, reference utils
├── bible.py                   ← Bible data loading, indexing, lookup, search engine
│
├── data/
│   └── kjv.json               ← the Bible dataset (read-only, committed)
│
├── database/
│   ├── schema.sql             ← table definitions (committed)
│   └── bible_app.db           ← generated at runtime (NOT committed)
│
├── templates/
│   ├── layout.html            ← base template: head, nav, flash messages, footer
│   ├── index.html             ← books list
│   ├── book.html              ← chapters within a book  (optional page)
│   ├── chapter.html           ← the reader
│   ├── search.html            ← search form + results
│   ├── notes.html             ← "My Notes" overview
│   ├── login.html
│   ├── register.html
│   ├── 404.html
│   └── 500.html
│
├── static/
│   ├── css/styles.css         ← your own styling on top of Bootstrap
│   └── js/notes.js            ← note editor / verse-selection behaviour
│
├── tests/                     ← (optional) manual test notes, or pytest files
│   └── README.md
│
├── requirements.txt           ← pinned dependencies
├── .gitignore
├── .env                       ← local secrets (NOT committed)
├── README.md                  ← CS50 submission documentation
└── CS50X_BIBLE_APP_ROADMAP.md ← this document
```

The minimum acceptable version is `app.py` + `helpers.py` + `data/` + `database/schema.sql` +
`templates/` + `static/`. The structure above is already the *upper* limit for this project — do **not**
add `blueprints/`, `models/`, `services/`, or `api/` folders.

### 5.2 What belongs where (and what does not)

#### `app.py` — the entry point and route layer

- **Why it exists** — Flask needs a module that creates the application object and declares URL rules.
  It is also the file a grader opens first.
- **Belongs** — App configuration (secret key source, database path, debug flag from environment),
  view functions grouped by feature with comments, error handlers, and the
  `if __name__ == "__main__":` block.
- **Does NOT belong** — Long validation rules, the search algorithm, SQL strings scattered everywhere,
  inline password hashing, Bible JSON parsing.
- **Rule of thumb** — If a view function is longer than roughly 15–25 lines of readable logic, part of
  it belongs in `helpers.py`.
- **Group your routes** in this order and comment the sections:
  Reading (index / book / chapter) → Search → Authentication → Notes → Errors.
- **Decide** — `app.py` or `application.py`? Either works. Pick one and use it consistently in your
  README and run instructions.

#### `helpers.py` — everything reusable

- **Why it exists** — So logic is written once, fixed once. This is where "real engineering" shows up
  in a small project.
- **Belongs** — Input validation functions, the login-required guard, DB connection and query
  functions, reference parsing/formatting, the note ownership check.
- **Does NOT belong** — Anything that returns HTML, anything that depends on a specific URL, or
  module-level code with side effects (use functions).
- **Decide** — Use the CS50 library's `SQL()` helper (importable in your environment) or raw `sqlite3`?
  Either is acceptable. Whichever you choose, keep **all** DB access inside a few functions here, so the
  choice is reversible and you can explain the trade-off in your video.

#### `bible.py` — the Bible domain

- **Why it exists** — The Bible is your domain data. Isolating it means `app.py` never needs to know
  what the JSON looks like.
- **Belongs** — Loading the dataset, validating its structure, building indexes (books, chapter counts,
  canonical ordering, verse lookups, a precomputed lowercase search corpus), lookup functions, and the
  search function.
- **Does NOT belong** — Flask imports, `request`, templates, database access. This module should be
  usable from a plain Python script — which is a great way to test it before the web layer exists.
- **Why it matters for your grade** — This file is where you demonstrate *algorithmic thinking*: why a
  linear scan is acceptable at this size, how your index makes navigation instant, what you trade in
  memory for speed.

---

#### `data/kjv.json` — the dataset

- **Why it exists** — It is your content.
- **Belongs** — Bible text and structure only.
- **Does NOT belong** — User-specific data, runtime mutations, secrets.

#### `database/schema.sql` — the schema

- **Why it exists** — So the database is *reproducible*: delete the `.db` file, run the schema, and you
  are back to a clean state. It is also the clearest documentation of your design.
- **Belongs** — Table definitions, keys, constraints, indexes, and optionally a small amount of seed
  data.
- **Does NOT belong** — Routine application queries (those live in helpers/route code). `schema.sql` is
  *structure*, not data access.
- **Trap** — Do not put the Bible in here. See §7.

#### `database/bible_app.db` — the live database

- **Why it exists** — It is what SQLite actually reads from and writes to.
- **Belongs** — Users and notes.
- **Does NOT belong** — In Git. Add it to `.gitignore`.

#### `templates/` — presentation

- **Why it exists** — Jinja keeps HTML out of your Python.
- **Belongs** — `layout.html` with blocks for title/content; one template per page; small partial
  templates for reused pieces (a verse row, a note card, a flash-message block).
- **Does NOT belong** — SQL, database connections, password checks, "is this user allowed" decisions,
  or long Python expressions. Templates may *format* and *branch*; they must not *decide security* or
  *fetch data*.

#### `static/` — assets

- **Belongs** — CSS, JS, icons, a favicon.
- **Does NOT belong** — User data, templates, generated files, the dataset.

#### `.env` / configuration

- **Why it exists** — The secret key and database path differ between your laptop and a deployed
  server. Keeping them out of source code means you never leak a secret in your repo.
- **Belongs** — `SECRET_KEY`, database path, debug flag.
- **Does NOT belong** — Committed to Git. Ever.

### 5.3 Naming decisions to make now (and not change later)

| Thing | Your choice | Why it must be stable |
| --- | --- | --- |
| Book identifier in URLs | e.g. `genesis`, `1-corinthians`, or `Gen` | It appears in links, notes, and your README |
| Note reference format | e.g. `John 3:16` | It appears in the notes list and in search results |
| DB column names | e.g. `note_id`, `user_id`, `body` | They appear in every query you write |
| Template variable names | e.g. `books`, `verses`, `notes` | A mismatch here is the #1 source of blank pages |

Write your four decisions at the top of `helpers.py` (or the README) as comments before coding.

**Checkpoint 5** — Point at any file above and explain in one sentence why it exists and what would
break if it disappeared. If you cannot, merge it away or re-read §4.

---

## 6. Database Design

### 6.1 What goes in the database (and what does not)

| Candidate | In SQLite? | Reasoning |
| --- | --- | --- |
| Users (accounts) | **Yes** | Must persist, must be queryable, must be unique |
| Notes | **Yes** | User-generated, mutable, must be tied to an owner |
| Bible books/chapters/verses | **No** | Read-only, never queried relationally, already in `kjv.json`. Putting it in SQLite would add ~31k rows of import code and zero new capability |
| Reading position (O4) | Optional | Only if you build O4; it is per-user state |
| Sessions | **No** | Flask's signed cookie session is sufficient and is what CS50 teaches |

You need exactly **two required tables**. Resist adding a third "because it looks professional".

### 6.2 Relationship diagram

```text
┌───────────────────────────┐                 ┌───────────────────────────────┐
│           users           │                 │             notes             │
├───────────────────────────┤                 ├───────────────────────────────┤
│ user_id       INTEGER  PK │                 │ note_id       INTEGER  PK     │
│ username      TEXT   UNIQ │────────────<    │ user_id       INTEGER  FK ────┤→ users.user_id
│ password_hash TEXT        │   1 user         │ book          TEXT  NOT NULL  │
│ created_at    TEXT        │   owns many      │ chapter       INTEGER NOT NULL│
└───────────────────────────┘   notes          │ verse         INTEGER NOT NULL│
                                               │ body          TEXT  NOT NULL  │
                                               │ created_at    TEXT            │
                                               │ updated_at    TEXT            │
                                               └───────────────────────────────┘
                                                    ▲ UNIQUE (user_id, book, chapter, verse)
```

Read the diagram as: **one** user has **zero or many** notes; **each** note belongs to **exactly one**
user. A note with no user is meaningless, which is why the foreign key is non-nullable.

### 6.3 `users`

| Column | Conceptual type | Rules | Why it exists |
| --- | --- | --- | --- |
| `user_id` | integer, auto-incrementing | PRIMARY KEY, never reused | Stable internal identity for the session and for foreign keys. Never expose it in URLs unless you can authorize it |
| `username` | short text | NOT NULL, UNIQUE, case-insensitive uniqueness recommended, trimmed, length-limited | What the human types to log in. Uniqueness is a schema-level guarantee, not just a Python check |
| `password_hash` | long text | NOT NULL | **Only** the hash. A hash is longer than the password and looks like random characters |
| `created_at` | text/timestamp | NOT NULL, defaults to now | Useful for debugging and for your own credibility ("accounts are real records") |

Design questions you must answer for yourself:

- Is `alice` the same user as `Alice`? (Decide, then enforce it in the schema **and** in validation.)
- What is the maximum username length? Minimum? Which characters are allowed?
- What is the minimum password length? (Recommendation: 8+.)
- Do you allow deleting accounts? (Recommendation: no. Out of scope.)

### 6.4 `notes`

| Column | Conceptual type | Rules | Why it exists |
| --- | --- | --- | --- |
| `note_id` | integer, auto-incrementing | PRIMARY KEY | Identifies one note for edit/delete |
| `user_id` | integer | NOT NULL, FOREIGN KEY → `users.user_id` | **This is the authorization column.** Every query filters on it |
| `book` | text | NOT NULL | Which book the note is attached to (same identifier you use in URLs) |
| `chapter` | integer | NOT NULL, > 0 | Which chapter |
| `verse` | integer | NOT NULL, > 0 | Which verse |
| `body` | text | NOT NULL, trimmed length > 0, maximum length enforced | The user's note |
| `created_at` | timestamp | NOT NULL | When it was written |
| `updated_at` | timestamp | NOT NULL | When it was last edited; displayed in the UI |

Design questions you must answer:

- **One note per verse per user, or many?** If one, add a UNIQUE constraint across
  (user_id, book, chapter, verse) and let the database reject duplicates. Then decide whether a second
  save *replaces* or *errors*.
- Should `updated_at` be set by your Python code or by the database default? If the database supplies
  it, is it UTC? (It is.) Will that be visible to the user, and does it matter?
- Should the note body allow newlines? Markdown? (Recommendation: plain text with line breaks
  preserved and HTML escaped — no Markdown, no rich text.)
- Are there length limits? Pick numbers (e.g. 2000 characters) and enforce them **both** in validation
  and as a database constraint so the rule cannot be bypassed.

### 6.5 Indexes and constraints (why they exist)

| Mechanism | Purpose | Cost |
| --- | --- | --- |
| PRIMARY KEY on ids | Fast row lookup, guaranteed identity | None worth worrying about |
| UNIQUE on `username` | Prevents duplicate accounts even under a race | Tiny insert cost |
| FOREIGN KEY | Prevents orphan notes; documents the relationship | Requires foreign keys to be enabled in SQLite (see **Trap**) |
| UNIQUE (user_id, book, chapter, verse) | Enforces your one-note-per-verse decision | Tiny insert cost |
| Index on `user_id` | Makes "give me this user's notes" fast | Small write cost |

**Trap** — SQLite accepts foreign key *declarations* even when enforcement is switched off, and
enforcement is **off by default**. You must explicitly ask for it on every connection, and you must
verify it works: try to insert a note with a user id that does not exist. It should fail. If it
succeeds, your protection is decorative.

**Trap** — `AUTOINCREMENT` (as opposed to `INTEGER PRIMARY KEY`) is not needed in SQLite; and ids are
reused after deletion only if you do not use it. Decide whether you care, and know the difference.

---

### 6.6 The SQL operations you will eventually need

Do not write these yet. This is your *query inventory* — the complete list of ways your application
will touch the database. If a query you write is not on this list, ask yourself why.

#### Registration (write access to users)

| Operation | Shape of the need | Points of care |
| --- | --- | --- |
| Check whether a username exists | Filter `users` by username (case-insensitive if you decided that) | Do this for a friendly error message, but still catch the UNIQUE violation as the real guarantee |
| Insert a user | Add username + hash + timestamp | Never pass the raw password; never build the statement as a string |
| Read the new user's id | Either from the insert result or by selecting by username | You will want it if you log them in immediately |

#### Login

| Operation | Shape of the need | Points of care |
| --- | --- | --- |
| Look up a user by username | Select the id, username, and password hash | Handle "no row" without an exception; return the same error message as a wrong password |
| Verify the password | Not SQL — compare with a hashing helper | The comparison must be constant-time-ish via the helper, not a `==` on hashes you implement yourself |

#### Reading notes in the reader

| Operation | Shape of the need | Points of care |
| --- | --- | --- |
| Fetch this user's notes for one chapter | Filter by `user_id`, `book`, and `chapter` | Order by verse so the display is stable; returns zero or more rows |
| Convert the list of rows into a lookup the template can use | Python work, not SQL | Keying by verse number avoids an inner loop in the template |

#### My Notes page

| Operation | Shape of the need | Points of care |
| --- | --- | --- |
| Fetch all notes for this user | Filter by `user_id`, ordered (most recent first, or canonical if you add ordering support) | This query without the `user_id` filter is the classic data leak |
| Count notes (optional) | Aggregate count for the same filter | Nice for an empty-state message |

#### Create / Edit / Delete a note

| Operation | Shape of the need | Points of care |
| --- | --- | --- |
| Insert a note | user_id + reference + body + timestamps | The reference must have been validated against the Bible data first |
| Fetch one note **for the current user** | Filter by note id **and** user id | Combined filter means a foreign note simply "does not exist" for you |
| Update a note body | Update where note id **and** user id match; set updated timestamp | Check how many rows changed to distinguish success from "not yours" |
| Delete a note | Delete where note id **and** user id match | Same row-count check |

#### Join practice (worth one deliberate use)

A `JOIN` is not strictly necessary here, because you always know the current user's id from the session.
But CS50 expects you to understand joins, and there is one honest use case: an "owner" column on the
notes page in a hypothetical multi-user view, or joining `users` → `notes` to count notes per user for
your own debugging. Write **one** join query during development, understand it, and be ready to explain
why your application itself does not need it. Do not invent a feature just to use a join — but do not
skip understanding joins either.

#### Filtering, ordering, validation recap

- **Filtering** — ALWAYS filter user-owned rows by the session user's id.
- **Ordering** — Results must have a deterministic order, otherwise your chapter's verses and your notes
  list will appear to shuffle between requests. Chapter verses come from JSON (already ordered); notes
  need an explicit `ORDER BY`.
- **Limiting** — Any list that can grow (notes, search results) needs a cap or pagination decision.
- **Validation** — The database enforces *structure and integrity* (types, uniqueness, non-null,
  foreign keys). Python enforces *business rules and messages* (trimmed non-empty text, length, allowed
  characters). You need both; neither replaces the other.

### 6.7 How to inspect your database yourself

You must be able to open the database and see the truth without going through your application:

- The SQLite command line: `sqlite3 database/bible_app.db` then `.tables`, `.schema notes`,
  `SELECT * FROM users;`, `SELECT * FROM notes;` (use `.quit` to exit).
- Check that foreign keys are enforced: `PRAGMA foreign_keys;` on a fresh connection should report on.
- Verify your application writes what you think it writes, and that the *hash* — not the password — is
  in the `password_hash` column.
- Delete the `.db` file and recreate it from the schema. If your app cannot start from an empty
  database, your setup is not reproducible and deployment will fail.

**Checkpoint 6.1** — Can you explain, without looking, why `notes.user_id` is the most important column
in the entire schema?
**Checkpoint 6.2** — Can you explain what a FOREIGN KEY *physically* prevents, and what it does not?
(It prevents a note referencing a nonexistent user. It does **not** stop one user from reading another
user's note — only your `WHERE` clause does that.)

---

## 7. Bible Data Architecture

### 7.1 First, answer this: where does the KJV text come from?

You said you already have the data as JSON. Two legal notes worth knowing before you publish a repo:

- The **King James Version text is in the public domain in the United States** (some other countries,
  notably the UK, restrict it under Crown copyright). For a CS50 project the US position is what
  matters, but cite the source in your README out of good practice.
- Record **where the file came from** and keep the original untouched. Never hand-edit verse text — if
  you "fix a typo", you have corrupted your dataset and silently broken search for that word.

### 7.2 Choosing the JSON shape

You must pick one structure and commit to it. The two realistic options:

**Option A — nested (natural reading order)**

```text
[
  { "book": "Genesis", "chapters": [ { "chapter": 1, "verses": [ {"verse": 1, "text": "..."}, ... ] },
                                     { "chapter": 2, "verses": [ ... ] } ] },
  { "book": "Exodus",  "chapters": [ ... ] },
  ...
]
```

**Option B — flat list of verse records**

```text
[ { "book": "Genesis", "chapter": 1, "verse": 1, "text": "In the beginning..." },
  { "book": "Genesis", "chapter": 1, "verse": 2, "text": "..." },
  ...
]
```

| Criterion | Nested | Flat |
| --- | --- | --- |
| Human readability | Good | Verbose |
| "All verses of a chapter" | Direct | Requires filtering |
| Easy to search | Requires flattening first | Direct iteration |
| Chapter count for a book | Direct (`len(chapters)`) | Must be computed or hard-coded |
| Risk of losing canonical order | Low (order is structural) | Higher (you must preserve file order) |

**Decide** — Pick one. Then build **one** in-memory index in `bible.py` that gives you the best of both
worlds, so the rest of your code never touches the raw shape:

```text
What you want at the end of the load step:

  ordered_books           → ["Genesis", "Exodus", ..., "Revelation"]      (canonical order)
  book_meta[slug]         → { "display": "Genesis", "chapters": 50, "testament": "OT" }
  chapters[slug][1]       → [ (verse_number, text), (verse_number, text), ... ]
  verse_index[(slug, ch, v)] → text        (direct lookup; also used for note display/links)
  search_corpus           → precomputed normalized text for fast, robust matching
  book_alias[...]         → optional: forgiving input like "1 Cor" → 1 Corinthians
```

**Checkpoint 7.1** — Can you explain why `verse_index` is a dictionary rather than a list?

**Checkpoint 7.2** — What happens to your memory footprint when you hold the raw JSON *and* the indexes?
(The KJV is roughly 31,100 verses and ~4–5 MB of JSON. Two or three derived structures is fine on a
laptop; be aware that "clone the whole text again per request" is not.)

### 7.3 Identifying books, chapters and verses

This decision follows you into your URLs, your notes table, and your README:

| Approach | Example | Pros | Cons |
| --- | --- | --- | --- |
| Display name in the URL | `/Genesis/1` | Human readable; self-documenting | Case, spaces and numbering make matching fragile ("1 Corinthians" vs "1Corinthians"); percent-encoding in links |
| Slug | `/genesis/1`, `/1-corinthians/3` | Stable, URL-safe, readable, easy to match | You must generate and store the mapping |
| Numeric id | `/book/1/1` | Trivially robust | Opaque; hides a positional assumption |
| Array position | index into the books list | Fast | **Do not.** If file order ever changes, every stored note silently points at the wrong book |

**Recommendation** — use a **slug** as the canonical identifier everywhere (URLs and `notes.book`), and
keep a display name in the index for the UI. Then:

- Write down a deterministic slug rule (lowercase, spaces → hyphens, punctuation removed) and implement
  it in exactly one function that converts slug ⇄ display name.
- Numbered books need extra care (`1`, `2`, `3`, and "Song of Solomon").
- Add a pass over the dataset that asserts "every slug is unique" — do this once, at load time.

### 7.4 Verse numbering and the off-by-one trap

- Verse numbers start at **1**, chapter numbers start at **1**: user-facing references are **one-based**.
- Python lists and many URL indices are **zero-based**. Mixing these is the most likely bug in a Bible
  app. Pick a rule (e.g. "all user-facing numbers are one-based; conversion happens only inside lookup
  functions") and write it down.
- Chapters have different verse counts. Never hard-code "chapter 1 has 31 verses" — always read the
  count from the data.
- Chapters per book range from 1 (Obadiah, Philemon, 2 John, 3 John, Jude) to 150 (Psalms). Test your
  "next chapter" logic against a single-chapter book.

---

### 7.5 How Flask should access the data

```text
app start
   │
   └─► load kjv.json ONCE ──► validate structure ──► build indexes ──► keep in module-level memory
                                                                             │
every request ──► route asks bible.py for what it needs (slug + numbers) ────┘
                     │
                     └─► returns plain Python data ──► route ──► template
```

| Strategy | When it is right | Risk |
| --- | --- | --- |
| Load at import time into module globals | This project | An import error kills the app at start-up — which is actually *good*, because it fails loudly |
| Load lazily on first request, then cache | If start-up speed mattered | First request is slow; more code |
| Re-read and re-parse the file on every request | **Never** | Re-parsing 4 MB per page will feel broken |
| Put the text into SQLite | **No** (§6.1) | Adds import complexity and gains nothing for a read-only dataset |

Note on Flask 3.x: there is **no** `before_first_request` hook any more (removed in Flask 2.3). If you
want an explicit initialisation step, do it at module level, in an app factory, or as a small one-off
script that creates the database from `schema.sql`. Do not invent workarounds for a hook that no longer
exists.

### 7.6 How the application locates a specific verse

Two lookups happen in different directions, and you need both:

1. **Navigation** (the user asks for a chapter): slug + chapter → validate the book exists → validate
   the chapter is within that book's chapter count → return the chapter's verses.
2. **References from elsewhere** (a note, or a search result): slug + chapter + verse → validate → build
   a link and a short excerpt.

A verse lookup should be a dictionary lookup, not a scan. `verse_index[(slug, chapter, verse)]` is
O(1)-ish; scanning all ~31,100 verses for each stored note is O(n) per note, and O(n·m) for a chapter's
notes.

### 7.7 How search should work, conceptually

```text
query string
   │
   ├─► normalize : trim, collapse repeated whitespace, settle case handling (case-insensitive?)
   ├─► validate  : non-empty, not absurdly long, reject/handle odd characters
   │
   ├─► match     : for each verse, does its normalized text contain the normalized query?
   │                 └─► decide: substring? whole-word? phrase?
   │
   ├─► collect   : reference + text (+ optionally a snippet centred on the match)
   │
   └─► order/cap : canonical order, or "most matches first"; cap the count or paginate
```

Decisions you must make and be able to justify:

| Decision | Options | Consequence |
| --- | --- | --- |
| Normalization | lowercase only; lowercase + strip punctuation; `casefold` | Affects whether "LORD's" matches "lord's" and "LORD" |
| Match type | substring (finds "love" inside "loved"); whole word (misses "loved"); phrase (multi-word) | Determines result quality; explain your choice in the video |
| Multi-word queries | one phrase; ALL words present (AND); ANY word present (OR) | AND/OR is a small, defensible algorithm — and a great thing to explain |
| Result cap | everything; cap at N; paginate | "the" appears tens of thousands of times; an uncapped page is a performance and UX problem |
| Order | canonical; grouped by book; relevance | Must be deterministic; be ready to justify it |
| Performance | naive scan over a precomputed normalized corpus; inverted index (word → verse ids); SQLite FTS5 | A linear scan over ~31k short strings is fast enough for one user. An inverted index is a genuine "algorithmic thinking" upgrade. FTS5 is a stretch goal requiring justification |

**Trap** — Building the normalized corpus *inside* the search function re-normalizes 31k verses on every
search. Precompute it once, then measure the difference.

**Trap** — Never render the raw query into HTML with escaping disabled. Jinja escapes by default; do not
defeat it with `|safe`.

**Checkpoint 7.3** — In one sentence each: (a) why search does not touch SQLite; (b) what your
normalization rules are; (c) whether your match is substring or whole-word, and how a user would notice
the difference.

---

## 8. Development Roadmap

### How to use this section — the phase gate rule

```text
Phase N ──► Tasks ──► Testing checklist ──► Completion criteria ALL met? ──► Phase N+1
                                                      │
                                                      └── NO ──► stay in Phase N.
                                                          Do not "come back to it later".
```

Each phase below has: **Objective · Concepts to Learn · Prerequisites · Tasks · Implementation
Guidance · Questions You Should Be Able to Answer · Testing Checklist · Completion Criteria · Common
Problems.**

---

### Phase 0 — Planning and Design

**Objective** — Turn this document into *your* project: decide the open questions, write your schema and
route plan on paper, and set up a working environment. No features are built in this phase.

**Concepts to Learn**
- The request/response cycle (CS50 Week 9 lecture, "Web Programming").
- What a route is; what a template is; what a session is.
- Idempotency and safe methods (GET vs POST) — enough to decide which routes are which.
- One-based vs zero-based indexing.
- What a "design decision" is: a choice you can defend, not a default you inherited.

**Prerequisites** — None beyond this document. Python and Flask are already installed on your machine.

**Tasks**
- [ ] Create the repository and the folder skeleton from §5.1 (empty files are fine).
- [ ] Create and activate a virtual environment; install Flask; freeze `requirements.txt`.
- [ ] Write `.gitignore` (§15) **before** the first commit.
- [ ] Write a first commit that contains only the skeleton + README stub + this roadmap.
- [ ] Make the four naming decisions from §5.3 and record them (in the README or as comments).
- [ ] Make the data-shape decision from §7.2 and the book-identifier decision from §7.3.
- [ ] Make the "one note per verse per user?" decision from §6.4 (F7).
- [ ] Draw, by hand or in a text file, your route plan: URL pattern → what it renders → GET or POST →
      login required yes/no. (Use the table in §3.7 as your starting point.)
- [ ] Write your schema plan as a list of tables/columns/constraints (§6) — *plan*, not SQL file yet.
- [ ] List your 12 required features and put them in the order you will build them (§8 phases).
- [ ] Choose your CSS approach: Bootstrap via CDN, Bootstrap downloaded locally, or plain CSS you write.
      Write down *why*.
- [ ] Decide where Bible JSON comes from and where you will store it (`data/kjv.json`), and note the
      licence/source in the README.

**Implementation Guidance** — This phase produces **documents, not code**. The most valuable artefact is
the route plan: if you can describe every URL your app will have, you have designed the application.
Keep the plan short (one page). Then walk away and check: does every required feature (F1–F12) have a
route or a piece of a route that delivers it? If a feature has no home in your route plan, it will not
get built.

**Questions You Should Be Able to Answer**
1. What are the exact URLs your application will have, and why each one is GET or POST?
2. Where does each required feature live?
3. What does a "note" row contain, and which column makes notes private?
4. Why is Bible text not in the database?
5. What are you deliberately not building (§18)?

**Testing Checklist**
- [ ] Run `python --version`, `python -c "import flask"` and confirm both work *inside* the venv.
- [ ] `git log` shows exactly one clean initial commit and `git status` is clean.
- [ ] `git status` does **not** list `.venv/`, `.env`, or any `.db` file.
- [ ] Your route plan covers all of F1–F12.

**Completion Criteria**
- [ ] Folder skeleton exists and is committed.
- [ ] Virtual environment works; `requirements.txt` exists.
- [ ] Every open **Decide** in §5, §6 and §7 has a written answer.
- [ ] Route plan exists and maps every required feature.
- [ ] You can explain your plan out loud for two minutes without reading it.

**Common Problems**
- *Planning forever.* If Phase 0 takes more than a day, you are over-designing. Two pages maximum.
- *No `.gitignore` at the start* → you commit your virtual environment (thousands of files) and your
  secret key. Fixing that later is painful.
- *Committing to a URL scheme you later hate.* That is fine — that is what Phase 3 is for. Just do not
  change it after Phase 6.

**Gate** — Do not write feature code until your route plan exists.

---

### Phase 1 — Project Setup (a running Flask skeleton)

**Objective** — A Flask application that starts, serves one page, and can grow. Nothing else.

**Concepts to Learn**
- How a Flask application object is created and how the development server starts.
- URL rules and view functions; how Flask matches a request to a function.
- `render_template`, `redirect`, `url_for`, `request`, and the difference between a rendered response
  and a redirect.
- Jinja template inheritance: how a `layout.html` with blocks saves you from repeating HTML.
- Environment variables vs hard-coded configuration; why a secret key exists at all.

**Prerequisites** — Phase 0 complete.

**Tasks**
- [ ] Create your empty skeleton per §5.1.
- [ ] Create and activate the virtual environment; install Flask; write `requirements.txt`.
- [ ] Write `.gitignore` and a one-paragraph `README.md`.
- [ ] Create the Flask app object and one placeholder route that renders a placeholder page.
- [ ] Create `templates/layout.html` with the page chrome and at least one Jinja `block` for content.
- [ ] Create the first real page (`index.html`) that extends the layout.
- [ ] Wire up static files: a `styles.css` linked through `url_for` and one Bootstrap include (CDN is
      fine) — confirm the styles actually apply.
- [ ] Add a development-only debug flag driven by an environment variable, not hard-coded.
- [ ] Run the app and fix every warning it prints.
- [ ] Commit.

**Implementation Guidance** — Keep this phase boring on purpose. Your goal is a *thin vertical slice*:
browser → Flask → template → browser. Verify it works before adding anything. Notice where Flask prints
the local URL, and notice what the terminal shows for each request (method, path, status code) — that
log line is your primary debugging tool for the rest of the project.

Decide and record: how you will start the app (e.g. `flask --app app run --debug` versus running the
module directly). Then use that exact command in your README, because your grader will copy it.

**Questions You Should Be Able to Answer**
1. What happens, step by step, between typing a URL and seeing HTML?
2. What does Jinja inheritance buy you, and where does the browser get the CSS file from?
3. Why does the app need a secret key, and what breaks without one?
4. Why is `debug=True` unacceptable in a deployed application?

**Testing Checklist**
- [ ] The app starts with no errors and no warnings you ignored.
- [ ] The placeholder page loads at the expected URL and returns HTTP 200.
- [ ] CSS changes are visible after a refresh (or a hard refresh).
- [ ] Deliberately break a template (e.g. rename a block) and confirm the error message points you to
      the right file and line, then fix it.
- [ ] Deliberately break a route (e.g. typo a decorator) and read the traceback before fixing it.

**Completion Criteria**
- [ ] App starts, one page renders inside the shared layout, CSS applies.
- [ ] Configuration comes from the environment; no secrets in source.
- [ ] `.gitignore` correct; repo committed and clean.
- [ ] You can name the file where a request "lands" and the file that renders the response.

**Common Problems**
- **Trap (Flask 3.x):** copying a tutorial that uses `@app.before_first_request` — removed in Flask 2.3.
  Initialise at import time or in an app factory instead.
- **Trap (Windows):** activating the environment with the Unix path (`.venv/bin/activate`) fails. Use
  `.venv\Scripts\activate` (PowerShell: `.venv\Scripts\Activate.ps1`).
- *Template not found* — Flask looks for `templates/` next to the app module. If your `app.py` lives
  elsewhere, the default lookup is wrong.
- *Static file 404* — you must link assets via `url_for('static', filename=...)`, not a hard-coded
  path, or the URL changes once you deploy.
- *Port already in use* — an earlier server is still running in another terminal. Find it, or run on a
  different port while developing.

**Checkpoint 1** — Can you explain how a Flask request reaches a route, and how Jinja receives data from
that route? If not, re-read §4.4 before continuing.

---

### Phase 2 — Bible Data Layer

**Objective** — Turn `data/kjv.json` into a trusted, indexed, in-memory API (`bible.py`) that the web
layer can rely on. **No web pages yet.**

**Concepts to Learn**
- File I/O and JSON parsing (`json.load`), and what happens when the file is malformed.
- Data-structure choice: lists for order, dicts for lookup; why a dict keyed by a tuple beats nested
  loops.
- Normalization for comparison: case, whitespace, punctuation.
- Defensive programming: validating assumptions about your own data file.
- Writing and running a plain Python test script (CS50 "unit test" thinking).

**Prerequisites** — Phase 1 skeleton committed. The JSON file present in `data/`.

**Tasks**
- [ ] Inspect the JSON first: print its top-level type, count the books, and print the structure of one
      book and one chapter. **Understand it before writing any parser.**
- [ ] Write a small standalone script that loads the file and answers: how many books, how many
      chapters in the last book, how many verses in Genesis 1, and the text of John 3:16.
- [ ] Convert that script into functions inside `bible.py` (loading, indexing, lookups).
- [ ] Build the indexes listed in §7.2: ordered book list, per-book metadata (display name, chapter
      count), the chapter map, the verse lookup, and the normalized search corpus.
- [ ] Add the slug ⇄ display-name conversion function (§7.3) and assert all slugs are unique.
- [ ] Add a structural validation step that fails loudly with a useful message if the file is not what
      you expect (missing keys, empty books, duplicate slugs).
- [ ] Write lookup functions that accept a slug and numbers and return clean data, and that signal
      "not found" in a way your future routes can detect (e.g. return nothing / raise a specific error —
      decide which and be consistent).
- [ ] Write a search function per §7.7, returning references plus text, with a cap.
- [ ] Time the load step and time a search. Record the numbers in your notes.
- [ ] Commit.

**Implementation Guidance** — This is the phase where you demonstrate algorithmic thinking, so *measure*
things: how long does loading take, how long does one search take, how big is the structure in memory?
Those numbers are excellent material for your presentation video. Also make the module usable without
Flask: if you can `import bible` in a plain script and use it, your separation is correct. Keep the raw
JSON untouched after loading (treat it as immutable) so a search bug cannot corrupt your reading data.

**Questions You Should Be Able to Answer**
1. What exactly does your load step produce, in memory? Describe each structure and its purpose.
2. Why is a verse lookup a dict lookup instead of a scan? What is the lookup cost?
3. What does your code do if the JSON is missing a book or has a chapter with zero verses?
4. How do you convert "1 Corinthians" into the slug you use in URLs? Where is that rule written down?
5. Substring or whole-word matching? Why? What does the user gain and lose?
6. What is your result cap and why that number?

**Testing Checklist**
- [ ] Total book count is 66 and canonical order is correct (Genesis first, Revelation last).
- [ ] Genesis 1 verse 1 text is correct; Revelation 22's last verse text is correct.
- [ ] A single-chapter book (e.g. Jude) reports a chapter count of 1 and its verses are retrievable.
- [ ] Psalm 119 returns 176 verses.
- [ ] Verse numbers begin at 1 and are contiguous within every chapter (write a loop that checks this
      across the whole dataset — a data-integrity test).
- [ ] `John 3:16` resolves; `John 3:99` and `Genesis 60` do **not** resolve, and do not raise an
      unhandled exception that you cannot interpret.
- [ ] A search for a word you know exists returns it; a search for "zzzzqq" returns an empty result.
- [ ] Search is case-insensitive for a word you know appears both ways.
- [ ] Load time and search time measured and recorded.

**Completion Criteria**
- [ ] `bible.py` works standalone, with no Flask imports.
- [ ] All checklist items pass.
- [ ] You have recorded load/search timings.
- [ ] No hard-coded verse counts or chapter counts anywhere in your code.

**Common Problems**
- *Guessing the JSON keys* — always print the structure first. A `KeyError` in a 4 MB file with a vague
  message wastes an hour.
- *Re-parsing the file per lookup* — check that your load happens once by printing inside the load
  function and confirming you only see it once.
- *Off-by-one on verse numbers* — verses are 1-based; write the data-integrity loop above to catch it.
- *Normalizing inside the search loop* — precompute; measure.
- *Encoding problems* — open the file explicitly as UTF-8 so apostrophes ("LORD's") never become
  mojibake.

**Checkpoint 2** — Can you explain how your search finds matching verses, from the query string to the
result list, including normalization and any cap? If not, do not start Phase 3.

---

### Phase 3 — Bible Reader (F1, F2, F3, F12 partial)

**Objective** — A working, browsable Bible: books list → chapter reader → navigation, with graceful
handling of invalid references.

**Concepts to Learn**
- Dynamic URL rules with variables (path parameters) and how Flask passes them to your function.
- Type conversion in URLs vs validating strings yourself.
- Jinja: `{% for %}`, `{{ }}`, conditionals, and automatic HTML escaping.
- Passing a context to `render_template` — and the mental link between route variables and template
  variable names.
- HTTP status codes: 200, 302, 404 and when each is appropriate.
- Returning a "not found" response instead of crashing.

**Prerequisites** — Phase 2's `bible.py` fully passing its checklist.

**Tasks**
- [ ] Build the books list page from the index (F1).
- [ ] Build the chapter reader route: accept a book slug and a chapter number, validate, render verses
      (F2).
- [ ] Display the current reference clearly ("Genesis 1") and label each verse with its number.
- [ ] Add a stable, unique identifier per verse in the rendered HTML (e.g. an id attribute) so later
      phases and JavaScript can target a specific verse. Decide the format now.
- [ ] Add Previous/Next chapter navigation, computed from the data, including across book boundaries
      (F3).
- [ ] Add a way to choose another chapter of the current book (F3) that reflects the real chapter count.
- [ ] Add a way to get back to the books list from every reading page.
- [ ] Handle invalid book slug and invalid chapter number with a friendly 404 page and correct status
      code (F12 partial).
- [ ] Add a global 404 handler for unknown URLs.
- [ ] Add one reusable partial template if you find yourself repeating the verse markup.
- [ ] Commit.

**Implementation Guidance** — Think about the *reference* as a first-class object in your code: a book
slug, a chapter, and optionally a verse. Write helper functions that validate a reference and format it
for display, then use them in every route. This is what makes Phase 6 (notes) easy instead of messy.
For navigation, compute neighbours in Python (previous/next chapter exist? or is this the end of a book?)
and pass the answer to the template, so the template never has to reason about boundaries.

**Questions You Should Be Able to Answer**
1. What are the exact URL patterns for the reader, and what makes a book slug valid?
2. How does the template learn which verses to display, and why can't it fetch them itself?
3. Which numbers in the URL are one-based, and where do you convert?
4. What happens if a user edits the URL to `/genesis/999`? Trace it through your code.
5. Why is a 404 more correct than a 200 page that says "not found"?

**Testing Checklist**
- [ ] Genesis 1 renders the full chapter with correct verse numbers.
- [ ] Revelation 22 renders; the last verse is present.
- [ ] A single-chapter book renders and its navigation does not offer an impossible chapter.
- [ ] Previous on the very first chapter is either absent or disabled — never a broken link.
- [ ] Next on the very last chapter is either absent or disabled.
- [ ] Next at the end of every book moves to chapter 1 of the next book; Previous at the start of every
      book moves to the last chapter of the previous book (test a few, and consider looping through all
      66 programmatically).
- [ ] The chapter picker offers exactly the right number of chapters for a 1-chapter, 50-chapter and
      150-chapter book.
- [ ] Invalid slug, invalid chapter, non-numeric chapter, and empty chapter value all give a friendly
      page with status 404 (verify the status in your terminal log or browser dev tools).
- [ ] View source: verse text containing apostrophes renders correctly and no HTML is injected.
- [ ] Page works with JavaScript disabled.

**Completion Criteria**
- [ ] Books list, chapter reader, and boundary-safe navigation all work for every book.
- [ ] Invalid references never produce a traceback.
- [ ] The page shows the user where they are and how to move.
- [ ] No database code exists yet (this phase is intentionally DB-free).

**Common Problems**
- *Passing the display name into the URL and failing on spaces* ("1 Corinthians" → `%201%20Corinthians`).
  Use slugs.
- *Off-by-one when slicing chapters* — remember user numbers are 1-based.
- *Hard-coding the chapter count* (e.g. assuming 50) instead of reading it from the index.
- *Blank page with no error* — almost always a template variable name mismatch. Check the name you
  passed to `render_template` against the name in the template, character by character.
- *Forgetting to escape* — never use `|safe` on any text that came from the dataset or a user.
- *Using the browser Back button as your "Previous chapter" feature* — graders notice.

**Checkpoint 3** — Can you explain, end to end, how the string "genesis" in a URL becomes a list of
verses in the HTML? If not, redo this phase's explanation before moving on.

---

### Phase 4 — Search (F4)

**Objective** — Search the whole KJV from the UI and navigate from results back into the reader.

**Concepts to Learn**
- Query string parameters vs form body: why search uses the URL (`?q=...`).
- Encoding of user input in URLs and why you must let the framework build your links.
- The distinction between validation (is this input acceptable?) and sanitization/escaping (is it safe
  to display?).
- Loop efficiency: precomputation, early exits, bounding result sets.
- Deterministic ordering of results.

**Prerequisites** — Phase 3 complete; `bible.py` search function already tested standalone.

**Tasks**
- [ ] Add a search form to the shared layout or to the reading pages, and a results page.
- [ ] Wire the form to a route that reads the query parameter and calls your search function.
- [ ] Handle the empty-query case: show the form with a message instead of returning the entire Bible.
- [ ] Handle the no-results case with a helpful message that echoes the query safely.
- [ ] Display each result with its full reference, the verse text, and a working link to the chapter
      (and ideally an anchor to the specific verse).
- [ ] Show the total number of matches, plus a note if results were capped, if you cap them.
- [ ] Keep the query visible in the input after searching.
- [ ] Add a limit/timeout guard: make sure a pathological query (very long, or a single letter) cannot
      make the page feel broken. Decide and implement your cap.
- [ ] Commit.

**Implementation Guidance** — Think about what a *good* result page looks like for a query like "the".
Returning 20,000 results is not a feature, it is a problem: decide what you do (cap with a message, or
group by book with counts) and be able to explain why. Also decide whether the match should be
highlighted in the result text — if you highlight, you must insert markup for the match **and** escape
the surrounding text; the safe way is to escape first, then insert your own markup around escaped
matches, and never wrap the raw text.

**Questions You Should Be Able to Answer**
1. Why is the query in the URL rather than in a form POST body?
2. What happens for a one-character query? For a 500-character query? For a query of only spaces?
3. How many verses are searched, how long does it take, and how did you measure that?
4. What is your result cap and what does the UI tell the user when the cap is hit?
5. If your search matched a verse containing `<script>`, what would appear on the results page?

**Testing Checklist**
- [ ] A very common word returns results without the page hanging.
- [ ] A word that appears once returns exactly that verse.
- [ ] `zzzzqq` returns the friendly empty state.
- [ ] Case variations ("Begat", "begat", "BEGAT") return the same results.
- [ ] A multi-word phrase behaves exactly as you documented in §7.7.
- [ ] Punctuation: apostrophes ("LORD's"), commas, quotes, ampersands.
- [ ] Leading/trailing spaces and multiple internal spaces are handled.
- [ ] Empty query → message, no crash, no full-Bible dump.
- [ ] Query containing HTML/JavaScript is displayed as text, never executed (inspect the page source).
- [ ] Every result link opens the right chapter, and (if animated) the right verse.
- [ ] Searching while logged in and while logged out works identically.
- [ ] Timings recorded for a common word and a rare word.

**Completion Criteria**
- [ ] All checklist items pass.
- [ ] Query normalization, match rules, and result cap are documented in your README/notes.
- [ ] Search never exposes raw user input as HTML.
- [ ] Result ordering is deterministic (repeat the same query twice; same order both times).

**Common Problems**
- *Recomputing the corpus per search* — measure before and after to see the difference.
- *Accidentally returning the whole text for an empty query* (because an empty string matches
  everything) — check for empty **before** searching.
- *Using `|safe` to highlight matches* — this reintroduces injection. Escape, then wrap.
- *Building result links by string concatenation* — let the URL builder handle encoding.
- *Non-deterministic ordering* because your index is a set/dict — sort by canonical order before
  slicing.

**Checkpoint 4** — Can you explain how a search query finds matching verses, including normalization,
matching rule, ordering, and cap? (This is the same question as Checkpoint 2 — if your answer changed
because of what you built, say so; that is fine.)

---

### Phase 5 — Database and Authentication (F5, F6)

**Objective** — A real database with real users, hashed passwords, working sessions, and a reusable
"login required" mechanism.

**Concepts to Learn**
- Relational schema basics: primary keys, uniqueness, `NOT NULL`.
- Why passwords are hashed and salted, and why hashing is deliberately slow.
- Sessions and cookies: what the cookie contains, why it must be signed, why the session must not hold
  secrets.
- The difference between authentication (who are you) and authorization (what may you do).
- SQL parameterization: why string-built SQL is a vulnerability, not a style choice.
- Executing a schema file to create a database from scratch (reproducibility).
- SQLite threading behaviour with a multi-threaded development server.

**Prerequisites** — Phase 1's configuration approach. Phases 2–4 are not required to start, but do not
begin notes (Phase 6) until this phase is fully done.

**Tasks**
- [ ] Write `database/schema.sql` implementing §6 (two tables, keys, constraints, indexes).
- [ ] Create the database from the schema file and confirm the tables exist (inspect with the `sqlite3`
      CLI, §6.7).
- [ ] Add DB configuration: path from the environment, plus a documented way to recreate the database.
- [ ] Add a DB connection helper used by everything (one place, one behaviour).
- [ ] Enable foreign key enforcement for every connection and prove it works with a deliberate bad
      insert.
- [ ] Build registration: GET form, POST handler, full validation, hashed password storage, friendly
      duplicate-username handling.
- [ ] Build login: verification against the stored hash, generic failure message, session set on success.
- [ ] Build logout: end the session fully and redirect somewhere sensible.
- [ ] Build the login-required guard (decorator or helper) and use it on at least one protected page.
- [ ] Update the navigation to reflect logged-in/out state.
- [ ] Add flash-style feedback messages for register/login/logout and display them in the layout.
- [ ] Commit.

**Implementation Guidance** — Write the schema first, then the *creation* step (drop-and-recreate must be
trivial), then the access functions, then the routes. Keep every credential check in one helper so "how
do we verify a password" has exactly one answer in your codebase. Store only the user's id (and maybe
username for display) in the session — never the password or its hash. Test the pipeline with the SQLite
CLI, not only through your app, so you can look at the actual rows and the actual hash.

**Decide** — CS50's `SQL()` helper vs raw `sqlite3`. The `cs50` package is importable in your
environment. Arguments for the helper: fewer lines, parameterization handled for you, familiar from CS50.
Arguments for raw `sqlite3`: no extra dependency, you learn `row_factory`, context managers, and
commit/rollback semantics, and it deploys anywhere. Either is fine for grading — but be able to explain
*why* you chose it, and keep all access behind your own helper functions so the decision stays one file
deep.

---

**Questions You Should Be Able to Answer**
1. Where does the cookie come from on the request that follows a successful login, and what is inside it?
2. Why must the password hash never be stored in the session or rendered in HTML?
3. How does SQLite physically store your users? Where is that file, and is it in Git?
4. Why does a unique constraint matter if Python already checks for duplicates?
5. Why is the login error message deliberately vague?
6. What exactly does "logged in" mean in your application? Which piece of data proves it?

**Testing Checklist**
- [ ] Registration with valid input creates exactly one row; the stored value is a hash, not the password.
- [ ] Duplicate username (exact, and different case per your decision) is rejected with a friendly error.
- [ ] Empty / mismatched / too-short password cases are each rejected with their own message.
- [ ] Login with the correct password works; a wrong password fails; an unknown username fails with the
      **same** message.
- [ ] After login the nav shows the user; after logout it does not.
- [ ] After logout, a protected page redirects to login (test by typing the URL directly).
- [ ] Closing and reopening the browser keeps or drops the session as you decided (document which).
- [ ] A bad insert with a nonexistent user id fails (proving foreign keys are enabled).
- [ ] Recreating the database from `schema.sql` works from scratch and the app still starts.
- [ ] SQL-injection attempts in the username field (a lone quote, or `' OR 1=1 --`) neither log you in
      nor break the app; verify with the CLI that any inserted value is literal text.

**Completion Criteria**
- [ ] Both tables exist and `schema.sql` is the single source of truth for structure.
- [ ] Registration, login, logout, and the login guard all work.
- [ ] Passwords are hashed; no plaintext anywhere (search your DB file for a known password string).
- [ ] All DB access goes through helpers using parameterized statements.
- [ ] The DB file is git-ignored, and the schema is committed.

**Common Problems**
- **Trap:** a `sqlite3` connection created in one thread and used in another raises "SQLite objects
  created in a thread can only be used in that same thread" once the dev server handles requests in
  parallel. Understand *why* it happens and fix it the principled way (per-request connection, or a
  correctly configured shared connection) rather than by disabling a check you do not understand.
- *Foreign keys silently off* — SQLite does not enforce them unless you ask, per connection.
- *A `NOT NULL` violation crashes instead of validating* — validate in Python first; the constraint is
  the safety net, not the user interface.
- *Storing the password because "it is just a project"* — the easiest way to lose points.
- *Reading `session` keys that were never set* — use `.get()`-style access, or visitors get 500s.
- *Forgetting to persist the write* — the insert appears to work in the same process and vanishes on
  restart. Verify with the CLI.

**Checkpoint 5** — Can you explain why passwords must be hashed, how SQLite stores your users, what a
session actually is, and how the login guard knows you are logged in? If any answer is fuzzy, stop here.

---

### Phase 6 — Notes (F7, F8, F9, F10, F11)

**Objective** — The feature that makes this a project rather than a viewer: private, per-verse notes
with full CRUD and correct ownership enforcement.

**Concepts to Learn**
- CRUD mapping: which HTTP methods and which SQL statements correspond to Create/Read/Update/Delete.
- Foreign keys in practice: linking a note row to a user row.
- Authorization vs authentication: the same route can be reachable by many users but must expose only
  one user's data.
- Data shaping: turning a list of note rows into a structure the template can use efficiently.
- `WHERE` clause discipline: an ownership filter belongs on **every** statement touching notes.
- Redirect-after-POST: why you redirect after a successful write instead of rendering.

**Prerequisites** — Phase 3 (reader + verse anchors) and Phase 5 (users + login guard) both complete,
plus the Phase 2 data-integrity tests passing so verses can be validated.

**Tasks**
- [ ] Add the notes access functions: fetch by user+chapter, fetch one by id+user, insert, update,
      delete. Each one parameterized, each one filtered by user where appropriate.
- [ ] Show the current user's notes inline in the chapter reader, attached to their verse (F8 partial).
- [ ] Make each verse selectable to open a note editor (plain HTML fallback first if you can).
- [ ] Build the create-note route: require login, require POST, validate reference against the Bible
      data, validate the body, insert, then redirect back to the chapter with feedback (F7).
- [ ] Build the "My Notes" page: list the current user's notes with references, snippets, and controls
      (F8).
- [ ] Build the edit route: fetch by id **and** user; if not found, respond as "not found"; otherwise
      validate and update (F9).
- [ ] Build the delete route: POST-only, ownership-filtered, with confirmation (F10).
- [ ] Add the ownership rule plainly in your code comments: "a note is visible/editable only to its
      owner; queries always filter by the session user's id" (F11).
- [ ] Decide and enforce duplicate-note behaviour if you chose one-note-per-verse (§6.4).
- [ ] Add empty-state UI for a user with no notes.
- [ ] Commit.

**Implementation Guidance** — Write the SQL-and-Python functions first and test them from a script with a
fake user id, *before* wiring any HTML. Then build the routes thinnest-first: create, list, edit,
delete. For the inline display, convert the fetched rows into a lookup keyed by verse number so the
template can ask "does this verse have a note?" once per verse instead of scanning the list. Always
redirect after a successful write so a refresh does not resubmit; use a feedback message to confirm
success. Never rely on the template to hide controls as your only protection — hidden HTML is not
security.

**Questions You Should Be Able to Answer**
1. Which column ties a note to a user, and where is it set when a note is created?
2. What happens when user B requests the edit URL for user A's note id? Trace it.
3. Why do all three write routes require POST?
4. Why redirect instead of rendering after a save?
5. How does the reader know which verses have notes without querying once per verse?
6. If you deleted the `WHERE user_id = ?` clause from a query by accident, what would a user see?

**Testing Checklist**
- [ ] Create a note as A on a verse; the verse shows the note only for A.
- [ ] Create with an empty body → rejected with a message; no row inserted.
- [ ] Create with an over-long body → rejected by your limit.
- [ ] Create while logged out → redirected to login, no row inserted.
- [ ] Create with a tampered verse reference (nonexistent chapter/verse) → rejected, no row inserted.
- [ ] Two notes on different verses both display correctly.
- [ ] Second note on the same verse behaves exactly as you documented.
- [ ] My Notes lists A's notes only; fresh account shows the empty state.
- [ ] Edit A's note → text and updated timestamp change; the DB shows one row, not two.
- [ ] Edit with an empty body → rejected.
- [ ] Edit a nonexistent note id → friendly not-found.
- [ ] **As B, attempt to edit and delete A's note ids directly** → both fail, and A's note is unchanged
      (verify with the CLI before and after).
- [ ] Delete A's note → disappears from the chapter and from My Notes; row gone from the DB.
- [ ] Delete via a GET request (type the URL) → refused.
- [ ] Refresh after each save → no duplicate submission.
- [ ] Note text containing `<script>` displays as literal text everywhere it appears (reader, notes page).

**Completion Criteria**
- [ ] Create, read, update, delete all work and are ownership-filtered.
- [ ] Cross-user access is impossible via URL tampering or form tampering (tested, not assumed).
- [ ] Every write route is POST + login-required + validated.
- [ ] A second account genuinely cannot see the first account's notes anywhere in the UI or data.

**Common Problems**
- *Checking ownership only in the template* ("hide the button for other users") — the server must refuse,
  not hide.
- *Fetching a note by id alone* then trusting it — always include the owner in the `WHERE` clause.
- *Deleting via a link/GET* — destructive actions must be POST.
- *Forgetting to redirect* → a refresh re-posts and duplicates or errors.
- *Treating the hidden form field as trusted* — re-validate the reference against the Bible data.
- *Storing the verse as a display string* ("John 3:16") and then having to parse it back — store stable
  identifiers.
- *Timestamp confusion* — decide once whether timestamps are UTC and how they are displayed.

**Checkpoint 6** — Can you explain how a foreign key connects a note to a user, and exactly which code
prevents user B from reading user A's note? (Answer must be server-side.)

---

### Phase 7 — Frontend and JavaScript Polish

**Objective** — Make the app pleasant and obviously complete, using JavaScript only where it genuinely
helps.

**Concepts to Learn**
- Semantic HTML and why it matters (accessibility, and it makes CSS trivial).
- Responsive layout with Bootstrap's grid/utility classes; consistent spacing and typography.
- DOM selection and event handling in vanilla JavaScript; `data-` attributes as the bridge from server
  to script.
- Progressive enhancement: the page must work before JavaScript runs, and must not break when it fails.
- CSS specificity, and why "just add `!important`" is not a fix.

**Prerequisites** — Phase 6 complete and all cross-user tests passing. Never polish before the core
works; polish on a broken core hides bugs.

**Tasks**
- [ ] Give every page a clear title and consistent navigation (Books · Search · My Notes · Log in/out).
- [ ] Make the reading column comfortable: line length, spacing between verses, verse numbers visually
      distinct.
- [ ] Style the note affordance: a verse with a note must be obvious at a glance (F8 improvement).
- [ ] Style the note editor (open/closed states) and its save/cancel/edit/delete affordances.
- [ ] Add client-side JavaScript per §14 — only the interactions you can justify.
- [ ] Make search results readable: reference bold, matched text visible, results clearly separated.
- [ ] Show feedback messages (success/error) in a consistent place with consistent styling.
- [ ] Make the layout usable at narrow widths (phone-sized window) — Bootstrap's grid handles most of it.
- [ ] Ensure every interactive element is reachable by keyboard and has visible focus.
- [ ] Ensure every form has labels and sensible input types.
- [ ] Test with JavaScript disabled and confirm nothing critical breaks.
- [ ] Commit.

**Implementation Guidance** — Pick one utility scale (spacing/typography) and stick to it rather than
styling element by element. Do the JavaScript last, one interaction at a time, testing after each. If an
interaction can be done with plain HTML (a form, a link, a `<details>` element), prefer that — it is less
code, it works without JS, and it cannot break. When you do use JavaScript, keep the data it needs in
`data-` attributes rather than constructing URLs in strings, and re-test the no-JS path afterwards.

**Questions You Should Be Able to Answer**
1. Which pages/sections are "must be usable with JavaScript off"? Prove it.
2. Where does your JavaScript get the information it needs (verse number, note text, URLs)?
3. What happens if the script file fails to load? Does the app still function?
4. Why is hiding a button with CSS not a security measure?

**Testing Checklist**
- [ ] Every page renders correctly at 375px width and at desktop width.
- [ ] Keyboard-only navigation can reach the search box, the note control, and the save button.
- [ ] Notes are visually obvious in the reader; verses without notes are not cluttered.
- [ ] With JavaScript disabled: read, search, register, login, create note, edit, delete all still work.
- [ ] With JavaScript enabled: the intended interactions work, and disabling JS does not leave broken
      UI elements behind.
- [ ] No console errors on any page (open dev tools, reload every page, watch the console).
- [ ] No 404s in the network tab for CSS/JS/images.

**Completion Criteria**
- [ ] All pages look intentional and consistent.
- [ ] JavaScript is optional for every core feature.
- [ ] No console errors and no missing assets.
- [ ] A stranger could use the app without instructions.

**Common Problems**
- *Polishing before the core is correct* — wasted effort, and it hides bugs behind styling.
- *Assuming users have wide screens* — test narrow.
- *Using JavaScript to build URLs that Jinja could have built* — fragile and inconsistent.
- *Making a button that does nothing without JS and calling it done* — always provide an HTML fallback.
- *`!important` everywhere* — fix your selectors instead.
- *Breaking auto-escaping while adding highlight markup* — escape, then wrap.

---

### Phase 8 — Systematic Testing

**Objective** — Prove the application is correct, including the cases you did not build for. Convert
"it seems to work" into evidence.

**Concepts to Learn**
- The difference between testing that a feature works and testing that it fails correctly.
- Test matrices: two users × cross-ownership attempts.
- Regression testing: re-running earlier checklists after later changes.
- Reading HTTP status codes and server logs as evidence.
- Why "I tried it once" is not testing.

**Prerequisites** — Phases 3–7 feature-complete. Do this phase before deployment, and again after it.

**Tasks**
- [ ] Create a written test log (markdown or spreadsheet): test · steps · expected · actual · pass/fail.
      This file also becomes evidence for your submission.
- [ ] Execute the full §11 checklist — every item — and record results.
- [ ] Build a two-user cross-ownership matrix and record the outcome of every combination.
- [ ] Loop through all 66 books and every chapter programmatically (calling your own lookup functions)
      and assert nothing raises. Record how many chapters and verses you verified.
- [ ] Test your error pages: bad slug, bad chapter, unknown URL, and a deliberately triggered server
      error — confirm no traceback is ever shown to a browser user.
- [ ] Test with JavaScript disabled, at a narrow viewport, and with the keyboard only.
- [ ] Test a cold start: delete the database, recreate it from the schema, and run the whole flow from
      registration onward.
- [ ] Re-run the Phase 3, 4, 5 and 6 checklists; fix regressions.
- [ ] Commit the test log.

**Implementation Guidance** — Record the *expected* result before you run each test; otherwise you will
unconsciously accept whatever happens. When a bug appears, do not fix it immediately: write down the
smallest reproduction, use §16 to locate the layer, then fix, then re-run that whole checklist section.
Keep a short "bugs found and fixed" list — excellent material for your video and your README's
challenges section.

**Questions You Should Be Able to Answer**
1. How many chapters did you verify, and what script or loop verified them?
2. Which exact tests prove user A cannot see user B's notes?
3. What was the worst bug you found, which layer was it in, and how did you diagnose it?
4. Which parts of the app remain untested, and why are you comfortable with that?

**Testing Checklist**
- [ ] §11 executed end to end with recorded results.
- [ ] Zero unhandled tracebacks for any input producible from the UI.
- [ ] Cold-start (empty DB) flow works.
- [ ] All 66 books render their chapters without error.
- [ ] Cross-user tests all pass.

**Completion Criteria**
- [ ] Test log exists, is committed, and shows every §11 item executed.
- [ ] All failures fixed and re-tested, or explicitly documented as accepted limitations.
- [ ] You can name your three riskiest untested assumptions.

**Common Problems**
- *Testing only the happy path* — graders immediately try invalid input.
- *Fixing without reproducing* — you will not know whether it is fixed.
- *Not re-testing after a fix* — the most common cause of a broken demo.
- *Testing through the UI only* — inspect the DB and logs directly at least once per feature.

---

### Phase 9 — Deployment

**Objective** — Make the project run somewhere other than your laptop, and prove it there.

**Concepts to Learn**
- Development vs production servers; why the built-in server is not for production.
- Environment variables and secrets on a host; why the secret key must not be committed.
- Database location on a host and file-system persistence (SQLite on an ephemeral file system resets!).
- Debug mode risks in production (the interactive debugger can execute code from a browser).
- Logs, and how to read them when something fails remotely.

**Prerequisites** — Phase 8 complete.

**Tasks**
- [ ] Verify all configuration comes from environment variables; nothing hard-coded.
- [ ] Write the exact run instructions in your README (create DB from schema → run → open).
- [ ] Confirm `.gitignore` excludes the DB file, `.env`, and `__pycache__`.
- [ ] Choose a host and read its deployment guide *before* writing any config.
- [ ] Deploy, then set environment variables on the host (secret key, DB path).
- [ ] If the host's file system resets on redeploy, ensure the database is created on startup if
      missing, or move it to a persistent location. **Decide and document.**
- [ ] Ensure debug mode is OFF on the deployed instance and error pages never show tracebacks.
- [ ] Walk the deployed app through the §11 checklist again (a second pass, on a different machine).
- [ ] Record the deployed URL in your README.
- [ ] Keep a copy of a known-working state so a bad deploy cannot sink your submission.

**Implementation Guidance** — Treat deployment as a *separate feature with its own testing*, not as a
final step done at 2 a.m. The three things that actually break: (1) the secret key differs or is missing
→ sessions break and login appears random; (2) the database path is relative and points somewhere
unwritable or non-persistent → registration appears to succeed and then vanishes; (3) a data-file path
assumes the repository root → an import-time crash with a confusing message. Solve all three by making
every path explicit and configurable.

**Questions You Should Be Able to Answer**
1. Where does the deployed app get its secret key, and what happens if it is missing?
2. Where does the deployed database live, and will it survive a redeploy? Why?
3. Why is debug mode dangerous on a public server?
4. How would you debug a problem that only happens on the deployed server?

**Testing Checklist**
- [ ] Deployed app loads the books list.
- [ ] Registration and login work on the deployed instance.
- [ ] Notes create, edit, delete on the deployed instance.
- [ ] Search works on the deployed instance.
- [ ] No tracebacks visible to users; a deliberate error shows your 500 page.
- [ ] Data survives a page reload and, if the host allows, a restart.
- [ ] The README instructions reproduce your setup from a clean clone.

**Completion Criteria**
- [ ] A working public URL exists and is recorded in the README.
- [ ] Secrets come from the environment; debug is off.
- [ ] The full §11 checklist passes on the deployed instance.
- [ ] Clean clone + README steps + schema recreate a working app.

**Common Problems**
- *Committing `.env`* — rotate the secret and remove it from Git history.
- *SQLite on an ephemeral file system* — recreate the DB on startup if absent, or use persistent
  storage; otherwise your demo loses its users mid-presentation.
- *Assuming the working directory is the repo root* — build paths relative to the code file.
- *Forgetting dependencies on the host* — pin them in `requirements.txt`.
- *Deploying at the last minute* — deploy while you still have two days to spare.

---

### Phase 10 — CS50 Final Submission

**Objective** — Package the project so a stranger can run it, understand it, and see what you learned.

**Concepts to Learn**
- Technical writing: a README that lets someone else run your project in under five minutes.
- Explaining design trade-offs out loud, concisely.
- Recording a demonstration video that *proves* behaviour rather than describing it.

**Prerequisites** — Phase 9 complete (not necessarily deployed publicly — but the app must run reliably
with documented instructions).

**Tasks**
- [ ] Write the README following §20's outline (do not copy a template blindly; adapt it).
- [ ] Confirm the README's run instructions work from a clean clone. Actually do this in a fresh folder.
- [ ] Confirm the Bible data file is included (or clearly documented) and its source is credited.
- [ ] Ensure `requirements.txt` is complete and minimal.
- [ ] Verify the repo contains no secrets, no DB file, no virtual environment.
- [ ] Write your design-decisions document (why two data stores, why slugs, why your search rules, why
      your note-uniqueness decision).
- [ ] Write your "what I learned" and "challenges" notes (short bullets; expand while recording).
- [ ] List future improvements (from §18's stretch list only).
- [ ] Prepare and record the demonstration video using §21's sequence (keep it short and dense).
- [ ] Verify the video shows: the URL, the whole core loop, the database being real, and one invalid
      input being handled gracefully.
- [ ] Re-read §19 and tick every box that is genuinely true.
- [ ] Final commit with a clear message; tag or note the submission state.

**Implementation Guidance** — Write the README as if for a future you who forgot everything: exact
commands, exact file locations, exact steps. Then have someone else (or a fresh terminal) follow it
literally. The most common submission failure is not a bug — it is instructions that only work on the
author's machine. For the video, prepare three or four specific things you want to *point at and
explain* (your search algorithm, your ownership filter, your schema), and speak about them while the
browser shows them working.

**Questions You Should Be Able to Answer**
1. Can a stranger run this in five minutes using only your README? Have you tested that literally?
2. For each required feature, where is it in the code? (Be able to point at the file and function.)
3. What are your three most important design decisions and their trade-offs?
4. What would you change if you started again, and why?
5. What did you build that you are genuinely proud of?

**Testing Checklist**
- [ ] Clean-clone test: fresh folder, following only the README, app runs.
- [ ] Database recreates from the schema without manual edits.
- [ ] No secrets in the repo (`git log -p` for `.env`, keys, passwords).
- [ ] No DB file, no `__pycache__`, no `.venv` committed.
- [ ] Demo video plays, is the right length, and shows every core feature.
- [ ] Video shows invalid input handled gracefully and a real database row changing.

**Completion Criteria**
- [ ] README complete and verified against a clean clone.
- [ ] Demonstration video recorded and reviewed by you once, critically.
- [ ] §19 checklist fully ticked.
- [ ] Repository in a state you would be happy to show an employer.

**Common Problems**
- *A README that assumes your venv is already active, or that you are on the same OS.*
- *A demo that only shows the happy path* — prove invalid input is handled.
- *A video that is a code tour with no interface* — show the application, not your editor.
- *Leaving debugging leftovers (print statements, commented-out experiments) in the final commit.*
- *Submitting without re-running the app from a clean state* — the classic "it worked yesterday".

**Gate** — The project is not complete until §23 (Definition of Done) is fully satisfied.

---

## 9. Learning Checkpoints

These are the moments where you stop typing and prove you understand. Write a two-to-four sentence answer
in your notes for each. If you cannot answer without looking at the code, you do not own it yet — and
during your presentation you will be asked exactly this kind of question.

### Checkpoint 1 — after Phase 1 (Flask basics)

- [ ] How does a Flask request reach a route? Name every step.
- [ ] How does Jinja receive data from Python, and what happens if a name does not exist?
- [ ] Why does the app need a secret key, and what exactly is signed with it?
- [ ] What is the difference between a redirect and rendering a template? Which one changes the browser's
      URL?

### Checkpoint 2 — after Phase 2 (data layer)

- [ ] How is the Bible stored, and what happens in memory when the app starts?
- [ ] Why is `verse_index` a dict keyed by a tuple, and what is its lookup cost?
- [ ] What normalization happens to text before searching, and why?
- [ ] Which numbers are one-based and which are zero-based, and where is that converted?
- [ ] How does the app know how many chapters a book has, without hard-coding anything?

### Checkpoint 3 — after Phase 3 (reader)

- [ ] Trace "Genesis 1" from URL to HTML.
- [ ] How does "next chapter" know when to move to the next book?
- [ ] Why does an invalid chapter return 404 rather than a page saying "no verses"?
- [ ] Which part of your code decides that a reference is valid?

### Checkpoint 4 — after Phase 4 (search)

- [ ] How does a search query find matching verses, step by step?
- [ ] Substring or whole-word? What is the user-visible consequence of that choice?
- [ ] Why is the query capped or paginated, and what does the user see when the cap is hit?
- [ ] Why can a search result never inject HTML into the page?

### Checkpoint 5 — after Phase 5 (auth)

- [ ] Why must passwords be hashed? Why is the hash deliberately slow?
- [ ] How does SQLite store my users, and where does that file live?
- [ ] What is in the session cookie, and what must never be in it?
- [ ] How does the login guard know the current user, on every request?
- [ ] What is the difference between authentication and authorization in this app?

### Checkpoint 6 — after Phase 6 (notes)

- [ ] How does a foreign key connect a note to a user?
- [ ] Which single condition in my queries makes notes private — and what breaks if it is removed?
- [ ] Why do create/edit/delete require POST, and what could go wrong with GET?
- [ ] How does the reader know which verses have notes without one query per verse?
- [ ] If I had to explain my ownership check to a security reviewer, what would I show them?

### Checkpoint 7 — after Phase 7 (frontend/JS)

- [ ] How does JavaScript interact with the DOM in my app — which elements, which events, and where does
      its data come from?
- [ ] Which features still work with JavaScript disabled, and how do I know?
- [ ] Why is hiding an element with CSS not an authorization control?

### Checkpoint 8 — before submission

- [ ] Can I explain every file in my project and why it exists?
- [ ] Can I explain every database column and constraint?
- [ ] Can I explain why the Bible is not in SQLite?
- [ ] Can I name the three bugs that cost me the most time, and the layer each one lived in?
- [ ] Can I demonstrate the entire application without AI assistance and without notes?

---

## 10. CS50 Concepts Mapping

### 10.1 Where each CS50 idea appears in this project

| Project component | CS50 concept | Where it lives | What to explain in the presentation |
| --- | --- | --- | --- |
| Flask routes / request handling | Web programming (Week 9) | `app.py` | How a URL becomes a function call; GET vs POST; status codes; redirect-after-POST |
| HTML structure | HTML/CSS (Weeks 8–9) | `templates/` | Semantic markup, forms, links, and why HTML comes from templates, not Python strings |
| Jinja templating | Templating / abstraction | `templates/*.html` | Inheritance via `layout.html`, loops over verses, auto-escaping as a security feature |
| CSS / Bootstrap | CSS, layout | `static/css/` | Responsive layout, readable reading column, consistent spacing |
| SQLite schema | Databases (Week 7) | `database/schema.sql` | PRIMARY KEY, UNIQUE, FOREIGN KEY, NOT NULL, indexes, and why constraints live in the schema |
| CRUD queries | SQL (Week 7) | `helpers.py` | SELECT/INSERT/UPDATE/DELETE, filtering by owner, ordering, row counts |
| Parameterized queries | SQL injection | all DB code | Why string concatenation is a vulnerability and how parameters work |
| Password hashing | Security | auth helpers | Hashing + salting, why hashing is slow, why hashes are not reversible |
| Sessions and login guard | Sessions / cookies | `app.py` + helpers | What the cookie holds, why it is signed, what "logged in" means |
| Authorization on notes | Security / access control | notes routes | Ownership filtering on every statement; why hidden UI is not protection |
| Bible JSON loading and indexing | Data structures / file I/O (Weeks 5–6) | `bible.py` | Dict vs list trade-offs, precomputed indexes, load-time vs query-time work |
| Search algorithm | Algorithms (Weeks 3–5) | `bible.py` | Normalization, linear scan vs index, complexity of your approach, result cap |
| Input validation | Defensive programming | `helpers.py` | Rejecting bad input at the edge; server-side validation |
| Error handling | Exception handling (Week 6) | routes + error handlers | 404/500 pages, never showing tracebacks, failing loudly at startup |
| JavaScript interactions | JavaScript (Week 8) | `static/js/` | DOM selection, events, progressive enhancement, `data-` attributes as the server→client bridge |
| Git workflow | Version control | repo | Meaningful commits, not committing secrets/data |
| Deployment/config | Web hosting | env + README | Environment variables, why debug mode is dangerous publicly |

### 10.2 How to use this table while building

- Before starting a phase, read the rows that match it and make sure those concepts are clear. If not,
  revisit the relevant CS50 material first.
- After finishing a phase, add one line to your notes: *"I can explain ___ because I did ___."* That
  sentence becomes presentation material.
- If a row in this table has no corresponding code in your project, either you skipped a feature or you
  built something you cannot explain. Both need attention.

### 10.3 The five explanations you should rehearse

1. **The request lifecycle for one page.** One URL, from browser to route to template to browser.
2. **Why two data stores.** Bible is read-only and shipped as a file; users/notes are mutable and live
   in SQLite. Explain the trade-off.
3. **How search works.** Normalization → matching → ordering → cap, plus why it is fast enough.
4. **How privacy is enforced.** The session identifies the user; every note query filters by that user;
   the template only renders what the server already authorized.
5. **What you would do differently.** One honest limitation and one concrete next step.

---

## 11. Testing Strategy

Record every test in a log with columns: **ID · Area · Steps · Expected · Actual · Pass/Fail · Notes**.
Do not record only failures. Your log is evidence.

### 11.1 Manual (browser) testing

- [ ] Every link in the navigation works from every page (no dead ends).
- [ ] Browser Back behaves sensibly after each action (especially after saves and deletes).
- [ ] Refresh after a save does not resubmit the form or duplicate data.
- [ ] Every page loads with status 200 and no console errors.
- [ ] Every page renders acceptably at 375px and 1280px+ widths.
- [ ] Keyboard-only operation of the search box, note control, and all buttons.
- [ ] With JavaScript disabled, all core features still work.
- [ ] A user with no notes, a user with one note, and a user with many notes all see sensible pages.
- [ ] Long verse text and long note text do not break the layout.

### 11.2 Database testing

- [ ] Tables, columns and constraints match `schema.sql` (`sqlite3` CLI: `.schema`).
- [ ] Recreating the DB from `schema.sql` produces an identical structure.
- [ ] Foreign keys are actually enforced (bad insert fails).
- [ ] Unique username is enforced by the DB, not just by Python (insert a duplicate directly via CLI →
      it must fail).
- [ ] Note uniqueness (if you chose it) is enforced by the DB.
- [ ] Registration persists after a full app restart.
- [ ] Notes persist after a full app restart.
- [ ] Editing a note updates the row in place (row count unchanged; `updated_at` changed).
- [ ] Deleting a note removes the row (verify by direct SELECT).
- [ ] No orphan notes exist: every `notes.user_id` matches a real user (write this as a SELECT and run
      it after your tests).
- [ ] No plaintext password exists anywhere: run a SELECT for the literal string you registered with and
      confirm zero rows.
- [ ] Deleting a user row (test only!) reveals what happens to dependent notes — know whether you get an
      error (good) or orphans (bad).

### 11.3 Authentication testing

| ID | Test | Expected |
| --- | --- | --- |
| A1 | Register with valid username + matching password | Account created; stored value is a hash |
| A2 | Register with empty username | Form redisplayed with an error; no row created |
| A3 | Register with empty password | Rejected |
| A4 | Register with mismatched confirmation | Rejected |
| A5 | Register with a 1-character password | Rejected (per your minimum length) |
| A6 | Register a duplicate username (exact) | Rejected with a friendly message |
| A7 | Register a duplicate username (different case) | Behaves per your documented decision |
| A8 | Register with spaces around the username | Trimmed and handled consistently |
| A9 | Login correct credentials | Logged in; nav changes |
| A10 | Login wrong password | Generic failure; **not** logged in |
| A11 | Login unknown username | Same generic failure message as A10 |
| A12 | Login with empty fields | No crash; failure message |
| A13 | Access a protected page while logged out | Redirect to login (302), then 200 on the login page |
| A14 | Access a protected page after logout | Redirect to login |
| A15 | Visit login/register while already logged in | Sensible behaviour (redirect or message) — document it |
| A16 | Session persistence across several pages | User stays logged in |
| A17 | Manually edit/delete the session cookie | Session invalid; no crash; no privilege gain; no 500 |
| A18 | Logout | Session cleared; protected pages unreachable |
| A19 | Reuse of an old cookie value after logout | Does not re-authenticate the user |
| A20 | SQL-injection string as username | No login, no data loss, no traceback |

### 11.4 Bible reader testing

- [ ] Genesis 1 (first chapter of the Bible) renders correctly.
- [ ] Revelation 22 (last chapter) renders correctly.
- [ ] Psalm 119 renders all 176 verses.
- [ ] A 1-chapter book renders and its navigation is boundary-safe.
- [ ] Previous/next work at the start and end of several books, including across book boundaries.
- [ ] Programmatic loop verifies every chapter of all 66 books loads without error (record the count).
- [ ] Invalid book slug → friendly 404 with correct status code.
- [ ] Invalid chapter number → friendly 404.
- [ ] Non-numeric chapter (e.g. `abc`) → friendly 404, no traceback.
- [ ] Chapter `0` and a negative chapter → rejected.
- [ ] Unknown URL entirely → your 404 page.
- [ ] Missing/renamed data file → app fails loudly at startup (not a blank page mid-demo).
- [ ] Verse text with special characters (apostrophes, quotes, ampersands) renders correctly.
- [ ] View-source check: no unescaped user-supplied text anywhere on reading pages.

---

### 11.5 Search testing

| ID | Query | Expected behaviour |
| --- | --- | --- |
| S1 | A very common word ("the", "and", "God", "love") | Results returned, capped/paginated per your rule, page responsive |
| S2 | A word that appears exactly once | Exactly one result with the right reference |
| S3 | A word that appears zero times (`zzzzqq`) | Friendly "no results" message, not an error |
| S4 | Different cases ("Begat", "begat", "BEGAT") | Identical results |
| S5 | A multi-word phrase ("the Lord is my shepherd") | Behaves exactly as documented (phrase / AND / OR) |
| S6 | A partial phrase ("shep") | Behaves per your match rule (substring vs whole word) |
| S7 | Leading/trailing/multiple spaces | Query normalized; sensible results |
| S8 | Punctuation: `LORD's`, `"quoted"`, `&`, `;`, `--`, `%`, `_` | No crash; no SQL/HTML interpretation |
| S9 | Empty query | Message; no crash; no full-Bible dump |
| S10 | Only spaces | Treated as empty |
| S11 | A 500-character query | Rejected or handled gracefully; no freeze |
| S12 | One character | Capped results, responsive, or a "too short" message |
| S13 | `<script>alert(1)</script>` | Displayed as literal text; never executed |
| S14 | `' OR 1=1 --` | No error; results unchanged; no DB effect |
| S15 | A non-English/emoji query | No crash |
| S16 | Same query twice | Identical order both times (determinism) |
| S17 | Every result link | Opens the correct chapter; anchor lands on the verse if you use anchors |

### 11.6 Notes testing

| ID | Test | Expected |
| --- | --- | --- |
| N1 | Create a note on a verse | Row created with correct owner; note visible inline for that user |
| N2 | Create with an empty/whitespace-only body | Rejected; no row |
| N3 | Create with an over-long body | Rejected by your limit; no row |
| N4 | Create while logged out | Redirect to login; no row |
| N5 | Create with a tampered book/chapter/verse | Rejected; no row |
| N6 | Note on the same verse twice | Per your documented decision |
| N7 | My Notes shows only my notes | Confirmed with two accounts |
| N8 | My Notes with zero notes | Empty state, no error |
| N9 | Edit my note | Text and timestamp update; still one row |
| N10 | Edit with an empty body | Rejected |
| N11 | Edit a nonexistent note id | Friendly 404 |
| N12 | **User B edits user A's note id** | Refused; A's note unchanged (verify via CLI) |
| N13 | **User B deletes user A's note id** | Refused; A's row still present (verify via CLI) |
| N14 | Delete my note | Row gone; UI reflects it; feedback shown |
| N15 | Delete via GET (typed URL) | Refused |
| N16 | Refresh after save | No duplicate submission |
| N17 | Note body containing `<script>` | Rendered as text in the reader and in My Notes |
| N18 | Note body with many newlines / very long word | Layout survives |
| N19 | Note on a verse in another book/chapter | Displays in the right place |

### 11.7 Security-specific tests

- [ ] SQL injection in every text input (username, password, note body, search query): no login bypass,
      no data loss, no traceback.
- [ ] XSS payloads in the note body and search query: rendered inert, visible in page source as text.
- [ ] Direct-object-reference sweep: log in as B and try A's note/verse URLs and form posts → all fail.
- [ ] Protected routes without a session → redirect, never a rendered page.
- [ ] Destructive actions via GET → refused.
- [ ] Server error page: trigger an error and confirm the user sees a friendly page, while the *server
      log* shows the details.
- [ ] The DB file is not downloadable from the deployed site.
- [ ] No secrets, absolute local paths, or password hashes appear in any rendered page.

### 11.8 Regression checklist (run after any later change)

- [ ] Cold start from an empty database.
- [ ] Register → log in → read → search → create → edit → delete → log out.
- [ ] First chapter, last chapter, single-chapter book.
- [ ] One invalid URL and one invalid chapter.
- [ ] Cross-user note access attempt.

---

## 12. Security Checklist

Explanations only — you write the code. For each item, know *what it stops* and *what happens if you
skip it*.

### 12.1 Password handling

- **Rule** — Store only a slow, salted hash. Never store, log, or display the plaintext password, and
  never put it in the session.
- **Why** — A leaked database should not immediately hand over working credentials; salts stop identical
  passwords from producing identical hashes; slowness makes brute-force attempts expensive.
- **Use the standard library helper** (Werkzeug provides hashing/verification functions Flask already
  depends on) rather than writing your own scheme. In Werkzeug 3.x the default method is **scrypt**, and
  verification handles the method and salt encoded in the stored string.
- **Do** compare using the library's verification function, and treat "no such user" and "wrong
  password" identically to the user.
- **Verify with the CLI** that a registered account's stored value is a hash, not the password.

### 12.2 Sessions and cookies

- **Rule** — The session must be signed with a strong secret key that comes from the environment and is
  never committed. Store only the user's id (and maybe username) in it.
- **Why** — The cookie is client-side; anything in it is readable by the user. The signature prevents
  tampering (a modified cookie is rejected), but a *readable* cookie must never contain secrets.
- **Do** rotate the secret if it leaks; keep sessions small; call `.clear()` on logout so the identity is
  truly gone.
- **Do** ensure cookie settings are sensible for production (for example, only sent over HTTPS, not
  readable by JavaScript) if your host supports HTTPS — a one-line configuration, but be able to explain
  why each flag exists.
- **Verify** — edit the cookie value by hand and confirm the app does not treat you as the user whose id
  you typed.

### 12.3 SQL injection

- **Rule** — Every query uses parameters. No user-supplied value is ever concatenated or interpolated
  into SQL text.
- **Why** — With concatenation, a value like `' OR 1=1 --` changes the *structure* of the statement
  instead of being data.
- **Do** keep all SQL inside a few helper functions so there is exactly one style in the codebase.
- **Verify** — attempt injection in every text input and check both the response and the resulting rows.

### 12.4 Input validation

- **Rule** — Validate on the server, always. Client-side attributes are courtesy, not control.
- **Validate** — required fields, lengths (min/max), types, allowed characters, trimmed non-empty text,
  and *references* (book/chapter/verse must exist in the dataset).
- **Why** — Anyone can submit any value to any endpoint with a tool; your HTML restrictions mean nothing
  to them.
- **Do** validate before touching the database, and report specific, friendly errors.
- **Verify** — submit over-long, empty, misspelled and malicious values by hand.

### 12.5 Authorization and user-owned data

- **Rule** — Every read or write of a note is filtered by the session user's id. A missing row and a
  not-yours row are indistinguishable to the client (both "not found").
- **Why** — This is the project's core privacy requirement. Hiding a button is not enforcement.
- **Do** put ownership in the `WHERE` clause; check the number of affected rows on updates and deletes.
- **Verify** — the two-account matrix in §11.7.

### 12.6 Output escaping (XSS)

- **Rule** — Let the template engine escape by default. Never disable escaping on user or dataset text.
  Escape first, then add your own markup (for example around search highlights).
- **Why** — Unescaped user text can execute JavaScript in another user's browser; in a notes app, one
  user could attack another.
- **Verify** — store `<script>alert(1)</script>` as a note body and confirm it displays as text and does
  not execute.

### 12.7 Method safety, destructive actions, CSRF

- **Rule** — Anything that changes data (create/edit/delete/logout) is POST-only. Anything safe and
  repeatable (viewing, searching) is GET.
- **Why** — GET must be safe and idempotent: a link, a prefetch, or an image tag should never delete
  data. Browsers and crawlers follow GET requests freely.
- **CSRF considerations for this scope** — Your session cookie is sent automatically, so a page on
  another site could in principle submit a form to your app on a logged-in user's behalf. For a CS50
  project, the minimum defensible position is: (a) state this limitation honestly in your README, and
  (b) if you want to address it, use a per-session token stored in the session and compared on POST.
  Either way, be able to explain what the attack is.
- **Verify** — try to perform each destructive action with a GET request; all must be refused.

### 12.8 Secrets, configuration and debug mode

| Item | Development | Production |
| --- | --- | --- |
| Secret key | from `.env`/environment | from host environment variables |
| Debug mode | may be on locally | **must be off** |
| Error details | traceback visible to you | generic page for users; details in server logs |
| Database | local file path | configured path that persists |
| `.env` | in `.gitignore` | not present in the repo at all |

- **Why debug off matters** — the interactive debugger allows code execution from a browser page, and
  tracebacks leak paths, queries and sometimes data.
- **Verify** — trigger an error on the deployed instance and confirm users see only your friendly page.

### 12.9 The honest security statement for your README

Write one short paragraph stating what your app protects (hashed passwords, session-based identity,
owner-filtered notes, parameterized queries, escaped output) and what it does not attempt (no email
verification, no password reset, no rate limiting, no CSRF token *if you chose not to add one*). Being
explicit about limits is a strength, not an admission of failure.

---

## 13. UI/UX Plan

Keep the visual design plain, consistent, and quiet. The text is the content; the interface should get
out of its way. You need **eight pages** (plus two error pages). Do not design more.

> **Visual reference:** `design/preview.html` in this repository renders every page below as a static,
> browser-viewable mockup (open the file directly — no server needed), with the design tokens in
> `design/manna.css` and a page → route → template → feature-ID map in `design/README.md`. Treat it as
> a target to build toward, **not** markup to paste: you still write your own Jinja templates.

### 13.1 The pages

| # | Page | Purpose | Requires login |
| --- | --- | --- | --- |
| 1 | Books list | Entry point; choose a book to read | No |
| 2 | Chapter reader | Read verses; open note editors | No (notes need login) |
| 3 | Search results | Show matches for a query | No |
| 4 | Register | Create an account | No |
| 5 | Login | Authenticate | No |
| 6 | My Notes | Review and manage all my notes | Yes |
| 7 | 404 page | Friendly not-found | No |
| 8 | 500 page | Friendly error | No |

Optional page: a "chapters in this book" page between the books list and the reader. Only add it if the
chapter picker in the reader feels cramped.

### 13.2 Page-by-page specification

#### Page 1 — Books list

- **Purpose** — Get the user reading in one click.
- **Main components** — Page title; a grouped or grid list of 66 books; the search form; global nav.
- **User actions** — Click a book; search; log in/out.
- **Information displayed** — Book names, ideally with chapter counts or testament grouping.
- **Notes** — Prefer a multi-column or grid layout over a single long centred column; users scan lists
  faster than prose. Every item must be a real link.

#### Page 2 — Chapter reader

- **Purpose** — Read, and attach thoughts to verses.
- **Main components** — Reference heading ("John 3"); previous/next chapter controls; chapter picker for
  the current book; the verse list with numbers; note indicators; note editor (hidden until used); a
  link back to the books list.
- **User actions** — Read; navigate; click a verse to open its note; save/edit/delete a note; search.
- **Information displayed** — Verse numbers and text; whether a verse has my note (and its text, for me
  only); whether I am logged in.
- **Notes** — Use a comfortable reading column (roughly 60–80 characters), generous line height, and a
  visually distinct verse number. The note control must be obvious but not noisy: 31,000 verses of
  buttons would be terrible. Prefer one clear affordance per verse, revealed on hover/focus and always
  available on tap/keyboard.

#### Page 3 — Search results

- **Purpose** — Show matches and let the user jump to context.
- **Main components** — Search form (pre-filled); result count; the result list; a message when capped;
  a link back to reading.
- **User actions** — Refine the query; click a result.
- **Information displayed** — Reference, verse text with the match visible, total matches.
- **Notes** — Always show the count; always give a way back. Keep each result compact — this page can
  contain many items.

#### Pages 4 and 5 — Register / Login

- **Purpose** — Create and use an identity.
- **Main components** — Form with labelled fields; submit button; a link between the two pages; error
  area.
- **User actions** — Submit; switch between register and login.
- **Information displayed** — Field-specific and summary errors; the username entered (preserved on
  error); never the password.
- **Notes** — Use proper `type` attributes so browsers offer sensible keyboard/autofill behaviour.
  Keep the two pages visually nearly identical so the switch is frictionless.

#### Page 6 — My Notes

- **Purpose** — Make stored notes findable and manageable.
- **Main components** — List or cards of notes; each with reference, body snippet, last-updated time, and
  edit/delete controls; a link to the verse; an empty state.
- **User actions** — Open the verse; edit; delete.
- **Information displayed** — "You have N notes"; canonical or recent ordering, stated in the heading or a
  caption so the user understands the order.
- **Notes** — The empty state is a real feature: explain how to create a note and link to the books list.

#### Pages 7 and 8 — Error pages

- **Purpose** — Keep the user oriented when something goes wrong.
- **Components** — A short human sentence, a link back to the books list, and (only in development) a
  code or reference for debugging.
- **Notes** — Never show a stack trace, a file path, SQL, or a database name to the user.

### 13.3 Consistency rules (write these down and follow them)

- [ ] One navigation bar, identical on every page, showing: Books · Search · My Notes (only when logged
      in) · Log In/Out.
- [ ] One feedback mechanism for success and error messages, in a fixed position.
- [ ] One primary button style, one secondary style, one destructive style (delete) — and destructive
      actions never look like ordinary links.
- [ ] Every form field has a visible label; errors appear next to the field they concern.
- [ ] One heading hierarchy: page title, then section headings, never skipped.
- [ ] Empty states exist for: no notes, no search results, empty search query.
- [ ] Every page has a way back to the reader and a way out of the current task.

### 13.4 What NOT to do

- No animation-heavy or card-grid dashboards; this is a reading app.
- No custom fonts loaded from five places; one system or one webfont at most.
- No dark-pattern confirmations; a simple confirmation step for delete is enough.
- No designing in a way that breaks the no-JavaScript path.

---

## 14. JavaScript Plan

JavaScript is the easiest way to add accidental complexity to this project. Use it for exactly three
things, and only after the no-JavaScript version works.

**Rule** — Every interaction below must have a working HTML-only fallback. If it does not, the
JavaScript is a liability, not a feature.

### 14.1 Where JavaScript genuinely helps

| # | Interaction | What JavaScript accomplishes | Fallback if it fails |
| --- | --- | --- | --- |
| 1 | Selecting a verse | Clicking a verse reveals/opens the note editor for *that* verse and (when logged in) prefills existing note text | A plain link or form per verse (for example an "Add/View note" link that loads a note page or an HTML `<details>` element containing the form) |
| 2 | Opening/closing the note panel | Shows one editor at a time, moves focus into it, hides others, and returns focus when closed; keeps the page from reflowing awkwardly | A server-rendered editor on its own page, or a form that posts and reloads |
| 3 | Showing/hiding UI | Reveals controls only when relevant (e.g. delete confirmation, "my notes only" filter on the reader, mobile nav) | The same controls rendered always, or a separate page route |
| 4 | Save feedback | Confirms a successful save without a full page reload, disables the save button while posting, prevents double-submits | A standard form POST with a server flash message |
| 5 | Search niceties | Live character counter, debounce, "clear" button, keyboard focus shortcut, indicating "searching…" | A normal submit button (this is the baseline you must keep) |
| 6 | Reading enhancements | Smooth scroll to a verse anchor, highlight the target verse after arriving from search or notes | Plain anchors and default scroll behaviour |
| 7 | Navigation enhancement | Mobile menu toggle, chapter dropdown convenience | A plain list of chapter links |

### 14.2 How the pieces communicate (concepts you must understand)

- The server renders the truth into the HTML: verse numbers, existing note text, URLs. JavaScript reads
  it from the DOM — commonly from `data-` attributes on the verse element rather than from a config
  object typed into the script.
- Never build URLs by string concatenation in JavaScript. Put the URL (or a route template) into the
  markup and read it back.
- If you ever post data with `fetch`, remember the server must still validate everything exactly as it
  does for a normal form post, and the response must be re-rendered or the page updated deliberately.
  For this project, **a normal form POST plus a page reload is a perfectly good implementation** — do not
  feel obliged to build a single-page feel.
- Keep scripts in `static/js/` and load them once from the layout; do not scatter inline scripts across
  templates.
- Wrap your code so it runs after the DOM exists, and guard against elements that are not present on the
  current page (a search page has no verses).

### 14.3 Questions to answer before writing any JavaScript

1. Which specific user problem does this interaction solve? (If you cannot answer, do not write it.)
2. What happens if the script fails to load? Have you tested that path *after* writing the script?
3. Where does the data come from — server-rendered attributes, or a request? Why is that the right
   choice?
4. Is any authorization decision being made in JavaScript? (Correct answer: never. The server decides;
   JavaScript may only hide or show what the server already allowed.)
5. Does keyboard focus end up somewhere sensible after the interaction (especially after opening or
   closing the editor)?

### 14.4 Testing checklist for JavaScript

- [ ] Every core feature works with JavaScript disabled.
- [ ] No console errors on any page, including pages without verses or notes.
- [ ] Rapid double-clicking the save button does not create two notes.
- [ ] Opening the editor for verse 5 while verse 3's editor is open does not leave orphaned state.
- [ ] After closing the editor, focus returns somewhere logical and the Escape key behaves predictably.
- [ ] The editor's content matches the correct verse after using Previous/Next chapter navigation
      (a classic bug: the script caches the first verse).
- [ ] With JavaScript enabled, the search form still works if you press Enter immediately.
- [ ] The interaction is usable on a narrow screen and by keyboard only.

### 14.5 What NOT to do with JavaScript

- Do not fetch the Bible or notes from a separate JSON API you invented for this project. You do not
  need an API; the server already renders everything.
- Do not implement validation only in JavaScript.
- Do not use a framework or a build step. Plain JavaScript is enough and keeps the project CS50-sized.
- Do not use JavaScript to make a page "load" that could just be HTML — you will break the no-JS path.
- Do not store note text in the DOM as the source of truth after editing; the database is the truth.

---

## 15. Git and Development Workflow

### 15.1 `.gitignore` (create this before your first commit)

At minimum, exclude: `.venv/` (or `env/`), `__pycache__/`, `*.pyc`, `.env`, the database file
(`database/*.db`), editor/OS junk (`.vscode/`, `.DS_Store`, `Thumbs.db`), and any scratch/debug output
files. **Keep committed:** all source, `templates/`, `static/`, `database/schema.sql`, `data/kjv.json`,
`requirements.txt`, `README.md`, and your test log.

Rule of thumb: *if deleting a file and recreating it is trivial (or it holds a secret), it does not
belong in Git.*

### 15.2 One-time setup

- [ ] `git init` in the project root, then check `git status` shows only source files (no `.venv`).
- [ ] Create the GitHub repository **empty** (no README, no `.gitignore`), or use whatever CS50 requires.
- [ ] First commit: skeleton + `.gitignore` + README stub + this roadmap.
- [ ] Verify with `git log --stat` that no unwanted file was committed.
- [ ] If you already committed a secret or the DB, remove the file from the index and rotate the secret;
      do not just delete it in a later commit.

### 15.3 Commit discipline

Commit when you reach a logical, working state — not at the end of the day out of guilt.

**Good commit messages** (imperative, specific, one idea each):

| Example | Why it is good |
| --- | --- |
| `Add chapter reader route with boundary-safe navigation` | One feature, describes the behaviour |
| `Load and index KJV JSON into lookups in bible.py` | Names the file and the intent |
| `Reject duplicate usernames with a friendly registration error` | Describes the user-visible result |
| `Filter note queries by session user id` | A security-relevant change, stated plainly |
| `Fix verse off-by-one when computing next chapter` | Names the bug and its area |
| `Add 404 page for invalid book slugs` | Scoped and verifiable |
| `Document search normalization rules in README` | Documentation is a real change |

**Poor messages to avoid:** `update`, `stuff`, `fix`, `final`, `asdf`, `changes`, `more work`.

Your commit history is evidence of how you built the project. A grader may look at it, and *you* will
look at it when writing your README's "challenges" section.

### 15.4 Branches

For a solo project, keep it simple:

- Work on `main` for the early phases.
- From Phase 5 onward, use a short-lived branch per feature (`phase5-auth`, `phase6-notes`,
  `polish-reader`) and merge when the phase's completion criteria are met.
- Never leave more than one branch open for long; you are not collaborating.
- Tag or note the submission state (`git tag submission`) so you can always return to exactly what you
  handed in.

### 15.5 Workflow loop

```text
1. git status                     → know what you changed
2. Make one coherent change
3. Test it (run the app, run the relevant checklist items)
4. git diff                       → read your own change; catch debug prints and commented-out code
5. git add <specific files>       → avoid blanket staging when unsure
6. git commit -m "<message>"
7. git push                       → keep the remote current (acts as a backup)
```

### 15.6 Testing before commits

- [ ] The app starts without errors.
- [ ] The pages touched by this change load.
- [ ] The relevant checklist section from §11 passes.
- [ ] No `print()` debugging statements or commented-out experiments remain (`git diff` shows them).
- [ ] No new secrets or hard-coded local paths.

### 15.7 Recovering from mistakes

| Situation | Recovery approach |
| --- | --- |
| Uncommitted change broke something | `git diff` to see it, then undo the specific edit by hand or revert that file |
| Committed but not pushed | Amend or reset the last commit (only if it is **your last commit** and unpushed) |
| Committed and pushed | Do not rewrite history; make a new commit that fixes it (and explain in the message) |
| Accidentally committed a secret | Remove the file from tracking, add it to `.gitignore`, rotate the key, and note it in the README |
| Accidentally committed the DB or `.venv` | Untrack it (`git rm --cached`), add to `.gitignore`, commit; history stays larger, which is acceptable |
| Deleted a file by hand and need it back | Restore it from the last commit |
| Want to try a risky idea | Branch first; delete the branch if it fails |
| Totally lost | `git reflog` lists recent states; `git stash` saved uncommitted work you meant to keep |

Learn these four commands before you need them: `git status`, `git diff`, `git log --oneline`, and
`git restore <file>`.

### 15.8 Repository hygiene at the end

- [ ] `git status` clean.
- [ ] No secrets, no DB, no virtual environment, no scratch files.
- [ ] README instructions match the repository exactly.
- [ ] Commit history tells a coherent story of the phases.
- [ ] The submission commit/tag is recorded in your notes.

---

## 16. Debugging Methodology

You will spend more time debugging than writing code. Do it in this order, every time. Do not skip steps
because you "already know" — the order is what makes it fast.

### 16.1 The nine-step procedure

```text
1. Reproduce      — find the smallest, most repeatable steps that show the problem
2. Locate layer   — request, logic, template, or data? (§4.1)
3. Inspect browser— console, network tab, page source, status codes
4. Inspect Flask  — read the traceback bottom-up and the per-request log line
5. Inspect DB     — query the actual rows with the sqlite3 CLI
6. Inspect input  — log exactly what the server received (temporarily, then remove)
7. Inspect output — log exactly what you are about to give the template
8. Fix ONE thing  — smallest possible change
9. Retest         — the original repro, then that feature's whole checklist section
```

If a step gives no information, you have not done it properly yet.

### 16.2 Which layer? Ask these questions

| Symptom | Most likely layer | First thing to check |
| --- | --- | --- |
| Page renders but a value is blank/`None` | Template seam | The name you passed vs the name used in the template |
| `UndefinedError` / Jinja error | Template seam | Variable name, or a dict key you assumed existed |
| 500 with a Python traceback | Logic seam | Read the **last** line: file, line, error type |
| 404 for a URL you expected to work | Request seam | The URL rule (typo, trailing slash, converter, variable name) |
| Form submits but nothing changes | Request/Data seam | Is the method POST? Are the field names the ones you read? Was it committed? |
| Data disappears after restart | Data seam | Committed? Which DB path? |
| Login state is random | Session seam | Secret key stability (is it regenerated on start?), cookie in the network tab |
| JavaScript does nothing | Frontend seam | Console errors, script path, DOM timing, element existence |
| Works locally, fails deployed | Config seam | Environment variables, paths, database persistence |

### 16.3 Flask errors

- Read the traceback **bottom-up**: the last frames belong to your code; the top ones are usually
  library internals.
- Use the interactive debugger locally, but understand its risk (§12.8) and keep it off in production.
- Temporarily disable the fancy error page when the error page itself is what confuses you.
- Log the URL and the incoming data at the start of a failing route, then remove the logging.
- Common causes: a missing import; a typo in a template name; a view function that falls off the end
  without returning a response; returning the wrong type (a plain dict is not a response).

### 16.4 SQL errors

| Error | Meaning | Approach |
| --- | --- | --- |
| `no such table` | Schema not created, wrong file, or wrong working directory | Inspect the DB with the CLI and confirm *which* file you opened |
| `no such column` | Column typo or mismatch with the schema | Re-read `schema.sql`; do not guess |
| `NOT NULL constraint failed` | You skipped a field or validation | Log the values you are inserting |
| `UNIQUE constraint failed` | Duplicate where the schema forbids it | Usually *good* news — turn it into a friendly message |
| `FOREIGN KEY constraint failed` | Referencing a nonexistent row | Confirm the id exists (session may be stale) |
| `datatype mismatch` | A number sent as text (or the reverse) | Inspect the value's *type*, not just the value |
| `database is locked` | Two writers at once | Understand connections and transactions; do not paper over it |

The standard technique: run the statement by hand in the CLI with literal values; then run it with the
actual values your code logs; compare. If the CLI works and the app does not, the difference is the
parameters, the connection, or the file.

---

### 16.5 Template errors

- Unknown variable → check the exact name passed to the render call against the name used in the
  template, character by character.
- Blank loops → the collection is empty or is not a list. Log its type and length.
- Attribute/key errors → a dict accessed with attribute syntax, or a list accessed with a key.
- Escaping oddities → look for a stray `|safe`.
- Technique that always works: temporarily print the raw context (or its keys) at the top of the page,
  confirm the shape, then remove it.

### 16.6 JavaScript errors

- Open the browser console **first**; an error there explains most "nothing happens" bugs.
- Check the Network tab that your script loaded (200, not 404) and is the version you think it is
  (hard refresh to defeat caching).
- Confirm the element exists on *this* page before attaching a listener; a selector that matches nothing
  is often the whole bug.
- Confirm timing: is the DOM ready before you attach?
- Log the values you read from the DOM, then delete the logs before committing.
- If nothing is logged at all, the script is not running, or it fails on its first line.

### 16.7 Authentication problems

- Is the secret key the same between restarts? An unstable key makes sessions appear random.
- Does the response set a cookie after login? Look in the Network tab, not just at the code.
- Does the cookie come back on the next request? If not, scope/path/secure settings are wrong.
- Is the login guard reading the same session key everywhere, with identical spelling?
- Is a redirect loop happening because a protected page redirects to another protected page?
- Verify the hash pipeline in isolation: hash a value, verify it, print the boolean.

### 16.8 Database state problems

- Never debug a data bug by looking only at the UI: query the rows directly.
- Compare "what should be there" with what is there: count rows, print the last inserted row.
- Check for duplicates and orphans with explicit queries.
- If in doubt, start clean: delete the DB, recreate it from the schema, repeat the exact steps. If it
  works on a clean database but not on the old one, your data is the problem, not your code.

### 16.9 Habits that make debugging fast

- **One change at a time.** Two simultaneous changes teach you nothing.
- **Bisect.** Comment out half of a suspect function to find which half misbehaves.
- **Write down the repro.** If you cannot describe it in two sentences, you do not understand it yet.
- **Read the error message literally.** It usually names the file, line, and problem.
- **Ask "which layer?"** before asking "what is wrong?".
- **Keep a bug log.** Symptom → cause → fix. It becomes your README's challenges section and your best
  defence if you are asked about debugging in the video.

---

## 17. Common Beginner Mistakes

Each entry: how to **recognize** it, why it hurts, and how to **avoid** it. Re-read this section before
Phase 6, and again before submission.

| # | Mistake | How to recognize it | Why it hurts | Fix / avoidance |
| --- | --- | --- | --- | --- |
| 1 | Putting too much logic in templates | `{% if %}` chains doing lookups or comparisons; the template needs data the route never passed | Untestable, invisible bugs; security decisions end up in HTML | Move the decision into Python; pass ready-to-render values |
| 2 | Database logic everywhere | SQL strings scattered across many files and routes | One schema change breaks ten places; inconsistent parameterization | One module for all DB access; routes call functions |
| 3 | Trusting user input | Using a hidden form field (book/chapter/verse) as-is | Users attach notes to nonexistent verses; tampering reaches other data | Re-validate every incoming reference server-side |
| 4 | Storing plaintext passwords | The DB column contains readable text | Instant loss of points; teaches the wrong habit | Hash with the standard library helper; verify with the CLI |
| 5 | Forgetting authorization checks | A query filters by note id but not by user id | Any user can read or edit any note by guessing an id | Owner filter in the `WHERE` clause of every note query; test with two accounts |
| 6 | One giant route | A 200-line view function | Impossible to read, test, or explain | Split into validation, lookup, render; extract helpers |
| 7 | Overusing JavaScript | Core features stop working with JS off | Fragile and harder to demo | HTML-first; JS for enhancement only |
| 8 | Features before the core is finished | Half-built extras while required features are missing | A demo with gaps scores worse than a small complete app | Obey §18; finish Phase 8 before any stretch goal |
| 9 | Not testing edge cases | It works for Genesis 1 and "love" | Breaks on Revelation 22, single-chapter books, empty queries | Work the §11 checklists literally |
| 10 | Copying code without understanding | You cannot explain a line to yourself | You cannot answer presentation questions or debug it | If you copy, rewrite it in your structure and say it out loud |
| 11 | Re-parsing the Bible per request | Pages feel slow | Wasted work on every page view | Load once at startup; measure |
| 12 | Off-by-one in chapter/verse numbers | Wrong verse shown; navigation skips or repeats | Data correctness is the app's whole point | One write-down of the 1-based/0-based rule; the Phase 2 integrity loop |
| 13 | Committing the DB or `.env` | `git status` shows them | Leaks secrets, bloats the repo, grades badly | `.gitignore` first, verified before every commit |
| 14 | Ignoring the traceback | Guessing instead of reading | Hours lost, wrong fixes | Read the last line; open that file and line |
| 15 | Silent failures | `except: pass`, or discarding errors | Bugs stay hidden until the demo | Catch specific errors; log or surface them |
| 16 | No empty states | Blank areas where a list should be | Feels broken to a first-time user | Explicit "no results" / "no notes yet" messages |
| 17 | Non-deterministic ordering | Results shuffle between refreshes | Looks buggy; hard to compare test runs | Always order results explicitly |
| 18 | Big-bang deployment | First deploy happens the night before | Deployment problems surface too late | Deploy at Phase 9, with time to spare |
| 19 | Vague commit history | `git log` is a wall of "update" | Loses a real portfolio artefact | Specific messages per §15.3 |
| 20 | Building an "API" nobody needs | Extra JSON endpoints "for later" | Doubles the surface area to build and test | The server renders HTML — that is enough |
| 21 | Changing the schema late | You "just add a column" in Phase 7 | Queries, templates and notes all break at once | Decide the schema in Phase 0/5 and keep changes additive |
| 22 | Hiding vs enforcing | The UI hides a button and you call it security | Direct URL access bypasses the entire control | Server-side ownership checks on every read/write |
| 23 | Hard-coding counts | "Psalm 119 has 176 verses" in the code | Silently wrong for other chapters | Always read counts from the data |
| 24 | No `ORDER BY` on notes | Notes appear in random order | Confusing, and it hides duplicate-note bugs | Explicit ordering everywhere |
| 25 | Debugging by adding features | "Maybe if I rewrite this part it will work" | New bugs on top of old ones | Reproduce, locate the layer, fix one thing (§16) |

**The pattern behind all of these** — they are all shortcuts taken to move faster. Each one costs more
time later than it saves now. When you feel the urge to take one, that is exactly the moment to stop,
write down the smallest correct version, and do that instead.

---

## 18. Scope Control

### 18.1 Core Project — the only thing that must exist

```text
F1  Books list                     F7  Create a note
F2  Chapter reader                 F8  View my notes
F3  Chapter navigation             F9  Edit my note
F4  Search                         F10 Delete my note
F5  Registration                   F11 Authorization (notes are private)
F6  Login / Logout                 F12 Bad input & not-found handling
```

Also required, though not a user-facing feature: a `schema.sql` that recreates the database, a README
that lets someone else run the app, a `.gitignore` that keeps secrets out, and a demonstration.

**Everything above must work, be tested, and be explainable before you do anything else.**

### 18.2 Stretch Goals — only after §19 is fully ticked

| Goal | Why it is a reasonable add-on | Why it must wait |
| --- | --- | --- |
| Filter/search within My Notes | Small query, real utility | Needs the notes list to exist and be stable |
| Highlight verses that have notes + "jump to my note" | Improves the core reading experience | Needs notes to be correct first |
| Copy-verse button | Small, genuinely nice | Trivial but irrelevant if notes are broken |
| Remember last reading position | Honest session usage beyond auth | Not required; adds state to reason about |
| Paginate search results | Shows `LIMIT`/`OFFSET` thinking | Only meaningful if search is already correct |
| Verse-range notes | More expressive notes | Changes the schema and the UI; a scope risk |

Add **at most two** stretch goals, and only after your test log proves the core is stable.

### 18.3 Out of Scope — DO NOT BUILD THIS YET (or at all, for this submission)

- [ ] Social features: following, friends, sharing notes publicly, public profiles.
- [ ] Comments or replies anywhere.
- [ ] Chat or messaging.
- [ ] AI features: chat with the Bible, summarization, embeddings, "ask a verse".
- [ ] Audio playback or text-to-speech.
- [ ] Multiple translations, translation switcher, parallel view, original-language interlinear.
- [ ] Cross-references, commentaries, dictionaries, Strong's numbers.
- [ ] Recommendation or "related verses" systems.
- [ ] Admin dashboards, user management screens, roles and permissions beyond "owner".
- [ ] Notifications (email, push, in-app).
- [ ] Reading plans, streaks, badges, gamification, points.
- [ ] Mobile apps, PWA/offline support, service workers.
- [ ] Sophisticated search: fuzzy matching, ranking/BM25, stemming, boolean query language,
      full-text indexes (FTS5), highlighting with relevance scores.
- [ ] Rate limiting, CAPTCHA, email verification, password reset, 2FA, OAuth/social login.
- [ ] Real-time anything: websockets, live updates, presence.
- [ ] Analytics dashboards of your own app.
- [ ] Microservices, containers, message queues, caching layers (Redis), CI/CD pipelines.
- [ ] Rewriting into a single-page application, or adding a JavaScript framework or build toolchain.
- [ ] Multi-database support or an ORM abstraction layer.
- [ ] A custom "API" that duplicates what your routes already render.

### 18.4 The scope-creep circuit breaker

Answer these three questions before adding anything not in §18.1:

1. **Does a required feature (F1–F12) depend on it?** If no, it is not next.
2. **Is §19 fully ticked?** If no, it is not next.
3. **Can I implement, test, and explain it in under two hours?** If no, it is a project, not a change —
   write it in the "future improvements" list in your README instead.

If you answer "but it would be cool" at any point, the correct action is: open your README, add it to
Future Improvements, close the file, and go back to the required work.

### 18.5 Why this restraint is the right call

CS50 evaluates what you built, whether it works, and whether you understand it — not how large it is.
A small application where every feature works, is tested, is secure, and is explained in your own words
will always outperform an ambitious half-finished one. Your scope decision is itself a design decision
you should mention in your README and your video: *"I deliberately shipped a small, complete, well-tested
app rather than an unfinished larger one."*

---

## 19. Final Quality Checklist

Tick every box before you consider the project finished. If a box cannot be ticked, that is your next
task — not a stretch goal.

### 19.1 Functionality

- [ ] F1 Books list shows all 66 books in canonical order.
- [ ] F2 Every chapter of every book renders with correct verse numbers and text.
- [ ] F3 Previous/Next chapter work, including across book boundaries, with no broken links at the ends.
- [ ] F3 Chapter picker offers exactly the correct number of chapters for each book.
- [ ] F4 Search returns correct, deterministic results for words and phrases.
- [ ] F4 Empty and no-match queries are handled with clear messages.
- [ ] F5 Registration works and rejects invalid/duplicate input.
- [ ] F6 Login, logout, and session persistence work correctly.
- [ ] F7 A logged-in user can create a note on a verse; it displays attached to that verse.
- [ ] F8 "My Notes" lists the signed-in user's notes with working links and an empty state.
- [ ] F9 A user can edit their own note; the change persists and the timestamp updates.
- [ ] F10 A user can delete their own note after confirmation; the row is gone.
- [ ] F11 No user can read, edit, or delete another user's note by any URL or form manipulation.
- [ ] F12 Invalid book, invalid chapter, invalid verse, bad method, and unknown URLs all fail gracefully.
- [ ] Refresh after any save does not duplicate data or resubmit.

### 19.2 Database

- [ ] `database/schema.sql` recreates the whole database from scratch.
- [ ] Tables, columns, types, and constraints match your design.
- [ ] PRIMARY KEY, UNIQUE (username), FOREIGN KEY, and NOT NULL all exist and actually do something.
- [ ] Foreign key enforcement is enabled on connections and verified with a bad insert.
- [ ] No plaintext password exists anywhere in the database.
- [ ] Note bodies and references are stored in the correct columns with the correct types.
- [ ] An orphan check returns zero rows (no note without a valid user).
- [ ] Row counts change exactly once per create and once per delete.
- [ ] The DB file is not committed and is listed in `.gitignore`.

### 19.3 Authentication and security

- [ ] Passwords are hashed with the standard library helper; hashes are never displayed or logged.
- [ ] The secret key comes from the environment and is not committed.
- [ ] Logout fully clears the session; protected pages become inaccessible.
- [ ] A tampered session cookie does not authenticate anyone.
- [ ] Every note query is filtered by the session user's id; all three write routes verify ownership.
- [ ] All data-changing routes are POST-only; GET cannot create, edit, or delete anything.
- [ ] Every SQL statement uses parameters; no string concatenation with user input anywhere.
- [ ] All user input is validated server-side (lengths, types, allowed values, reference existence).
- [ ] User text is escaped on output; `|safe` appears nowhere it could affect user or dataset text.
- [ ] Error pages reveal no traceback, path, query, or schema information.
- [ ] The README contains an honest statement of what is and is not protected (CSRF, rate limiting,
      password reset, etc.).

### 19.4 UI and error handling

- [ ] Consistent navigation on every page showing login state.
- [ ] Feedback messages for register, login, logout, save, edit, delete, and errors.
- [ ] Empty states for no notes, no results, and empty search.
- [ ] Destructive actions are visually distinct and require confirmation.
- [ ] Forms have labels, sensible input types, and errors next to the relevant field.
- [ ] Layout works at 375px and desktop widths.
- [ ] Keyboard-only navigation reaches and operates every control.
- [ ] Core features work with JavaScript disabled (tested, not assumed).
- [ ] No console errors and no missing static assets.
- [ ] Reading column is comfortable and verse numbers are visually clear.

### 19.5 Code organisation

- [ ] Templates contain no SQL and no authorization decisions.
- [ ] All database access is behind a small number of helpers using parameters.
- [ ] `bible.py` has no Flask dependencies and can be imported by a plain script.
- [ ] No view function is doing several unrelated jobs.
- [ ] No dead code, no commented-out experiments, no leftover debug prints.
- [ ] Names are consistent: one spelling for each column, session key, template variable, and slug.
- [ ] The four naming decisions from §5.3 are documented and actually followed.

### 19.6 Testing and documentation

- [ ] Test log exists, is committed, and covers every item in §11.
- [ ] Regression pass completed after the last change.
- [ ] Cold start from an empty database tested.
- [ ] Bugs found and fixed are recorded (for your README and video).
- [ ] README follows §20's outline and includes run instructions.
- [ ] README instructions verified from a clean clone.
- [ ] Data source and licence noted in the README.
- [ ] Design decisions and limitations documented.

### 19.7 Git and deployment

- [ ] `git status` clean; history tells a coherent story.
- [ ] No secrets, DB files, virtual environments, or scratch files committed.
- [ ] Commit messages are meaningful.
- [ ] Submission state tagged or recorded.
- [ ] Deployed app works (or a documented alternative the grader can run).
- [ ] Debug mode off in the deployed instance; secrets from the environment.
- [ ] Full §11 checklist passed on the deployed instance.

### 19.8 Explainability (the real test)

- [ ] You can explain every file's purpose without opening it.
- [ ] You can explain every table, column, and constraint.
- [ ] You can explain why the Bible is not in the database.
- [ ] You can explain how search works, including normalization and the cap.
- [ ] You can explain exactly what protects one user's notes from another.
- [ ] You can demonstrate the entire application without notes and without AI.

---

## 20. CS50 Final Project Requirements

This section is your submission outline — it tells you *what to prepare*, not what to write. Fill in your
own content.

### 20.1 What CS50 asks for, mapped to your project

| Requirement | What you must produce | Where it lives in your project |
| --- | --- | --- |
| Source code | Complete, runnable application | The repository root |
| A way to run it | Exact commands for a stranger | `README.md` "How to run" |
| A demonstration | A short video showing the app working | Your video |
| Explanation | What it is, why you built it, how it works | README + video narration |
| Design decisions | The choices you made and their trade-offs | README "Design decisions" |
| Technologies used | The stack and why each piece is there | README "Technologies" |
| Challenges | The hard parts and how you solved them | README "Challenges" |
| What you learned | The concepts you now understand | README + video reflection |
| Future improvements | Honest, concrete next steps | README "Future improvements" |

### 20.2 README outline (write your own content)

1. **Title** and a one-sentence description.
2. **What it is / what it does** — the three problems it solves (§1).
3. **Screenshots or a link** — one image of the reader and one of the notes flow is enough.
4. **Features** — list required features F1–F12 with one line each; mark optional features as extras.
5. **Technologies** — Python, Flask, SQLite, Jinja, HTML/CSS, Bootstrap, vanilla JavaScript, and why
   each is present (for example: *no framework because the pages are server-rendered*).
6. **Data** — where the KJV text came from, its structure conceptually, and the public-domain note (§7.1).
7. **Architecture** — a short description plus the diagram from §4.2 (draw your own version).
8. **Database** — your two tables, their columns, and the relationship. Include your one-note-per-verse
   decision.
9. **Design decisions and trade-offs** — for example: Bible in JSON not SQLite; slugs as identifiers;
   search normalization and match rules; server-rendered pages with optional JavaScript; capped search
   results.
10. **Security** — hashed passwords, sessions, parameterized queries, owner-filtered notes, escaped
    output, POST-only writes, and an honest statement of limits.
11. **How to run** — create a virtual environment, install dependencies, create the database from the
    schema, run the app, open the URL. Include the exact commands for your OS.
12. **How to use** — the 30-second tour: register, read, search, add a note, find it again.
13. **Testing** — what you tested and how (a summary; the full log can be a separate file).
14. **Challenges and what I learned** — three or four specific items with the fix and the concept behind
    it. Be concrete: "my next-chapter navigation skipped a chapter because I mixed 1-based verse numbers
    with 0-based list indices."
15. **Limitations** — no password reset, no CSRF token (if applicable), no multi-translation support.
16. **Future improvements** — only items from §18.2/§18.3, stated as concrete steps.
17. **Acknowledgements** — dataset source, any CS50 material, and any AI assistance you used (see §22).

### 20.3 Demonstration video outline (content, not script)

- [ ] Show the app running at its URL, with the terminal visible for a moment.
- [ ] Walk the full core loop once, unhurried: books list → chapter → read → search → jump to a result.
- [ ] Register a new account live, then log in and log out.
- [ ] Read a chapter, add a note to a specific verse, show it attached to that verse.
- [ ] Go to My Notes, edit the note, then delete it after confirming.
- [ ] Show the database being real: create a note, then run a quick SELECT in the terminal and show the
      new row (and the hashed password for a user).
- [ ] Show one failure handled well: invalid chapter in the URL, and a timestamped/HTML-injection string
      in a note body rendering as text.
- [ ] Show the code briefly — only the parts you want to explain: the search function, the ownership
      filter, the schema.
- [ ] State the trade-offs you made and one thing you would do differently.
- [ ] Keep it short and dense: every second should show something working or explain something real.

### 20.4 Submission checklist

- [ ] Repository complete and pushed.
- [ ] README complete and verified against a clean clone.
- [ ] `requirements.txt` complete.
- [ ] Data file committed (or clearly documented with instructions to obtain it).
- [ ] No secrets, no DB file, no virtual environment in the repo.
- [ ] Video recorded, reviewed once critically, and uploaded.
- [ ] Design decisions, challenges, and learning notes written down.
- [ ] §19 fully ticked.
- [ ] A personal note recorded of what you would do next.

---

## 21. Final Demonstration Plan

The demonstration must **prove** seven things. Design your sequence around the proof, not around a tour
of pages. Rehearse it twice before recording.

| # | What it proves | Demonstration step | What to say while doing it (ideas) |
| --- | --- | --- | --- |
| 1 | The application works | Open the deployed/local URL cold and load the books list | "This is a Flask app serving Jinja templates; the Bible text comes from a JSON file loaded once at startup" |
| 2 | Users can interact with the Bible | Open Genesis 1, scroll, use Next, jump to Revelation 22, open a single-chapter book | "Navigation is computed from the data, so boundaries are handled — here is the end of the Bible" |
| 3 | Search works | Search a common word, then a rare word, then a nonsense string | "Search is case-insensitive, normalized; results are capped and in canonical order — and here is the no-results state" |
| 4 | Authentication works | Register a new user live, log out, log back in, then try a protected page while logged out | "Passwords are stored only as a slow hash; the session is a signed cookie holding just the user id" |
| 5 | Notes work | Click a verse, write a note, see it attached; then edit it, then delete it | "A note stores the owner, the reference and the text; the verse now shows my note" |
| 6 | The database is really used | Create a note, then run a SELECT in the terminal and show the new row; show the hashed password column | "This is the SQLite file — here is my user row with a hash, here is the note row with my user id" |
| 7 | The project demonstrates CS50 concepts | Show the schema file briefly, then the ownership filter in the notes query, then the search function | "This WHERE clause is the whole privacy model; this index is why lookups are instant; this is where the algorithm lives" |

### 21.1 Two-account proof (the most convincing 60 seconds)

1. Log in as user A, add a note to a verse.
2. Log out, log in as user B.
3. Open the same chapter: B sees **no** note from A.
4. Copy A's note edit URL and paste it while logged in as B: it fails.
5. Log back in as A: the note is intact.

Prepare this in advance, and state the conclusion: *"Notes are private because every query filters by the
session user's id — not because the button is hidden."*

### 21.2 Failure-handling proof

- Type an invalid chapter in the URL and show the friendly 404.
- Submit an empty search and show the message.
- Enter a note body containing a script tag and show it rendering as visible text.

### 21.3 Sequencing advice

- Order the demo so the app is always in a working state between segments (log out cleanly before
  switching users).
- Do the database proof *after* creating fresh data, so the row is obviously new.
- Show the code only for the three or four things you want to be asked about — do not scroll through
  files.
- Keep a fallback: if the deployed instance misbehaves, have the local instance ready and simply say so.
- End with the honest trade-off statement and one future improvement. That is what a good engineer
  sounds like.

---

## 22. "Before You Ask AI" Rule

AI is your mentor, rubber duck, and reviewer. It is **not** the author of your project. If you cannot
explain a line in your submission, you have a problem that no amount of working code can fix — and you
will be asked about your code during evaluation.

### 22.1 The rules

1. **Attempt the problem first.** Try for at least 20–30 minutes. Write down what you tried and what you
   expected. Half of all bugs are solved by the act of writing this down.
2. **Explain the problem before asking for anything.** State what you are trying to do, what you
   expected, what happened, and the smallest repro. A precise question usually answers itself.
3. **Ask for concepts before code.** "Explain how Flask sessions work and what belongs in the session"
   teaches you something. "Write my login route" does not.
4. **Ask for review, not replacement.** Paste your code and ask what is wrong, unsafe, or unclear. Then
   rewrite it yourself, in your own structure and words.
5. **Ask for hints before solutions.** "Which layer is this likely to be in, and how would I verify
   that?" is almost always better than being handed a fix.
6. **Read the error message before asking.** If you still need help, include it verbatim, with the file
   and line it points to.
7. **Never paste code you cannot explain.** If AI writes something, you must be able to narrate it line
   by line, out loud, before it goes into the project.
8. **Never let AI make security decisions for you.** Understand *why* passwords are hashed, *why* the
   owner filter exists, and *why* queries are parameterized. If you cannot explain it, you cannot defend
   it.
9. **Keep an AI log.** One line per use: what you asked, what you learned, what you changed. Useful for
   your README's acknowledgements, and it keeps you honest about how much was yours.
10. **Never ask AI to finish the project.** The point is that *you* build it. Use AI where you are stuck,
    blocked, or want a critical second opinion.
11. **Never ask AI to write your README or video narration verbatim.** Bullet points you write and then
    speak about are always stronger than text you did not compose.
12. **Verify everything AI tells you against the running app.** Library APIs change — Flask 3 removed
    hooks that old tutorials still use, and password-hashing defaults differ between versions. If a
    suggestion does not work, find out why; that investigation is the learning.

### 22.2 Good questions vs weak questions

| Weak | Strong |
| --- | --- |
| "Write a Flask route for notes." | "I have a notes table with a user_id column. Explain how to make sure only the owner can edit a note, and how I should test that." |
| "Why doesn't my code work?" | "This function returns an empty list for 'love' but a match for 'love.' — here is the function and the data shape; which layer should I check first?" |
| "Fix my template." | "My page renders blank where the verse list should be. Here is the render call and the template block. What is the most likely name mismatch?" |
| "Add login." | "I want to store only the user id in the session. Explain what a signed cookie protects against and what it does not." |
| "Is this secure?" | "Here is my notes query and my ownership check. What inputs could bypass it, and how would I test that?" |

### 22.3 The understanding test (use it constantly)

Before moving on from any AI-assisted area, answer these out loud:

- [ ] What does this code do, step by step?
- [ ] Why is it written this way rather than another way?
- [ ] What would break if I deleted this line or changed this value?
- [ ] How would I test that it works?
- [ ] Could I rewrite it from scratch tomorrow?

If you cannot answer all five, the code is not yours yet: delete it and rebuild it yourself.

### 22.4 Honest acknowledgement

If AI helped you understand a concept or debug a problem, say so in your README — one sentence is
enough. What you must never do is claim authorship of code you cannot explain. Mentors respect a student
who says *"I did not understand sessions, so I studied them and rewrote my login logic twice"* far more
than one who submits code they cannot defend.

---

## 23. Final "Definition of Done"

The project is finished **only** when every statement below is true. This is a hard gate, not a
guideline.

### 23.1 Product

- [ ] All twelve required features (F1–F12) work in the deployed or documented environment.
- [ ] Every book and chapter of the dataset can be read, including the first, the last, and
      single-chapter books.
- [ ] Search returns correct, deterministic results and handles empty and no-match queries.
- [ ] A user can register, log in, log out, and stays logged in as expected.
- [ ] A user can create, view, edit, and delete notes attached to specific verses.

### 23.2 Safety and correctness

- [ ] Passwords are stored only as hashes; no plaintext password exists anywhere.
- [ ] Every note read/write is filtered by the session user's id, verified with two accounts.
- [ ] Invalid input anywhere (book, chapter, verse, form fields, query string, unknown URL) produces a
      friendly response with a correct status code — never a traceback.
- [ ] All SQL uses parameters; all user text is escaped on output.
- [ ] Data-changing actions are POST-only.
- [ ] Data persists across restarts, and the database recreates from `schema.sql`.

### 23.3 Quality

- [ ] The schema is documented and enforced (keys, uniqueness, foreign keys, not-null).
- [ ] The UI is usable: consistent navigation, clear feedback, empty states, works at narrow widths and
      without JavaScript.
- [ ] The code is organised per §5: routes, helpers, Bible domain, templates, static.
- [ ] No dead code, no leftover debug output, no committed secrets or database files.
- [ ] The test log covers §11, and every recorded failure was fixed or documented as an accepted
      limitation.

### 23.4 Understanding and submission

- [ ] You can explain every major component: the request lifecycle, the data layer, search, the schema,
      sessions, and the authorization model.
- [ ] You can demonstrate the entire application — including the two-account privacy proof and one
      invalid-input case — without notes and without AI.
- [ ] The README lets a stranger run the project and understand its design decisions and limitations.
- [ ] The demonstration video shows the application working, the database being used, and the concepts
      you want credit for.
- [ ] §19 and §20.4 are fully ticked.
- [ ] You have recorded what you learned and what you would do next.

> **Small project. Real engineering. Deep understanding.**
>
> When all of the above is true, you are done — and you have something you can genuinely explain,
> which is the only thing that ultimately matters.
