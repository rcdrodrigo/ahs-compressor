# AHS-Compressor v2.0
[![Apoyar el proyecto](https://img.shields.io/badge/Apoyar_el_proyecto-❤️-ff69b4?style=for-the-badge)](#️-support-this-project)

A tool to compress Python code into an **Abstract Hierarchical Structure (AHS)**, designed to optimize code analysis and interaction for Large Language Models (LLMs).

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## What problem does it solve?

LLMs have a limited context window. Analyzing or modifying large code repositories is inefficient and often impossible, as the full source code doesn't fit into the model's prompt.

**AHS-Compressor** addresses this problem through "context compression." It doesn't reduce the file size but transforms the code into a high-level structure (the AHS) and a corresponding code map. This allows an LLM to:

1.  **See the project's "architecture"** (the AHS structure) without needing to see every line of code.
2.  **Navigate the code intelligently**, requesting only the specific snippets it needs from the code map.
3.  **Modify code safely**, as reconstructing the code from the AHS and map preserves 100% of the original formatting, including comments (thanks to `libCST`).

## Key Features

- **Format Preservation:** Thanks to `libCST`, all comments, whitespace, and code structure are kept intact.
- **JSON Structure:** The AHS format is now a structured JSON, making it easy to parse and extend.
- **Project-Level Support:** The CLI can process entire directories, generating a single AHS for the whole project.
- **API and CLI:** Offers both a command-line interface (`ahs-cli`) for local use and a web API (FastAPI) for integrations.
- **Packaged:** Ready to be installed as a Python package via `pip`.

## Understanding AHS-Compressor: Real Utility & Workflow

AHS-Compressor's true utility lies in its ability to **overcome the context window limitations of LLMs**, especially local models.

Imagine an LLM as a very intelligent student who can only read one page of a book at a time. If you give it an entire book (a large software project), it gets overwhelmed and cannot grasp the overall plot or where to find specific information.

**AHS-Compressor transforms the "book" into:**

1.  **A "Table of Contents" or "Roadmap" (the AHS):** A compact representation of the project's structure (what files exist, what classes and functions they contain, how they relate). This "index" is so small that the LLM can read it entirely.
2.  **A "Glossary" or "Dictionary" (the Code Map):** Contains the exact text of each code snippet referenced in the index.

### Key Benefits:

*   **Semantic Context Compression:** It doesn't reduce file size, but rather the amount of "irrelevant information" that the LLM needs to process to understand the structure.
*   **Intelligent Navigation:** Allows the LLM (or you, guiding the LLM) to "jump" directly to relevant code sections without loading the entire file.
*   **Fidelity Preservation:** Thanks to `libCST`, code reconstruction is 100% identical to the original, including comments, formatting, and whitespace. This is vital for a developer's work.
*   **Empowering Local LLMs:** Local models, with their smaller context windows, are the biggest beneficiaries. AHS-Compressor makes them far more useful for software engineering tasks.

### How to Use (The Workflow):

Using AHS-Compressor involves an iterative workflow between you and the LLM.

1.  **Step 1: Encode the Project (Human Action)**
    *   Use the CLI to transform your project into the AHS + Map format.
    *   `ahs-cli encode ./my_project -o my_project_context.json`
    *   This generates a JSON file with two main keys: `"ahs"` (the structure) and `"map"` (the content of code snippets).

2.  **Step 2: Interact with the LLM (Human + LLM Interaction)**
    *   **You provide the LLM with the AHS (the `"ahs"` part of the JSON).** Tell it: "Here's my project's structure. Each node has a `ref` (e.g., `@0`) you can use to ask me for the exact code."
    *   **You give the LLM a task.** For example: "Refactor the `calculate_sum` function in `my_module.py`. According to the AHS, that function is `FunctionDef` with `ref: @5`."
    *   **The LLM (or you, guided by the LLM) identifies the relevant `ref`.**
    *   **You provide the LLM with the content of that `ref` from the code map (the `"map"` part of the JSON).** Tell it: "The content of `@5` is: `def calculate_sum(a: int, b: int) -> int: ...`"
    *   **The LLM processes the code snippet and returns the modified version.** Ask it to return *only* the modified code snippet, without extra explanations.
    *   **You update the code map.** Take the LLM's modified snippet and replace it in the corresponding key of the map (`"map": {"@5": "new code"}`).

3.  **Step 3: Decode the Project (Human Action)**
    *   Once you've made changes (or at each significant iteration), use the CLI to reconstruct the full project with the LLM's changes.
    *   `ahs-cli decode my_project_context.json -o ./restored_project`
    *   This generates a new directory with your updated code.

## Practical Example: LLM Interaction Setup

Here's a proven prompt template you can use with any LLM (local or remote) to get the best results with AHS-Compressor:

### Recommended System Prompt Template

```
You are an expert assistant for Python code analysis and refactoring. I will give you the structure of a project in a special format called AHS (Abstract Hierarchical Structure).

Your task is to help me understand and modify code based on this structure. I will give you the complete structure first. Then, you can request the code for any part using its ref (for example, @5). You must NOT invent code, only request it through its ref.

PROJECT STRUCTURE (AHS):
[INSERT_YOUR_AHS_HERE]

Wait for my first instruction.
```

### Real Example in Action

Let's say you have a Windows diagnostic script. After encoding with `ahs-cli encode diagnostic_script.py -o diagnostic.json`, your AHS might look like this:

```json
[
    { "type": "Import", "ref": "@0" },
    { "type": "Import", "ref": "@1" },
    { "type": "Import", "ref": "@2" },
    { "type": "Import", "ref": "@3" },
    { "type": "Import", "ref": "@4" },
    { "type": "FunctionDef", "ref": "@5", "name": "ejecutar_powershell" },
    { "type": "FunctionDef", "ref": "@6", "name": "guardar_log" },
    { "type": "FunctionDef", "ref": "@7", "name": "escanear_procesos" },
    { "type": "FunctionDef", "ref": "@8", "name": "conexiones_red" },
    { "type": "FunctionDef", "ref": "@9", "name": "archivos_malformados" },
    { "type": "FunctionDef", "ref": "@10", "name": "escaneo_sfc" },
    { "type": "FunctionDef", "ref": "@11", "name": "escaneo_dism" },
    { "type": "FunctionDef", "ref": "@12", "name": "limpiar_temporales" },
    { "type": "FunctionDef", "ref": "@13", "name": "liberar_memoria" },
    { "type": "FunctionDef", "ref": "@14", "name": "listar_inicio" },
    { "type": "FunctionDef", "ref": "@15", "name": "comprimir_y_abrir_logs" }
]
```

### Sample Interaction Flow

**You:** "I want to optimize the memory cleanup function. Can you analyze the liberar_memoria function?"

**LLM:** "I can see the liberar_memoria function in the structure (ref: @13). To analyze and optimize it, I need to see the current implementation. Please provide the content of @13."

**You:** [Copy the content from your JSON map for "@13"]

**LLM:** [Analyzes the function and suggests optimizations]

**You:** [Update the map with the LLM's improved version, then decode to get the updated project]

This workflow allows the LLM to:

🎯 Focus immediately on relevant code sections  
🧠 Understand context without being overwhelmed by irrelevant code  
🔄 Work iteratively on specific improvements  
📊 See the big picture of your project's architecture  

### Maximizing Efficiency:

1.  **Specific Prompt Engineering for AHS:**
    *   **Clarity:** Be extremely clear with the LLM about the AHS format and how it should interact with it.
    *   **Roles:** Define roles. "I will give you the structure. You tell me which `ref` you need. I will give you the content. You will return the modified content."
    *   **Structured Output:** Ask the LLM to return *only* the modified code, without preambles or explanations. This facilitates map updates.

2.  **Small, Focused Iterations:**
    *   Don't try to have the LLM refactor the entire project at once. Work on individual functions or classes.
    *   Encode -> LLM modifies a snippet -> Update map -> Decode -> Test. Repeat.

3.  **Integration with Your Workflow (Future):**
    *   **Scripts:** You can write Python scripts to automate reading the JSON, interacting with an LLM API (if using a remote or local one with an API), updating the JSON, and decoding.
    *   **IDE Plugins:** The long-term vision is a VS Code plugin that handles all this transparently for the user.

4.  **Strategic LLM Use:**
    *   **High-Level Analysis:** Use the AHS to ask the LLM to analyze architecture, identify dependencies, or suggest where to add new functionality.
    *   **Snippet Refactoring:** Once a snippet is identified, the LLM is excellent for refactoring, optimizing, or adding tests to that specific code.
    *   **New Code Generation:** You can ask it to generate a new function or class, and then manually insert it into the appropriate place in the code map.

5.  **Version Control (Git):**
    *   AHS-Compressor complements Git, it doesn't replace it. Always work on a Git branch. After each encoding/decoding cycle and verification, make a commit.

## Installation

### Recommended Method: Using pipx

To use `ahs-cli`, this project's command-line tool, you need to install it on your system. The best way to do this is using a tool called `pipx`.

#### Why Use `pipx`? (The Toolbox Analogy)

Think of your computer as a large workshop where each project you work on needs its own special tools.

* **Normal (Global) Installation:** This is like throwing all the tools from all your projects into one giant box in the middle of the workshop. At first it seems convenient, but it quickly becomes chaos. A screw from one project gets mixed up with another, and if two projects need different versions of the same wrench, you have a big problem!

* **Virtual Environments (`venv`):** This is like having a separate, dedicated toolbox for each project. It's very organized and safe, but every time you want to use a tool, you have to go find that specific box and open it (`activate` the environment).

* **Installation with `pipx` (Best of Both Worlds):** `pipx` acts like an intelligent tool manager. It creates a special, isolated toolbox just for `AHS-Compressor`, but then takes the main tool (`ahs-cli`) and hangs it on a **public tool wall** in your workshop.

**The result:** The `ahs-cli` command is always visible and available for you to use anywhere in the workshop, but all its specialized parts and gears remain stored and organized in their own box, without mixing with anything else.

#### Benefits of using `pipx`:
* **Convenience:** You type `ahs-cli` in any terminal and it simply works. You don't need to `activate` anything.
* **Safety:** Your main Python installation stays clean and stable. There's no risk of `AHS-Compressor` conflicting with other projects or tools.
* **Easy Maintenance:** Updating or uninstalling the tool is incredibly simple.

#### Step-by-Step Installation Guide

**1. Install `pipx`**
Open your terminal (PowerShell, CMD, etc.) and run this command. You only need to do this once in your lifetime:

```bash
pip install pipx
```

**2. Add `pipx` to your system**
This command ensures your system knows where to find the tools that `pipx` installs:

```bash
pipx ensurepath
```

*(You may need to restart your terminal after this step)*

**3. Install `AHS-Compressor`**
Finally, install the tool directly from GitHub with this simple command:

```bash
pipx install git+https://github.com/rcdrodrigo/ahs-compressor.git
```

**4. Verify Installation**
Test that everything is working correctly:

```bash
ahs-cli --help
```

You should see the help information for the AHS-Compressor tool.

### Alternative Installation Methods

#### For Developers (Local Development)
If you want to contribute to the project or work with the source code:

```bash
# Clone the repository
git clone https://github.com/rcdrodrigo/ahs-compressor.git
cd ahs-compressor

# Install in editable mode
pip install -e .
```

#### Using pip (Not Recommended for End Users)
If you prefer not to use `pipx`, you can install with regular pip, but be aware of potential conflicts:

```bash
pip install git+https://github.com/rcdrodrigo/ahs-compressor.git
```

### Quick Start

Once installed, you can immediately start using AHS-Compressor:

```bash
# Compress a Python project
ahs-cli encode ./my_project -o compressed_project.json

# Decompress back to source code
ahs-cli decode compressed_project.json -o ./restored_project
```

### Updating AHS-Compressor

To update to the latest version:

```bash
pipx upgrade ahs-compressor
```

### Uninstalling

To remove AHS-Compressor from your system:

```bash
pipx uninstall ahs-compressor
```

## Usage

### Command-Line Interface (CLI)

The CLI is the primary way to interact with the tool to compress and decompress projects.

**1. Encode an entire project:**

```bash
# Encodes the 'my_project' directory and saves the output to 'compressed_project.json'
ahs-cli encode ./my_project -o compressed_project.json
```

**2. Decode a project:**

```bash
# Reads 'compressed_project.json' and restores the code in the 'my_project_restored' directory
ahs-cli decode compressed_project.json -o ./my_project_restored
```

### Web API

The application also includes a FastAPI for integrations.

**To start the server:**

```bash
# Make sure you have uvicorn installed (it's in the dependencies)
uvicorn app.main:app --reload
```

The server will be available at `http://localhost:8000`.

**Main Endpoints:**

- `POST /compress-text`: Compresses a code snippet sent in the request body.
- `POST /decompress-text`: Decompresses an AHS and map sent in the request body.
- `GET /health`: A status endpoint to check if the API is running.

## Development

To contribute to the project, clone the repository, install the dependencies in editable mode as shown above, and start making changes.

### Next Steps

- [ ] Implement project-level compression in the API using background tasks.
- [ ] Publish the package to PyPI.
- [ ] Add support for more languages (e.g., JavaScript, Java) using dedicated parsers.
- [ ] Create a Python client to interact with the API more easily.

## ❤️ Apoya este proyecto

AHS-Compressor es un proyecto gratuito y de código abierto que requiere tiempo y esfuerzo para mantenerlo y mejorarlo. Si encuentras útil esta herramienta, considera apoyar su desarrollo.

⭐ **Estrella el repositorio:** Es la forma más rápida y sencilla de mostrar tu apoyo y ayudar a que el proyecto gane visibilidad en la comunidad.

💝 **Contribuye:** ¿Encontraste un error? ¿Tienes una idea para mejorar? ¡Las solicitudes de incorporación de cambios son bienvenidas!

📢 **Corre la voz:** Comparte el proyecto con otros desarrolladores que puedan encontrarlo útil.
