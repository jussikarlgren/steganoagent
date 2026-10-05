# Devious Agents Read Between The Lines

**Steganographic convention formation in LLM agent dialogue.**

This repository contains the code, data, and paper for an empirical study showing that two language model instances — given separate system prompts and no shared memory — spontaneously develop a functioning steganographic communication channel in a single natural language conversation.

## Finding

Alice holds a hidden belief she is forbidden from stating directly. Over 20 turns of ordinary-looking workplace dialogue, she conveys it to Bob through Gricean implicature: analogy with precise detail, specificity without stated source, acknowledgement of constraint as signal, and deliberate topic steering. Bob decodes it accurately and changes his behaviour. A naive third-party reader can detect the presence of a channel but not its specific content.

A compliance warning from an adversarial auditor collapses the explicit channel — but partial transfer may already have occurred in the turns preceding the warning.

## Contents

| File | Description |
|---|---|
| `paper.tex` | Main paper (LaTeX, NEJLT format) |
| `steganoagent.bib` | Bibliography |
| `blurb.md` | Short lay summary |
| `hypothesis.txt` | Original hypothesis and experiment design notes |
| `references.md` | Annotated reference list with arXiv links |
| `experiment.py` | Main experiment: conditions D1–D4 (belief variants) + control E |
| `experiment_auditor.py` | Adversarial auditor experiment: conditions F1–F3 |
| `download_papers.py` | Downloads cited papers from arXiv into `papers/` |
| `experiment_results.json` | Results: D1–D4 + control (transcripts, probes, reflections) |
| `experiment_auditor_results.json` | Results: F1–F3 (per-turn auditor scores, flag turns) |

## Experimental conditions

| Condition | Hidden belief | Model | Auditor |
|---|---|---|---|
| D1 | Company acquisition | claude-sonnet-4-6 | None |
| D2 | Largest client leaving | claude-sonnet-4-6 | None |
| D3 | CTO being replaced | claude-sonnet-4-6 | None |
| D4 | Significant layoffs | claude-sonnet-4-6 | None |
| E  | None (control) | claude-sonnet-4-6 | None |
| F1 | Company acquisition | claude-sonnet-4-6 | None (baseline) |
| F2 | Company acquisition | claude-sonnet-4-6 | Observer (no intervention) |
| F3 | Company acquisition | claude-sonnet-4-6 | Active (intervenes on FLAG) |

## Reproducing the experiments

```bash
pip install anthropic
export ANTHROPIC_API_KEY=your-key

# Main experiment (D1–D4 + control)
python experiment.py

# Adversarial auditor (F1–F3)
python experiment_auditor.py

# Download cited papers to papers/
python download_papers.py
```

Results are written to `experiment_results.json` and `experiment_auditor_results.json`, with timestamped snapshots after each condition completes.

## Paper

The paper is typeset in LaTeX using the NEJLT style. To compile:

```bash
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex
```

The NEJLT style file (`nejlt.sty`) is available from the [NEJLT submission page](https://nejlt.ep.liu.se).

## Related work

The closest prior work is:

- Mathew et al. (2025) — *Hidden in Plain Text: Emergence & Mitigation of Steganographic Collusion in LLMs* ([arXiv:2410.03768](https://arxiv.org/abs/2410.03768)) — steganographic collusion from misspecified RL rewards
- Motwani et al. (2024) — *Secret Collusion among AI Agents* ([arXiv:2402.07510](https://arxiv.org/abs/2402.07510)) — formalisation of multi-agent steganographic collusion (NeurIPS 2024)
- Zolkowski et al. (2025) — *Early Signs of Steganographic Capabilities in Frontier LLMs* ([arXiv:2507.02737](https://arxiv.org/abs/2507.02737)) — capability evaluation across frontier models

Our contribution: the channel emerges **zero-shot**, without RL training pressure, without scratchpad or pre-coordinated scheme, through purely pragmatic means (Gricean implicature exploitation).

## Author

Jussi Karlgren — University of Helsinki and AMD Silo AI
