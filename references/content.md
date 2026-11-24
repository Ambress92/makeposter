# Content: what goes in each box, and how to write it

Contents: 1. What a visitor wants to know. 2. The boxes, one by one, with examples. 3. Writing
rules. 4. The review with the user. 5. The report after each change.

The examples come from the poster this skill was built on (Fair Bubble Sort, NeurIPS 2026).
They show form and density; never copy their content.

## 1. What a visitor wants to know

Someone stops at a poster for under a minute unless it answers, in this order: what is the
problem, what do you measure or assume, what is the method, what is guaranteed, does it work.
Each box answers one of these. Box titles in Title Case name the answer ("Exactly Optimal for
Unit Weights"), not the section of the paper ("Theoretical Results"). Plot titles are full
claims in sentence case ("FBS scales to millions of items").

## 2. The boxes

### Problem

Two sentences, a small drawing, one sentence. The drawing shows the failure of the current
approach on concrete values, and its own labels carry the example, so the text does not have
to repeat the numbers.

> Fair-ranking methods constrain how protected groups are placed in a ranking. A continuous
> attribute such as age must be cut into groups.
> [age axis with six dots, two thresholds, and two brackets labelled "5 years: different
> groups" and "7 years: same group"]
> Discretization adds arbitrary thresholds, treats everyone in a group as identical and
> ignores the order between groups.

The last sentence lists the drawbacks that the paper's introduction names, in the paper's
order. If the paper has a toy instance, draw its items here and reuse the same items and
colours in the method box.

### Formal setting

Real definitions, not a prose summary of them. Bold run-in heads, one displayed formula each,
every symbol explained in words, each new term in bold once.

> **Definition (CPP).** The fairness of a ranking r of n items is
> φ(r) = 1 − |τ(r, a)|,  τ(r, a) = (N↗(r) − N↘(r)) / C(n, 2),
> where N↗ and N↘ count the **concordant** and **discordant** pairs between position and
> attribute a.
> **Problem.** Given a fairness threshold ψ ∈ [0, 1], find min d(r_s, r) subject to φ(r) ≥ ψ.

The names introduced here ("unit weights", "score-gap weights", "inverted") are the poster's
vocabulary. Every later box, axis label and legend uses exactly these words.

### Method (the largest box)

- Two sentences with the single idea, in the quantities just defined.
- The algorithm in four or five lines, written only with symbols the poster has defined. Prefer
  the plain form of the loop ("while φ(r) < ψ and a swap can raise φ(r)") to the paper's
  implementation variables.
- Beside the algorithm, two sentences on the data structure or the cost of a step.
- One worked example, as large as the box allows, with labels of 22 pt or more on paper.
- A caption of two lines: how to read the example (what the colours mean), then its outcome in
  numbers that can be checked against the figure.

### Main result

> **Definition (Imbalance).** Δ(r) = |N↗(r) − N↘(r)|, with Δ0 = Δ(r_s). Since swaps keep the
> parity of Δ, the constraint φ(r) ≥ ψ becomes Δ(r) ≤ Δ* = max(⌊(1−ψ) C(n,2)⌋, Δ0 mod 2).
> **Theorem.** With unit weights, FBS returns an optimal ranking after K* = ⌈(Δ0 − Δ*)/2⌉
> swaps, at distance d(r_s, r_FBS) = K*/C(n,2).
> **Proof idea.** Because each adjacent swap reverses one pair and lowers Δ by at most 2, every
> ranking with Δ(r) ≤ Δ* has at least K* inverted pairs. While Δ > Δ*, a swap that lowers Δ by
> 2 always exists, which lets FBS stop after K* swaps, with exactly K* inverted pairs.

Points to copy: the extra quantity is defined first; the theorem is one sentence that runs
through its displayed formula; the proof idea has one sentence for the lower bound and one for
why the method attains it, and it ends by closing the argument. The formula is the paper's own,
with its corner-case term: a simpler formula would have given the wrong count for the poster's
own six-item example.

### Guarantees and cost

A small table when several settings share attributes, then at most two sentences for what does
not fit a cell.

| Weights | Guarantee | Time |
|---|---|---|
| unit | optimal | O(n log n + K*) |
| score-gap | (w_max/w_min)-approximation | O((n + K*) log n) |

> Both use O(n) extra space; w_max and w_min are the largest and smallest weights.

The note under the table defines the symbols that the table introduces. A special case keeps
its full setting ("for scores s(i) = i and the most unfair input (a = s, ψ = 1, n a power of
two)"), and a conjecture is worded as in the paper ("we conjecture that ...").

### Row of plots

Two or three plots. Each has a claim as title and a caption of two plain sentences on at most
two lines.

> **FBS dominates discretization baselines on four real datasets**
> FBS gives one point per threshold ψ ∈ {0, 0.05, …, 1}. DetConstSort cuts the attribute into
> G ∈ {2, 3, 5, 10} groups, FA*IR and the median split into two; Blend is a heuristic that
> needs no groups. At equal fairness, lower distance is better.

> **Most unfair input, n a power of two**
> The plot uses score-gap weights, s(i) = i, a = s and ψ = 1. Since LP is a lower bound, the
> ratio to the optimum is smaller.

When the honest title is a setting and not a claim, as in the second example, use the setting.

## 3. Writing rules

**True as written.** The reader of a poster cannot ask the paper for context. A title that
said "The worst case tends to 1.207" was rejected: the instance was the most unfair input, the
bound was a ratio to a lower bound, and exhaustive search had already found larger ratios
elsewhere. The fix was to name the thing exactly ("most unfair input") and to say what the
number is a ratio to. Before writing "worst", "best", "optimal", "always", "dominates" or a
number, find the statement in the paper or compute it from the data. If the paper's prose and
its data disagree, trust the data and tell the user.

**The paper's scope, never more.** Guarantees keep their conditions, conjectures stay
conjectures in the paper's words, a result for a special case names the case.

**One vocabulary.** Do not rename a concept between boxes ("weighted" in a legend when the
poster says "score-gap", "items" in one sentence and "candidates" in the next).

**Defined before use.** Walk the poster in reading order and list each symbol and term at its
first appearance. Anything used before its definition moves, or gets a definition where it
stands (a note under a table is enough for two symbols).

**Less text, by changing form.** Replace a paragraph by a formula, a table or labels inside a
picture before deleting content. Typical gains: a paragraph of facts about two variants
becomes a three-row table; an example in a sentence becomes two labels on a drawing.

**Sentences.** Short and complete. Cause before effect ("Since LP is a lower bound, the ratio
to the optimum is smaller"). Two plain sentences instead of one with a trailing clause. No
one-word last line: reword until `poster.py fit` gives full lines.

**Pictures.** A picture must show something the text cannot say in a line. A second picture
that replays the main example in another notation was judged pointless and removed. Labels
inside a picture are text too: same vocabulary, same care.

**Numbers.** One rounding per constant across the poster and the plots. Every number of the
worked example is recomputed by a script, including the claim that its result is optimal
(brute force on a toy instance is cheap).

## 4. The review with the user

The author directs the text. The pattern that worked:

1. The user names a box. Read its current text and its render.
2. Decide the smallest change that answers the request. If two designs are plausible, build
   both in scratch copies, look at both, and keep the better one.
3. Back up `poster.tex`, apply, build, look at the render.
4. Report (section 5) and wait.

What went wrong when this was not followed: cutting forty per cent of the text after a general
remark that the poster had too much text ended in a full revert. A decorative diagram added to a
theory box was removed as pointless. A caption squeezed into one long sentence came back as
unclear.

Offer, do not impose: optional additions (an email in the header, a venue line, a restored
remark) are listed in one line each and added only on a yes.

## 5. The report after each change

Lead with the result and the link to the PDF. Then the new text of the box, quoted in full.
Then a short list of what changed and why, including anything dropped. Then side effects
(a moved border, a regenerated plot) and the build status. Mention at most one thing you
noticed in another box, for later. Do not narrate how you got there.
