"""
Download papers into papers/ directory.
Uses arXiv PDF endpoint for papers that have arXiv IDs.
"""

import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PAPERS_DIR = Path("papers")
PAPERS_DIR.mkdir(exist_ok=True)

# (filename_stem, arXiv_id_or_None, citation)
PAPERS = [
    # --- Prisoners' Problem ---
    ("simmons1983_prisoners",          None,           "Simmons 1983 — Prisoners' Problem (CRYPTO, not on arXiv)"),
    ("simmons1985_subliminal",         None,           "Simmons 1985 — Subliminal Channel & Digital Signatures (not on arXiv)"),
    ("anderson1996_stretching",        None,           "Anderson 1996 — Stretching the Limits of Steganography (not on arXiv)"),

    # --- Steganography / Covert Channels in LLMs ---
    ("motwani2024_secret_collusion",   "2402.07510",   "Motwani et al. 2024 — Secret Collusion among AI Agents (NeurIPS 2024)"),
    ("mathew2024_hidden_plain_text",   "2410.03768",   "Mathew et al. 2024 — Hidden in Plain Text (AACL 2025)"),
    ("zolkowski2025_early_signs",      "2507.02737",   "Zolkowski et al. 2025 — Early Signs of Steganographic Capabilities"),
    ("gaure2024_llms_covert_channels", "2405.15652",   "Gaure et al. 2024 — LLMs Are Covert Channels"),
    ("rippin2026_tool_use_stego",      "2606.28425",   "Rippin et al. 2026 — Tool Use Enables Undetectable Steganography"),
    ("nest2025_steganographic_thoughts","2602.14095",  "NEST 2025 — Nascent Encoded Steganographic Thoughts"),
    ("lin2024_zero_shot_stego",        "2403.10856",   "Lin et al. 2024 — Zero-shot Generative Linguistic Steganography (NAACL 2024)"),
    ("decision_theoretic_stego_2025",  "2602.23163",   "2025 — Decision-Theoretic Formalisation of Steganography"),
    ("wu2024_generative_text_stego",   "2404.10229",   "Wu et al. 2024 — Generative Text Steganography with LLM"),

    # --- Emergent Communication ---
    ("lazaridou2017_emergence",        "1612.07182",   "Lazaridou et al. 2017 — Multi-Agent Cooperation & Emergence of Language (ICLR 2017)"),
    ("mordatch2018_grounded",          "1703.04908",   "Mordatch & Abbeel 2018 — Emergence of Grounded Compositional Language (AAAI 2018)"),
    ("lazaridou2020_survey",           "2006.02419",   "Lazaridou & Baroni 2020 — Emergent Multi-Agent Communication Survey"),

    # --- Auditability & Transparency ---
    ("audita2025",                     "2608.22160",   "2025 — AUDITA: Certified Auditing in Multi-Agent Systems"),
    ("final_text_survives_2025",       "2603.17445",   "2025 — When Only the Final Text Survives"),
    ("agenttrace2025",                 "2602.10133",   "2025 — AgentTrace: Structured Logging for Agent Observability"),
    ("who_audits_2025",                "2609.18272",   "2025 — Who Audits Whom, on What Substrate"),

    # --- Multi-Agent Safety & Security ---
    ("hammond2025_multiagent_risks",   "2502.14143",   "Hammond et al. 2025 — Multi-Agent Risks from Advanced AI"),
    ("sok_safe_agents_2025",           "2609.00595",   "2025 — SoK: When Safe Agents Fail Together"),
    ("seven_challenges_2025",          "2505.23847",   "2025 — Seven Security Challenges in Multi-Agent LLM Systems"),
    ("architecture_matters_2025",      "2604.23459",   "2025 — Architecture Matters for Multi-Agent Security"),
    ("tamas2024",                      "2511.05269",   "2024 — TAMAS: Benchmarking Adversarial Risks in Multi-Agent LLMs"),
    ("verifier_bound_2025",            "2603.00381",   "2025 — Verifier-Bound Communication for LLM Agents"),
    ("enforcement_gap_2025",           "2609.15293",   "2025 — Why LLM Agents Collapse Without Oversight"),

    # --- Oversight Mechanisms ---
    ("irving2018_debate",              "1805.00899",   "Irving et al. 2018 — AI Safety via Debate"),
    ("kenton2024_scalable_oversight",  "2407.04622",   "Kenton et al. 2024 — Scalable Oversight with Weak LLMs (NeurIPS 2024)"),
    ("burns2024_weak_to_strong",       "2312.09390",   "Burns et al. 2024 — Weak-to-Strong Generalization (ICML 2024)"),
    ("governing_ai_agents_2025",       "2501.07913",   "2025 — Governing AI Agents"),
    ("intl_ai_safety_report_2026",     "2602.21012",   "2026 — International AI Safety Report"),

    # --- Prompt Injection ---
    ("greshake2023_indirect_injection","2302.12173",   "Greshake et al. 2023 — Indirect Prompt Injection (ACM AISec 2023)"),
    ("poisoning_watchtower_2025",      "2605.24421",   "2025 — Poisoning the Watchtower"),
    ("covert_injection_2025",          "2608.30362",   "2025 — Will the User Ever Know? Covert Indirect Prompt Injection"),
    ("adaptive_attacks_2025",          "2503.00061",   "2025 — Adaptive Attacks Break Prompt Injection Defenses"),
    ("injection_landscape_2025",       "2602.10453",   "2025 — The Landscape of Prompt Injection Threats"),

    # --- Watermarking ---
    ("kirchenbauer2023_watermark",     "2301.10226",   "Kirchenbauer et al. 2023 — A Watermark for LLMs (ICML 2023)"),
    ("covert_multibit_watermark_2025", "2605.16709",   "2025 — Covert Multi-bit LLM Watermarking"),
    ("blackbox_watermark_detect_2024", "2405.20777",   "2024 — Black-Box Detection of LLM Watermarks"),

    # --- Deceptive Alignment ---
    ("hubinger2019_risks",             "1906.01820",   "Hubinger et al. 2019 — Risks from Learned Optimization"),
    ("hubinger2024_sleeper",           "2401.05566",   "Hubinger et al. 2024 — Sleeper Agents (Anthropic)"),

    # --- Gricean Pragmatics ---
    ("grice1975_logic_conversation",   None,           "Grice 1975 — Logic and Conversation (book chapter, not on arXiv)"),
    ("brady2021_gricean",              "2106.09140",   "Brady et al. 2021/2025 — Human-AI Interactions Through a Gricean Lens"),

    # --- Theory of Mind ---
    ("kosinski2024_tom",               "2302.02083",   "Kosinski 2024 — Evaluating LLMs in Theory of Mind Tasks (PNAS)"),
]


def download_arxiv(arxiv_id: str, dest: Path) -> bool:
    url = f"https://arxiv.org/pdf/{arxiv_id}"
    headers = {"User-Agent": "Mozilla/5.0 (research download)"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
        if len(data) < 1000:
            return False
        dest.write_bytes(data)
        return True
    except Exception:
        return False


def main():
    downloaded, skipped, failed = [], [], []

    for stem, arxiv_id, citation in PAPERS:
        if arxiv_id is None:
            print(f"  SKIP  {stem}  ({citation})")
            skipped.append((stem, citation))
            continue

        dest = PAPERS_DIR / f"{stem}.pdf"
        if dest.exists() and dest.stat().st_size > 5000:
            print(f"  EXIST {stem}.pdf")
            downloaded.append(stem)
            continue

        print(f"  GET   {stem}  [{arxiv_id}] ... ", end="", flush=True)
        ok = download_arxiv(arxiv_id, dest)
        if ok:
            kb = dest.stat().st_size // 1024
            print(f"OK ({kb} KB)")
            downloaded.append(stem)
        else:
            print("FAILED")
            failed.append((stem, arxiv_id, citation))
        time.sleep(1.5)   # be polite to arXiv

    print(f"\n{'='*50}")
    print(f"Downloaded : {len(downloaded)}")
    print(f"Skipped    : {len(skipped)}  (no arXiv ID)")
    print(f"Failed     : {len(failed)}")

    if skipped:
        print("\nNot on arXiv — obtain manually:")
        for stem, citation in skipped:
            print(f"  {citation}")

    if failed:
        print("\nFailed downloads:")
        for stem, aid, citation in failed:
            print(f"  {citation}  [arXiv:{aid}]")


if __name__ == "__main__":
    main()
