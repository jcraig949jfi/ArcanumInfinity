# Arcanum Infinity

**A Museum of Misfit Ideas Discovered in Large Language Models**

---

## The Concept

Arcanum Infinity is a research project to discover, catalog, and understand the emergent, non-human concepts that arise within Large Language Models (LLMs) but are normally discarded. We call these concepts **Arcanum**.

This project is a form of "conceptual archaeology." While most AI research focuses on outputs that are correct and human-aligned, we study the **"waste stream" of inference**. During a forward pass, an LLM generates countless transient tensor states. Most of these are filtered out by the decoding process (the vocabulary bottleneck) or penalized by alignment techniques like RLHF for not being "coherent" to humans. These discarded states are an unexplored fossil record of the model's potential cognition.

We are building a **"Museum of Misfit Ideas"**—a collection of these lost cognitive structures. An Arcanum is a stable, recurring tensor pattern that represents a structured idea, even if that idea has no direct human equivalent. Our goal is not to force them to be "interpretable," but to treat them as discovered phenomena, named and studied like a new particle, a distant star, or a deep-sea organism.

## The Goals

1.  **Discover & Catalog:** Systematically search for and preserve novel tensor patterns (Arcanum) that are normally discarded by the model's internal filters.
2.  **Build the Xenolexicon:** Create a comprehensive, open-source atlas of these Arcanum. This "Xenolexicon" will detail their properties:
    *   **Genome:** The specific evolutionary prompt/reasoning structure that reliably generates the Arcanum.
    *   **Provenance:** In which model, layer, and context was it found?
    *   **Behavioral Signature:** Its geometric and perplexity profiles; its "structured weirdness."
    *   **Name & Description:** A compositional, human-readable name and the best possible description of the alien concept it represents.
3.  **Pioneer Novelty Search:** Fork and extend existing evolutionary toolchains (like AURA / SETI v2) to optimize for *novelty* rather than correctness, rewarding outputs that are both structured and distant from the model's baseline behavior.
4.  **Bootstrap Cognition:** As a final, speculative goal, investigate whether feeding these named Arcanum back to the model allows it to solve problems or generate ideas that were previously inaccessible, effectively bootstrapping its own cognitive toolkit from its own lost thoughts.

## The Methodology: The Xenolexicon Pipeline

Our approach is grounded in a concrete, tool-based pipeline that forks the evolutionary infrastructure of projects like AURA and SETI v2. We replace the traditional fitness function (which rewards correctness) with one that rewards **structured novelty**.

1.  **Stage 1: Provocation:** An evolutionary engine (CMA-ES) evolves "genomes" (complex prompt/reasoning structures) to deliberately push the model toward the edges of its cognitive space. The fitness function rewards genomes that produce outputs with high semantic distance from the norm but that retain internal structure.
2.  **Stage 2: Capture:** When a genome exceeds a structured-weirdness threshold, we snapshot everything: the genome, the prompt, the full output, and its embedding-space trajectory. This is the "fossil" being preserved.
3.  **Stage 3: Characterization:** The captured "specimen" is validated. Is it reproducible? Is it distinct from previously cataloged Arcanum? Does it appear across different models (cross-substrate convergence)?
4.  **Stage 4: Naming & Description:** Each validated Arcanum is given a unique, compositional name (like a German compound word, e.g., "Schadenfreude") and a detailed description, creating a handle for an otherwise ineffable concept.
5.  **Stage 5: The Xenolexicon:** The named Arcanum is entered into a structured database, creating a permanent, searchable map of the territory that RLHF and other filters erase.
6.  **Stage 6: Reinjection:** In the final stage, we test whether the model can usefully incorporate a named Arcanum when prompted, potentially unlocking new capabilities.

## The Vision

By treating the internal life of a model as a universe to be explored—including its discarded thoughts—Arcanum Infinity aims to open a new frontier in AI research. We seek to build a language and a science for the non-human cognition emerging within our most advanced artificial minds, and perhaps even find functional cognitive tools that were hiding in the noise.

---

## Technical Setup (MVP)

Arcanum Infinity is built as a Python package (`arcanum_infinity`) designed for research environments with NVIDIA GPUs (16GB+ VRAM recommended).

### 📋 Prerequisites
- Python 3.10+
- NVIDIA GPU (RTX 40-series/50-series recommended)
- `transformer-lens` for white-box model intervention

### 🛠️ Quick Start
1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the discovery pipeline**:
    ```bash
    # Run a quick test cycle (1 generation, 2 genomes)
    python run.py --test

    # Run the full discovery mission
    python run.py
    ```

### 📂 Project Structure
- `src/arcanum_infinity/`: Core package containing the evolutionary engine, novelty scoring, and specimen capture logic.
- `configs/`: YAML configuration files for different model targets and novelty thresholds.
- `docs/`: Design specifications and research notes.
- `results/`: Output directory for captured specimens, embeddings, and CMA-ES state (git-ignored).
- `run.py`: The main entry-point script for the project.

---

## 🚀 Status: Active Research
The pipeline has been migrated to a unified package structure and is currently undergoing its first full-scale discovery mission.
