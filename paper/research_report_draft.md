# LLM-Assisted Generation and Experimental Validation of Synthetic BGP Misconfiguration Scenarios

**Authors:** Asad Ullah, Isha Tur Raazia  
**Project Term:** October 15, 2026 – December 26, 2026  

---

## 1. Executive Summary & Research Context

### 1.1 Research Question
Can a locally-run LLM (via Ollama) generate experimentally valid BGP misconfiguration scenarios that add useful behavioral diversity beyond template-based generation, for training anomaly detectors?

### 1.2 Core Experimental Premise
The LLM proposes a bounded configuration change; our FRR laboratory environment determines whether the change actually reproduces the intended BGP fault. Failed LLM generations are recorded as valid experimental failure data rather than discarded.

### 1.3 Scope & Constraints
- **Target Scope:** 3 Core BGP Fault Classes (Neighbor ASN mismatch, accidental prefix filtering, export-policy violation).
- **Local LLM Setup:** Offline CPU-based inference via Ollama.
- **Target Infrastructure:** Containerlab with FRRouting (FRR) routers running in WSL2.

---

## 2. Experimental Setup & Hardware Specifications

### 2.1 Host Hardware & System Configuration
- **OS:** Windows 11 25H2
- **CPU:** Intel Core i5-10210U (4 cores / 8 threads, AVX2 support)
- **RAM:** 16 GB System Memory
- **Storage:** 65+ GB Free SSD Space
- **Virtualization:** Enabled (WSL2 Architecture)

### 2.2 Resource Partitioning (`.wslconfig`)
To balance resource consumption between local LLM generation and network emulation, system RAM and CPU cores are capped for WSL2:
- **WSL2 Memory Cap:** 7 GB
- **WSL2 Processor Cap:** 6 Logical Cores
- **WSL2 Swap Allocation:** 8 GB

---

## 3. Methodology Overview

### 3.1 Network Topologies
- **Phase 1 Topology (3-Router Chain):**
  `AS100 (r1) <---> AS200 (r2) <---> AS300 (r3)`
- **Phase 2 Topology (5-Router Mesh):** Provider-Customer peering topology for route leak and export-policy testing.

### 3.2 Correctness Levels
1. **Syntactically Valid:** FRR accepts configuration lines without syntax errors.
2. **Operationally Executable:** The lab deploys and session execution/attempts occur.
3. **Semantically Valid:** Observed BGP behavior matches the intended operational fault label.