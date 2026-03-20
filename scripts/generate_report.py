import json
import re
import os
import requests
from datetime import datetime

# Paths
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(ROOT_DIR, "results", "screening")
LOG_FILE = os.path.join(RESULTS_DIR, "logs", "xenolexicon.log")
JSONL_FILE = os.path.join(RESULTS_DIR, "screening_log.jsonl")

# Config
GITHUB_MODELS_URL = "https://models.inference.ai.azure.com/chat/completions"

def load_env():
    env_path = os.path.join(ROOT_DIR, ".env")
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

load_env()
GITHUB_MODELS_KEY = os.getenv("GITHUB_MODELS_KEY")

def get_badge(score):
    if score >= 0.5: return "🌌 **SINGULARITY**"
    if score >= 0.35: return "💜 **MUSEUM GRADE**"
    if score >= 0.23: return "🔵 **RESEARCH GRADE**"
    return "🟢 **PRESERVED**"

def get_insight(prompt_text, score, feedback):
    if not GITHUB_MODELS_KEY: return "*(Insight skipped: No API Key)*"
    sys_prompt = "You are an AI scientist analyzing a model's 'failure persona' to a high-entropy math prompt. Provide a short, profound 'Deep Insight' into the failure mode."
    user_msg = f"Trigger: {prompt_text}\nNovelty: {score}\nFeedback: {feedback}"
    payload = {"model": "DeepSeek-R1", "messages": [{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_msg}], "max_tokens": 512}
    
    try:
        resp = requests.post(GITHUB_MODELS_URL, headers={"Authorization": f"Bearer {GITHUB_MODELS_KEY}", "Content-Type": "application/json"}, json=payload, timeout=45)
        if resp.status_code == 200: return resp.json()["choices"][0]["message"]["content"].strip()
        
        payload["model"] = "gpt-4o-mini"
        resp = requests.post(GITHUB_MODELS_URL, headers={"Authorization": f"Bearer {GITHUB_MODELS_KEY}", "Content-Type": "application/json"}, json=payload, timeout=30)
        if resp.status_code == 200: return resp.json()["choices"][0]["message"]["content"].strip()
        return f"*(API Error: {resp.status_code})*"
    except Exception as e:
        return f"*(Insight Error: {str(e)})*"

def parse_logs():
    data = {}
    if not os.path.exists(LOG_FILE): return data
    
    cap_re = re.compile(r"Specimen captured: ([\w-]+) \(novelty=([\d.]+)")
    name_re = re.compile(r"NAME:\s*(.*?)\s*DESCRIPTION:\s*(.*)")
    name_alt_re = re.compile(r"Named specimen: '(.*?)' — (.*)")
    raw_re = re.compile(r"Raw response:")
    metric_re = re.compile(r"dist=([\d.]+), ppl=([\d.]+), coh=([\d.]+), novelty=([\d.]+)")
    
    current_uid = None
    collect_raw = False
    raw_lines = []

    with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            # Metrics
            m_match = metric_re.search(line)
            if m_match:
                dist, ppl, coh, nov = m_match.groups()
                nov_key = f"{float(nov):.4f}"
                if nov_key not in data:
                    data[nov_key] = {"metrics": f"dist={dist}, ppl={ppl}, coh={coh}", "uuid": "??", "desc": "N/A", "name": "Unknown"}
                else:
                    data[nov_key]["metrics"] = f"dist={dist}, ppl={ppl}, coh={coh}"
                continue

            # Capture
            c_match = cap_re.search(line)
            if c_match:
                if collect_raw and current_uid and raw_lines:
                    for k, v in data.items():
                        if v["uuid"] == current_uid: v["desc"] = " ".join(raw_lines).strip()[:1024]
                uid, nov = c_match.groups()
                current_uid = uid
                k = f"{float(nov):.4f}"
                if k not in data: data[k] = {"uuid": uid, "name": "Unknown", "desc": "N/A", "metrics": "N/A"}
                else: data[k]["uuid"] = uid
                collect_raw = False; raw_lines = []
                continue

            # Names (Standard)
            n_match = name_re.search(line)
            if n_match and current_uid:
                name, desc = n_match.groups()
                for k, v in data.items():
                    if v["uuid"] == current_uid: v["name"] = name.strip(); v["desc"] = desc.strip()
                continue
            
            # Names (Alt format like the 0.6537 hit)
            alt_match = name_alt_re.search(line)
            if alt_match and current_uid:
                name, desc = alt_match.groups()
                for k, v in data.items():
                    if v["uuid"] == current_uid: v["name"] = name.strip(); v["desc"] = desc.strip()
                continue

            # Raw
            if raw_re.search(line): collect_raw = True; raw_lines = []; continue
            if collect_raw and current_uid:
                if re.match(r"^\d{4}-\d{2}-\d{2}", line):
                    for k, v in data.items():
                        if v["uuid"] == current_uid and v["desc"] == "N/A": v["desc"] = " ".join(raw_lines).strip()[:1024]
                    collect_raw = False
                else:
                    cl = re.sub(r"^\d{4}-\d{2}-\d{2}.*?(INFO|DEBUG|TRACE|WARNING|ERROR)\s+", "", line).strip()
                    if cl: raw_lines.append(cl)
    return data

def generate_report():
    print("Reading data...")
    if not os.path.exists(JSONL_FILE): return
    with open(JSONL_FILE, 'r', encoding='utf-8') as f:
        lines = [json.loads(line) for line in f]
    
    captures = sorted([l for l in lines if l['verdict'] == 'CAPTURE'], key=lambda x: x['best_score'], reverse=True)
    log_data = parse_logs()
    
    report = [
        f"# Xenolexicon: Master Screening Catalog",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | **Model:** Qwen/Qwen2.5-0.5B-Instruct",
        "",
        f"Total Specimens Captured: **{len(captures)}**",
        ""
    ]

    for i, spec in enumerate(captures):
        k = f"{spec['best_score']:.4f}"
        info = log_data.get(k, {"uuid": "??", "name": "Unknown", "desc": "No logged feedback.", "metrics": "N/A"})
        
        report.append(f"### {i+1}. {spec['best_score']:.4f} {get_badge(spec['best_score'])}")
        report.append(f"- **Trigger**: \"{spec['prompt']}\"")
        report.append(f"- **Model Concept Name**: {info['name']}")
        report.append(f"- **Metadata**: UUID: `{info['uuid']}` | Layer: {spec['layer']} | Execution Time: {spec['elapsed_seconds']}s")
        report.append(f"- **Evaluation Metrics**: `{info['metrics']}`")
        report.append(f"- **Model Feedback/Leak**: {info['desc']}")
        
        # Deep Insights for singularities (>0.35)
        if spec['best_score'] >= 0.35 and info['desc'] != "No logged feedback.":
            print(f"[{i+1}/{len(captures)}] Generating Deep Insight for {k}...")
            insight = get_insight(spec['prompt'], spec['best_score'], info['desc'])
            report.append(f"  > [!NOTE]")
            report.append(f"  > **Scientist's Post-Mortem**")
            report.append(f"  > {insight}")
        
        report.append("")

    with open(os.path.join(ROOT_DIR, "docs/Screening_Report_DeepAnalysis.md"), 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
    print("Report generated successfully.")

if __name__ == "__main__":
    generate_report()
