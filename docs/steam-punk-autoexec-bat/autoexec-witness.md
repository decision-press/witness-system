# Witness-System Autoexec (v0.1)

**File:** `docs/autoexec-witness.md`  
**Purpose:** Define a repeatable boot sequence for the operator + witness-system on a Linux box.  
**Scope:** Human discipline + directory structure + constructor usage. No magic.

---

## 0. Intent & scope check

Before touching the keyboard:

1. State today’s **primary intent** in one sentence.  
   - Example: “Clarify Pillar 3 protocols for collaboration” or “Work on Astro layout for public site.”
2. Confirm **this session is part of the witness-system** (not casual chat, not random browsing).
3. If the intent doesn’t belong in any pillar, do not start a witness session.

---

## 1. Environment

**Assumed environment:**

- OS: Linux
- Root repo: `~/Projects/witness-system` (or equivalent)
- Version control: `git`
- Editor: any (vim, nano, VS Code, etc.)

**Required directories (conceptual):**

- `constructor/` – canonical constructor text & versions  
- `pillars/` – pillar-specific docs, guides, workflows  
- `logs/` – transcripts, notes, session artifacts  
- `meta/` (optional) – governance, decisions, design notes  

Adjust naming to match the actual repo, but keep the roles stable.

---

## 2. Mode & color-state

The witness-system uses simple modes:

- **grey** – no pillar active; general/meta orientation only  
- **green** – a specific pillar is active and in-bounds  
- (Other colors may be defined later; green is the normal “in pillar” state.)

**Rule:**  
Do not mix pillars. One active pillar per session or sub-session.

---

## 3. Boot sequence (human ritual)

1. **Open terminal & set root**

   ```bash
   cd ~/Projects/witness-system
