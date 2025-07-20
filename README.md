# AHS-Compressor v2.0
[![Support this project](https://img.shields.io/badge/Support_this_project-❤️-ff69b4?style=for-the-badge)](#️-support-this-project)

A tool to compress Python code into an **Abstract Hierarchical Structure (AHS)**, designed to optimize code analysis and interaction for Large Language Models (LLMs).

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 What problem does it solve?

LLMs have a limited context window. Analyzing or modifying large code repositories is inefficient and often impossible, as the full source code doesn't fit into the model's prompt.

**AHS-Compressor** addresses this problem through "context compression." It doesn't reduce the file size but transforms the code into a high-level structure (the AHS) and a corresponding code map. This allows an LLM to:

1. **See the project's "architecture"** (the AHS structure) without needing to see every line of code
2. **Navigate the code intelligently**, requesting only the specific snippets it needs from the code map
3. **Modify code safely**, as reconstructing the code from the AHS and map preserves 100% of the original formatting, including comments (thanks to `libCST`)

## ✨ Key Features

- **🔄 Format Preservation:** Thanks to `libCST`, all comments, whitespace, and code structure are kept intact
- **📋 JSON Structure:** The AHS format is now a structured JSON, making it easy to parse and extend
- **🏗️ Project-Level Support:** The CLI can process entire directories, generating a single AHS for the whole project
- **⚡ API and CLI:** Offers both a command-line interface (`ahs-cli`) for local use and a web API (FastAPI) for integrations
- **📦 Ready to Install:** Available as a Python package via `pip`

## 🧠 Understanding AHS-Compressor: Real Utility & Workflow

AHS-Compressor's true utility lies in its ability to **overcome the context window limitations of LLMs**, especially local models.

### 📚 The Book Analogy

Imagine an LLM as a very intelligent student who can only read one page of a book at a time. If you give it an entire book (a large software project), it gets overwhelmed and cannot grasp the overall plot or where to find specific information.

**AHS-Compressor transforms the "book" into:**

1. **📑 A "Table of Contents" (the AHS):** A compact representation of the project's structure - what files exist, what classes and functions they contain, how they relate. This "index" is so small that the LLM can read it entirely.

2. **📖 A "Dictionary" (the Code Map):** Contains the exact text of each code snippet referenced in the index.

### 🎯 Key Benefits

- **🗜️ Semantic Context Compression:** Reduces "irrelevant information" that the LLM needs to process to understand the structure
- **🧭 Intelligent Navigation:** Allows the LLM to "jump" directly to relevant code sections without loading the entire file
- **✅ Perfect Fidelity:** Code reconstruction is 100% identical to the original, including comments and formatting
- **🏠 Empowering Local LLMs:** Local models with smaller context windows become far more useful for software engineering tasks

### 🔄 How to Use: The Complete Workflow

Using AHS-Compressor involves an iterative workflow between you and the LLM.

#### Step 1: Encode the Project (Human Action)
Use the CLI to transform your project into the AHS + Map format:
```bash
ahs-cli encode ./my_project -o my_project_context.json
```
This generates a JSON file with two main keys: `"ahs"` (the structure) and `"map"` (the content).

#### Step 2: Interact with the LLM (Human + LLM)
1. **Provide the AHS structure** to the LLM
2. **Give the LLM a task** (e.g., "Refactor the `calculate_sum` function")
3. **LLM identifies relevant `ref`** (e.g., `@5`)
4. **You provide the content** from the code map for that `ref`
5. **LLM processes and returns modified version**
6. **You update the code map** with the changes

#### Step 3: Decode the Project (Human Action)
Reconstruct the full project with your changes:
```bash
ahs-cli decode my_project_context.json -o ./restored_project
```

## 💬 LLM Interaction Setup

### Recommended System Prompt Template

```
You are an expert assistant in Python code analysis and refactoring. I will give you a project structure in a special format called AHS (Abstract Hierarchical Structure).

Your task is to help me understand and modify the code based on this structure. I will give you the complete structure first. Then, you can request the code for any part using its `ref` (for example, `@5`). Do not invent code, only request it through its `ref`.

---
PROJECT STRUCTURE (AHS):
[INSERT_YOUR_AHS_HERE]
---

Now, wait for my first instruction.
```

### 📋 Real Example in Action

After encoding a Windows diagnostic script:

```json
[
    { "type": "Import", "ref": "@0" },
    { "type": "Import", "ref": "@1" },
    { "type": "FunctionDef", "ref": "@5", "name": "ejecutar_powershell" },
    { "type": "FunctionDef", "ref": "@6", "name": "guardar_log" },
    { "type": "FunctionDef", "ref": "@7", "name": "escanear_procesos" },
    { "type": "FunctionDef", "ref": "@13", "name": "liberar_memoria" }
]
```

**Sample Interaction Flow:**

**You:** "I want to optimize the memory cleanup function. Can you analyze the liberar_memoria function?"

**LLM:** "I can see the liberar_memoria function in the structure (ref: @13). To analyze and optimize it, I need to see the current implementation. Please provide the content of @13."

**You:** [Copy the content from your JSON map for "@13"]

**LLM:** [Analyzes the function and suggests optimizations]

This workflow allows the LLM to:
- 🎯 Focus immediately on relevant code sections
- 🧠 Understand context without being overwhelmed
- 🔄 Work iteratively on specific improvements
- 📊 See the big picture of your project's architecture

## 🚀 Installation

### Recommended Method: Using pipx

#### 🔧 Why Use `pipx`? (The Toolbox Analogy)

Think of your computer as a large workshop where each project needs its own special tools:

- **❌ Global Installation:** Like throwing all tools into one giant box - chaos ensues!
- **⚠️ Virtual Environments:** Like separate toolboxes - organized but inconvenient
- **✅ pipx (Best of Both Worlds):** Creates isolated toolboxes but puts main tools on a public wall for easy access

#### Step-by-Step Installation Guide

**1. Install `pipx`** (once in your lifetime):
```bash
pip install pipx
```

**2. Add `pipx` to your system:**
```bash
pipx ensurepath
```
*(Restart your terminal after this step)*

**3. Install `AHS-Compressor`:**
```bash
pipx install git+https://github.com/rcdrodrigo/ahs-compressor.git
```

**4. Verify Installation:**
```bash
ahs-cli --help
```

### Alternative Installation Methods

#### For Developers (Local Development)
```bash
git clone https://github.com/rcdrodrigo/ahs-compressor.git
cd ahs-compressor
pip install -e .
```

#### Using pip (Not Recommended for End Users)
```bash
pip install git+https://github.com/rcdrodrigo/ahs-compressor.git
```

### Maintenance Commands

**Update to latest version:**
```bash
pipx upgrade ahs-compressor
```

**Uninstall:**
```bash
pipx uninstall ahs-compressor
```

## 📘 Usage

### Command-Line Interface (CLI)

**Encode an entire project:**
```bash
ahs-cli encode ./my_project -o compressed_project.json
```

**Decode a project:**
```bash
ahs-cli decode compressed_project.json -o ./my_project_restored
```

### 🌐 Web API

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

Server available at `http://localhost:8000`

**Main Endpoints:**
- `POST /compress-text`: Compresses a code snippet
- `POST /decompress-text`: Decompresses an AHS and map
- `GET /health`: Health check endpoint

## 🛠️ Development

### Getting Started
```bash
git clone https://github.com/rcdrodrigo/ahs-compressor.git
cd ahs-compressor
pip install -e .
```

### 🗺️ Roadmap

- [ ] 📦 Publish package to PyPI
- [ ] 🌐 Implement project-level compression in API with background tasks
- [ ] 🔧 Add support for more languages (JavaScript, Java)
- [ ] 🐍 Create Python client for easier API interaction
- [ ] 🔌 VS Code plugin development

## 💡 Best Practices

### Maximizing Efficiency

1. **🎯 Focused Iterations:** Work on individual functions or classes, not entire projects at once
2. **📝 Clear Prompting:** Be explicit about the AHS format and interaction patterns
3. **🔄 Test-Driven Workflow:** Encode → LLM modifies → Update map → Decode → Test → Repeat
4. **📚 Strategic Analysis:** Use AHS for architecture analysis and dependency identification
5. **🔧 Version Control:** Always work on Git branches and commit after each cycle

## ❤️ Support This Project

AHS-Compressor is a free, open-source project that requires time and effort to maintain and improve. If you find this tool useful, consider supporting its development:

⭐ **Star the repository:** The quickest way to show support and help the project gain visibility

💝 **Contribute:** Found a bug? Have an improvement idea? Pull requests are welcome!

📢 **Spread the word:** Share the project with other developers who might find it useful

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
