# Xenolexicon: Evolutionary Discovery of Structured Novel Concepts in the Activation Space of Small Language Models

**Arcanum Infinity Research Group**

*Working Paper — Draft for Community Review*

*March 2026*

---

## Abstract

We present **Xenolexicon**, a system for the automated discovery, capture, and cataloging of structured novel tensor patterns—termed *Arcanum*—from the internal activation space of Large Language Models (LLMs). Unlike conventional interpretability research, which seeks to explain known model behaviors in human terms, Xenolexicon treats the model's intermediate representations as a search space for *emergent concepts* that may have no direct human analogue. We employ a modified evolutionary strategy (CMA-ES) to evolve provocation prompts that maximize a composite fitness function rewarding *structured novelty*: outputs that are simultaneously high in semantic distance from baseline behavior and high in internal coherence. We report results from inaugural runs on Qwen 2.5 0.5B across two consumer-grade NVIDIA GPUs (16 GB and 8.2 GB VRAM), demonstrating monotonically increasing novelty scores across four generations of evolution. We describe the six-stage Xenolexicon pipeline, analyze the dynamics of the evolutionary search including layer diversification behavior, and propose a **rapid genome screening** strategy that could dramatically accelerate specimen discovery by cycling through large banks of semantically diverse provocation prompts. The Xenolexicon database and tooling will be released as an open-source resource for the research community.

---

## 1. Introduction

The dominant paradigm in LLM interpretability research is reductive: researchers seek to identify and explain the internal mechanisms by which models produce their observed outputs. Mechanistic interpretability, probing classifiers, and representation engineering all share a common assumption—that the goal is to map the model's internal states onto *known human concepts*. This is valuable work, but it leaves a vast territory unexplored.

During every forward pass, an LLM generates a high-dimensional tensor state at each layer. The overwhelming majority of these states are never expressed as output tokens; they are either filtered by the vocabulary projection head (the "vocabulary bottleneck"), suppressed by sampling strategies (top-k, top-p), or actively penalized by alignment techniques such as RLHF and DPO. We refer to this discarded information as the model's "waste stream."

We propose that this waste stream may contain *structured cognitive artifacts*—stable, recurring patterns that represent coherent ideas, even if those ideas have no existing human name or category. We call these artifacts **Arcanum**, and the systematic search for them **conceptual archaeology**.

This paper makes the following contributions:

1. We formalize the concept of structured novelty search in LLM activation space, defining a composite fitness metric that balances semantic distance against coherence.
2. We describe the full six-stage Xenolexicon pipeline for automated Arcanum discovery, from evolutionary provocation through naming and cataloging.
3. We present empirical results from inaugural runs on Qwen 2.5 0.5B demonstrating successful evolutionary optimization toward novel structures.
4. We propose a rapid genome screening strategy leveraging large, diverse prompt banks to accelerate the search process.

---

## 2. Related Work

### 2.1 Mechanistic Interpretability

The circuits-based approach to interpretability, pioneered by Olah et al. (2020) and extended by Anthropic's work on superposition (Elhage et al., 2022), seeks to reverse-engineer the computational graph of neural networks. Recent work on Sparse Autoencoders (Cunningham et al., 2023; Bricken et al., 2023) has dramatically scaled this approach. Our work is complementary: where SAEs decompose known behaviors into interpretable features, we search for structured patterns that may not correspond to any known behavior.

### 2.2 Representation Engineering

Representation engineering (Zou et al., 2023) and activation steering (Turner et al., 2023) demonstrate that model behavior can be controlled by adding vectors to the residual stream. Our provocation mechanism is related, but rather than steering toward a known behavioral target, we steer toward regions of maximal structured novelty.

### 2.3 Evolutionary and Quality-Diversity Methods

The CMA-ES algorithm (Hansen & Ostermeier, 2001) provides our core optimization engine. Our approach also draws from quality-diversity methods (Mouret & Clune, 2015) and novelty search (Lehman & Stanley, 2011), which demonstrated that optimizing for novelty rather than fitness can discover solutions unreachable by objective-driven search. The AURA and SETI frameworks for evolutionary prompt engineering provide our architectural starting point.

### 2.4 Emergent and Non-Human Cognition

Work on emergent communication in multi-agent systems (Lazaridou et al., 2016) and on "alien" representations in vision models (Olah et al., 2017) establishes precedent for studying non-human-interpretable structures in neural networks. Our contribution is to systematize this into a discovery pipeline rather than treating it as an incidental finding.

---

## 3. Method: The Xenolexicon Pipeline

The Xenolexicon system consists of six sequential stages, each implemented as a modular component. The architecture is designed to fork existing evolutionary codebases (specifically, SETI v2-class systems) with minimal modification.

### 3.1 Stage 1: Provocation

The evolutionary engine maintains a population of *N* = 20 genomes per generation, each representing a composite provocation strategy. A genome encodes: (a) a steering vector applied to a target layer of the model, (b) a selection from a bank of provocation prompts, and (c) generation parameters including temperature and sampling strategy. The CMA-ES optimizer evolves the population to maximize the composite fitness function *F*:

> *F(g) = d_semantic(g) × C(g)*

where *d_semantic* is the cosine distance in embedding space between the genome's steered output and a baseline (un-steered) output for the same prompt, and *C* is a coherence function defined as a Gaussian over log-perplexity:

> *C(g) = exp(−(log PPL(g) − μ_target)² / 2σ²)*

This targets a "sweet spot" of structured weirdness: outputs that are neither degenerate gibberish (very high perplexity) nor boringly predictable (very low perplexity).

A **scout system** allocates a fraction of each generation's evaluations to non-target layers, enabling the optimizer to discover productive zones across the model's full depth. In our inaugural runs, the primary target was Layer 18, with scouts sampling Layers 13, 15, and 20.

### 3.2 Stage 2: Capture

When a genome's fitness *F(g)* exceeds a predefined novelty threshold *τ* (set to 0.3 in our experiments), the system triggers a full specimen capture. The captured data includes the genome vector, the provocation prompt, the complete model output, the output embedding, the perplexity profile, and all metadata (model identifier, layer, timestamp, fitness score).

### 3.3 Stage 3: Characterization

Each captured specimen undergoes automated validation: (a) Reproducibility—the genome is re-evaluated multiple times to verify that it reliably produces outputs in the same embedding neighborhood. (b) Distinctness—the specimen's embedding is compared against all existing Xenolexicon entries to reject near-duplicates. Future versions will incorporate cross-substrate convergence checks across different model architectures.

### 3.4 Stage 4: Naming

A separate, un-steered LLM instance acts as a "lexicographer," receiving the novel output and generating a compositional name (modeled on German compound-word formation) and a best-effort natural language description. A deterministic fallback name (e.g., XENO-001-L18-a1b2c3) is assigned if the naming model fails to produce a satisfactory result.

### 3.5 Stage 5: Cataloging

The named specimen is entered into the Xenolexicon database with full provenance, behavioral signatures, reproducibility scores, and all associated metadata. The MVP implementation uses a lightweight persistent store (SQLite or structured JSON).

### 3.6 Stage 6: Reinjection (Future Work)

The architecture is designed to support reinjection experiments in which discovered Arcanum names and descriptions are incorporated into new prompts to test whether they enable the model to access previously inaccessible reasoning pathways.

---

## 4. Experiments and Results

### 4.1 Experimental Setup

We conducted inaugural runs of the Xenolexicon pipeline on **Qwen 2.5 0.5B**, a compact language model suitable for rapid iteration on consumer hardware. Two machines were used in parallel:

| Configuration | Machine A | Machine B |
|:---|:---|:---|
| **GPU** | NVIDIA (16 GB VRAM) | NVIDIA GeForce GTX 1070 (8.2 GB) |
| **Model** | Qwen 2.5 0.5B | Qwen 2.5 0.5B |
| **Primary Target Layer** | Layer 18 | Layer 18 |
| **Population Size** | 20 genomes/generation | 20 genomes/generation |
| **Peak VRAM Usage** | 1.7 GB | TBD |

The provocation prompt bank for the inaugural run consisted of four domain-specific prompts targeting speculative mathematics and physics, designed to push the model into conceptually rich but under-explored territory. The capture threshold was set at *τ* = 0.3.

### 4.2 Evolutionary Dynamics

The CMA-ES optimizer demonstrated consistent improvement across the first four generations. Table 2 summarizes the progression of the best novelty score per generation on Machine A.

| Gen | Best Novelty | Productive Genomes | Wall Time (min) |
|:---:|:---:|:---:|:---:|
| 0 | 0.0869 | 2 / 20 | ~7.7 |
| 1 | 0.0996 | 2 / 20 | ~7 |
| 2 | 0.1182 | 2 / 20 | ~7 |
| 3 | 0.1212 | 2 / 20 | ~7 |

*Table 2. Novelty score progression across generations (Machine A, Qwen 2.5 0.5B).*

Several features of the evolutionary dynamics merit discussion:

**Monotonic improvement.** The best novelty score increased in every generation, from 0.0869 (Gen 0) to 0.1212 (Gen 3), representing a 39.5% improvement over four generations and a 104% improvement over the random baseline of 0.0593. This "staircase" pattern indicates that CMA-ES has successfully identified a productive gradient in the structured-novelty landscape.

**Stable selection pressure.** Each generation consistently produced 2 out of 20 genomes classified as "Productive" (10% hit rate). This ratio suggests a healthy balance between exploitation and exploration—sufficient selection signal to drive improvement without premature convergence.

**Layer diversification.** While the primary target was Layer 18, the scout system identified a secondary productive zone at Layer 13 in Generation 2. The optimizer subsequently began tracking both layers, suggesting that structured novelty may emerge at multiple stages of the model's processing hierarchy.

**Resource efficiency.** Peak VRAM usage on Machine A was 1.7 GB with a steady state of 1.4 GB, demonstrating that meaningful novelty search can be conducted on the 0.5B model with minimal hardware requirements.

---

## 5. Toward Rapid Genome Screening

A key observation from our inaugural runs is that the evolutionary process, while effective, is time-intensive: each generation requires approximately 7 minutes of wall-clock time on consumer hardware. At the current trajectory, reaching the capture threshold of 0.3 may require 15–25 additional generations, corresponding to 2–3 hours of continuous computation per mission.

We propose a **rapid genome screening** strategy to dramatically improve the efficiency of the search. The core insight is that the *provocation prompt* itself—not just the steering vector—is a critical determinant of whether the model enters a productive region of its activation space. Different prompts elicit different baseline activation geometries, and some of these geometries may be far more amenable to structured novelty than others.

### 5.1 Prompt Bank Construction

We have assembled a bank of 150 provocation prompts generated by six different LLMs (Claude, GPT-4, Gemini Flash, Gemini Pro, Granite 4, HuggingFace models, and Amazon Nova). Each prompt targets the intersection of speculative mathematics, physics, high-dimensional geometry, and complexity science. Crucially, these prompts were generated by different model architectures, ensuring diversity in the semantic geometry of the provocations themselves.

### 5.2 Early Termination Protocol

We propose a screen-and-advance protocol:

For each candidate prompt, run a *short evolutionary burst* (e.g., 2–3 generations with a reduced population of 10 genomes). If the best novelty score after this burst does not exceed a *screening threshold* (e.g., 0.10, approximately the Gen 1 performance in our inaugural run), terminate the run and advance to the next prompt. If the threshold is met, invest full computational resources in a deep evolutionary run with the standard population size.

### 5.3 Expected Benefits

This strategy converts the search problem from a single deep optimization to a two-phase process: a rapid, broad scan across prompt space followed by deep exploitation of the most promising prompts. Given our bank of 150 prompts, a 2-generation screening burst at reduced population size should require approximately 3–4 minutes per prompt. The full bank could be screened in under 10 hours across two machines, identifying the most fertile provocation prompts for subsequent deep runs.

### 5.4 Semantic Diversity as a Prior

An additional advantage of the multi-source prompt bank is that prompts generated by different model architectures occupy different regions of semantic space. A prompt from Claude (e.g., "If a tensor could forget one of its indices mid-contraction, what kind of residual geometric object would it leave behind?") elicits a qualitatively different baseline activation geometry than one from Gemini Pro (e.g., "How might one mathematically define a shadow manifold that only interacts with standard spacetime through sporadic leakage of higher-order tensor anomalies?"). This diversity serves as a prior over the search space, reducing the risk of all runs converging to the same local optimum.

---

## 6. Discussion

### 6.1 What Are We Finding?

It is important to be precise about what the current results demonstrate and what they do not. We have shown that CMA-ES can optimize a structured-novelty fitness function on a small language model, producing monotonically increasing scores. We have not yet captured a specimen that exceeds the 0.3 threshold. The system is, in evolutionary terms, still in its exploratory phase—the "scouts are getting warmer," but no museum-quality specimen has been collected.

The consistent 10% productive rate and the emergence of a secondary productive layer (Layer 13) suggest that the novelty landscape is not degenerate—there exist real, discoverable ridges of structured novelty in this model's activation space.

### 6.2 Model Scale Considerations

Qwen 2.5 0.5B was chosen for rapid iteration, but a 0.5B-parameter model has limited representational capacity. The waste stream of a model this size may simply contain fewer structured artifacts than that of a 7B or 70B model. Future work should systematically compare Arcanum yield across model scales. Our consumer-hardware approach (8–16 GB VRAM) constrains us to models in the 0.5B–3B range, but this is itself a feature: if structured novelty can be discovered even in small models, it suggests that these phenomena are fundamental rather than emergent only at scale.

### 6.3 The Genome Diversity Hypothesis

Our proposed rapid screening strategy rests on what we term the Genome Diversity Hypothesis: that the semantic content of the provocation prompt is at least as important as the steering vector in determining whether the model enters a productive activation regime. If this hypothesis is correct, then the 150-prompt bank represents a 37.5× expansion of the search space relative to our inaugural 4-prompt mission, with correspondingly greater probability of encountering a prompt-vector combination that triggers specimen-grade novelty.

### 6.4 Ethical Considerations

Our work deliberately seeks model outputs that are "weird"—distant from the model's aligned, human-readable behavior. We note that "structured weirdness" is not the same as "harmful weirdness." The coherence term in our fitness function penalizes degenerate outputs, and the provocation prompts are grounded in mathematics and physics rather than in domains where misalignment could produce harmful content. Nevertheless, any technique that deliberately pushes a model away from its alignment training warrants careful monitoring, and we encourage the community to develop safety frameworks specific to novelty search.

---

## 7. Conclusion

We have presented Xenolexicon, a six-stage pipeline for the automated discovery of structured novel concepts in the activation space of language models. Our inaugural runs on Qwen 2.5 0.5B demonstrate that evolutionary optimization of a structured-novelty fitness function produces consistent, measurable improvement across generations. We have proposed a rapid genome screening strategy that leverages a diverse bank of 150 provocation prompts to accelerate the search for specimen-grade Arcanum.

The broader vision of this work is to treat the internal life of language models not merely as a mechanism to be explained, but as a territory to be explored. The waste stream of inference may contain cognitive structures that are genuinely novel—ideas that no human has thought and no model has been asked to articulate. The Xenolexicon is our first map of this territory.

---

## References

Bricken, T., et al. (2023). *Towards Monosemanticity: Decomposing Language Models With Dictionary Learning.* Anthropic Research.

Cunningham, H., et al. (2023). *Sparse Autoencoders Find Highly Interpretable Features in Language Models.* ICLR 2024.

Elhage, N., et al. (2022). *Toy Models of Superposition.* Anthropic Research.

Hansen, N. & Ostermeier, A. (2001). *Completely Derandomized Self-Adaptation in Evolution Strategies.* Evolutionary Computation, 9(2), 159–195.

Lazaridou, A., et al. (2016). *Multi-Agent Cooperation and the Emergence of (Natural) Language.* ICLR 2017.

Lehman, J. & Stanley, K. O. (2011). *Abandoning Objectives: Evolution Through the Search for Novelty Alone.* Evolutionary Computation, 19(2), 189–223.

Mouret, J.-B. & Clune, J. (2015). *Illuminating Search Spaces by Mapping Elites.* arXiv:1504.04909.

Olah, C., et al. (2017). *Feature Visualization.* Distill.

Olah, C., et al. (2020). *Zoom In: An Introduction to Circuits.* Distill.

Turner, A., et al. (2023). *Activation Addition: Steering Language Models Without Optimization.* arXiv:2308.10248.

Zou, A., et al. (2023). *Representation Engineering: A Top-Down Approach to AI Transparency.* arXiv:2310.01405.
