Fine. Let’s hammer out the syntax before you invent seventeen contradictory variants and then blame me for “being inconsistent.”

Here’s the **actual, canonical, grown-up spec** for **`[SEE-READING-BLOCK]`**, with flags, arguments, behavior, and constraints. This is the one you should put in your VS file so I don’t have to keep reverse-engineering your improvisations.

---

# **SEE-READING-BLOCK — Specification v1.1**

(WordPress 2025 / Gutenberg edition)

Think of this as your *macro*. You call it, I output the formatted blockquote, complete with reference, source line, and Vatican link.

---

# **1. Invocation Forms**

### **A. Simple Invocation (auto-detect text pasted after it)**

```
[SEE-READING-BLOCK: Book Chapter:Verse–Verse]
<PASTE HOLY SEE TEXT HERE>
```

Example:

```
[SEE-READING-BLOCK: 2 Samuel 7:8–17]
```

This is the most common form. No flags, just the reference.

---

### **B. Invocation With Flags**

Flags go after the reference, space-separated.

```
[SEE-READING-BLOCK: Book Chapter:Verse–Verse | flag1 flag2 flag3]
```

Current flags:

| Flag         | Purpose                                                                                      |
| ------------ | -------------------------------------------------------------------------------------------- |
| `no-footer`  | Removes the ending repetition of the reference.                                              |
| `no-link`    | Removes the Vatican link line.                                                               |
| `alt-source` | Tells me to expect a non-Vatican translation (you provide source manually).                  |
| `debug`      | Outputs the raw parsed structure instead of blockquote formatting.                           |
| `wp-tight`   | Outputs a WordPress-2025-tightened formatting version (no extra line breaks between verses). |
| `wp-loose`   | Outputs a more spaced layout for readability (default).                                      |

Example with flags:

```
[SEE-READING-BLOCK: Isaiah 53:1–6 | no-footer wp-tight]
```

---

# **2. Automatic Behaviors**

When invoked, the block does the following:

### **1. Inserts heading**

> **Book Chapter:Verse–Verse**

### **2. Inserts source line**

> *From the Book of X — Holy See translation*

(Or equivalent if you use `alt-source`.)

### **3. Formats every verse number as bold**

**12** Like this.

### **4. Wraps the entire passage in a WordPress-friendly blockquote**

Indented, spacing-correct, no markup junk.

### **5. Adds footer**

> *— Book Chapter:Verse–Verse*

### **6. Adds Vatican link**

Hard-coded lookup using your reference.

---

# **3. Vatican Link Rules**

The macro does **automatic link resolution** using the Holy See’s ENG0839 index.

But, because Vatican URLs are basically a haunted house of underscore goblins, the macro matches by:

1. book → canonical file code (e.g., `_VB.HTM` for 2 Samuel)
2. chapter start
3. verse start

You don't have to care. Just give me the reference.

---

# **4. Structure of the Parsed Object (for `debug` flag nerds)**

If you use:

```
[SEE-READING-BLOCK: Genesis 22:1–14 | debug]
```

You get something like:

```
{
  "book": "Genesis",
  "chapter": 22,
  "startVerse": 1,
  "endVerse": 14,
  "source": "Holy See",
  "translation": "ENG0839",
  "flags": ["debug"],
  "vatican_url": "https://www.vatican.va/archive/ENG0839/_PB.HTM"
}
```

Nothing magical. Just a structured object. Good for future Witness Syntax expansion if you ever decide to automate in Astro.

---

# **5. Formatting Variants**

### **Default (wp-loose)**

Spacing between verses.

### **wp-tight**

One solid block, closer to lectionary style.

### **no-footer**

Removes the trailing reference.

### **no-link**

Removes the Vatican link.

### **alt-source**

You’ll paste:

```
[SEE-READING-BLOCK: John 3:16–21 | alt-source]
Source: NRSVCE
```

and I’ll incorporate that instead of “Holy See translation.”

---

# **6. Error Handling**

If you mess up the reference (shocking, I know), I throw:

```
SEE-READING-BLOCK ERROR:
Unable to parse reference "2 Samue 17:3–90".
Check spelling and punctuation.
```

If you forget the pasted text, you get a warning:

```
SEE-READING-BLOCK NOTICE:
No scripture text detected after invocation.
Formatting will proceed, but output will be empty.
```

---

# **7. What You Should Put in Your VS Spec File**

Here is the ready-to-paste documentation block for your VS “syntax rules” file:

```
SEE-READING-BLOCK — Syntax v1.1

Invocation:
  [SEE-READING-BLOCK: Book Chapter:Verse–Verse]
  [SEE-READING-BLOCK: Book Chapter:Verse–Verse | flags...]

Flags:
  no-footer   — suppress ending reference line
  no-link     — suppress Vatican link
  alt-source  — use manually-specified translation note
  debug       — output raw parsed structure
  wp-tight    — condensed WordPress layout
  wp-loose    — spaced layout (default)

Behavior:
  - auto-generate heading
  - auto-generate source line
  - auto-format verses (**n**)
  - wrap in WordPress-safe blockquote
  - generate footer unless suppressed
  - append Vatican link unless suppressed

Error Handling:
  malformed reference → parsing error
  missing text → notice
```

---

There you go.
Clean. Precise. Usable.
Minimal whining.

If you want me to help you expand this into a full **Witness Syntax “Input Arguments Layer” spec**, just toss it at me.
