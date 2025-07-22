# AHS-Compressor v2.0 [![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![GitHub stars](https://img.shields.io/github/stars/rcdrodrigo/ahs-compressor?style=social)](https://github.com/rcdrodrigo/ahs-compressor/stargazers)
> A tool to compress Python code into an **Abstract Hierarchical Structure (AHS)**, designed to optimize code analysis and interaction with Large Language Models (LLMs).

---

## 🎯 What problem does it solve?
LLMs have a limited context window. Analyzing or modifying large code repositories is inefficient and often impossible, as the full source code doesn't fit into the model's prompt.

**AHS-Compressor** addresses this problem through "context compression." It doesn't reduce the file size but transforms the code into a high-level structure (the AHS) and a corresponding code map. This allows an LLM to:
1.  **See the project's "architecture"** (the AHS structure) without needing to see every line of code.
2.  **Navigate the code intelligently**, requesting only the specific snippets it needs from the code map.
3.  **Modify code safely**, as rebuilding the code from the AHS and map preserves 100% of the original formatting, including comments (thanks to `libCST`).

## ✨ Key Features
- **🔄 Format Preservation:** Thanks to `libCST`, all comments, whitespace, and code structure are kept intact.
- **📋 JSON Structure:** The AHS format is now a structured JSON, making it easier to parse and extend.
- **🏗️ Project-Level Support:** The CLI can process entire directories, generating a single AHS for the whole project.
- **⚡ API and CLI:** Offers both a command-line interface (`ahs-cli`) for local use and a web API (FastAPI) for integrations.
- **📦 Ready to Install:** Available as a Python package via `pip`.

## 🧠 Understanding AHS-Compressor: Real-World Utility and Workflow
The true utility of AHS-Compressor lies in its ability to **overcome the context window limitations of LLMs**, especially local models.

### 📚 The Book Analogy
Imagine an LLM as a very smart student who can only read one page of a book at a time. If you give them an entire book (a large software project), they get overwhelmed and can't grasp the overall plot or where to find specific information.

**AHS-Compressor transforms the "book" into:**
1.  **📑 An "Index" (the AHS):** A compact representation of the project's structure—what files exist, what classes and functions they contain, how they relate. This "index" is small enough for the LLM to read completely.
2.  **📖 A "Dictionary" (the Code Map):** Contains the exact text of each code snippet referenced in the index.

### 🎯 Key Benefits
- **🗜️ Semantic Context Compression:** Reduces the "irrelevant information" the LLM needs to process to understand the structure.
- **🧭 Smart Navigation:** Allows the LLM to "jump" directly to relevant code sections without loading the entire file.
- **✅ Perfect Fidelity:** Code reconstruction is 100% identical to the original, including comments and formatting.
- **🏠 Empowering Local LLMs:** Local models with smaller context windows become much more useful for software engineering tasks.

### 🔄 How to Use: The Complete Workflow
Using AHS-Compressor involves an iterative workflow between you and the LLM.

#### Step 1: Encode the Project (Human Action)
Use the CLI to transform your project into the AHS + Map format:
```bash
ahs-cli encode ./my_project -o project_context.json
```
This generates a JSON file with two main keys: `"ahs"` (the structure) and `"map"` (the content).

#### Step 2: Interact with the LLM (Human + LLM)
1.  **Provide the AHS structure** to the LLM.
2.  **Give the LLM a task** (e.g., "Refactor the `calculate_sum` function").
3.  **The LLM identifies the relevant `ref`** (e.g., `@5`).
4.  **You provide the content** from the code map for that `ref`.
5.  **The LLM processes and returns the modified version**.
6.  **You update the code map** with the changes.

#### Step 3: Decode the Project (Human Action)
Rebuild the complete project with your changes:
```bash
ahs-cli decode project_context.json -o ./restored_project
```

## 💬 LLM Interaction Setup
### Recommended System Prompt Template
```
You are an expert assistant for Python code analysis and refactoring. I will provide you with a project structure in a special format called AHS (Abstract Hierarchical Structure). Your task is to help me understand and modify the code based on this structure.
First, I will give you the complete structure. Then, you can request the code for any part using its `ref` (e.g., `@5`). Do not invent code; only request it using its `ref`.
---
PROJECT STRUCTURE (AHS):
[
  { "type": "Import", "ref": "@0" },
  { "type": "Import", "ref": "@1" },
  { "type": "FunctionDef", "ref": "@5", "name": "run_powershell" },
  { "type": "FunctionDef", "ref": "@6", "name": "save_log" }
]
---
Once this is done, wait for my first instruction.
```

**Example Interaction Flow:**
**You:** "I want to optimize the memory cleanup function. Can you analyze the `free_memory` function?"
**LLM:** "I can see the `free_memory` function in the structure (ref: @13). To analyze and optimize it, I need to see the current implementation. Please provide the content of @13."
**You:** [Copy the content from your JSON map for "@13"]
**LLM:** [Analyzes the function and suggests optimizations]

This workflow allows the LLM to:
- 🎯 Immediately focus on relevant code sections.
- 🧠 Understand the context without being overwhelmed.
- 🔄 Work iteratively on specific improvements.
- 📊 See the big picture of your project's architecture.

## 🤖 Complete Example with Claude
Want to see AHS-Compressor in action refactoring a real 2000+ line project?
👉 [Complete Example: AHS-Compressor + Claude](https://github.com/rcdrodrigo/ahs-compressor/blob/main/Complete%20Example%3A%20AHS-Compressor%20%2B%20Claude.md)

This detailed example demonstrates:
- **🎯 Full step-by-step workflow** - From encoding to reconstruction.
- **💬 Real conversation with Claude** - Specific interactions and optimized prompts.
- **⚡ Refactoring a security system** - A complex project with multiple modules.
- **📊 Performance metrics** - 5x faster than traditional methods.
- **🛠️ Best practices** - Proven strategies for maximum efficiency.

**Example Results:**
- ✅ 2,180 lines analyzed without losing context.
- ✅ 15+ functions optimized with best practices.
- ✅ 8 bugs found and proactively fixed.
- ✅ Only ~1,200 tokens per iteration (vs. 8,000+ traditionally).

### 🚀 Highlighted Use Cases
- **Legacy Code Modernization** - Update old systems.
- **Architecture Reviews** - In-depth design analysis.
- **Performance Optimization** - Identify and resolve bottlenecks.
- **Code Quality Improvement** - Apply patterns and best practices.

## 🚀 Installation
### Recommended Method: Using pipx
#### 🔧 Why use `pipx`? (The Toolbox Analogy)
Think of your computer as a large workshop where each project needs its own special tools:
- **❌ Global Install:** Like throwing all tools into one giant box - chaos ensues!
- **⚠️ Virtual Environments:** Like separate toolboxes - organized but inconvenient.
- **✅ pipx (The Best of Both Worlds):** Creates isolated toolboxes but puts the main tools on a public wall for easy access.

#### Step-by-Step Installation Guide
**1. Install `pipx`** (once in your life):
```bash
pip install pipx
```
**2. Add `pipx` to your system path:**
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

#### Using pip (Not Recommended for End-Users)
```bash
pip install git+https://github.com/rcdrodrigo/ahs-compressor.git
```

### Maintenance Commands
**Upgrade to the latest version:**
```bash
pipx upgrade ahs-compressor
```
**Uninstall:**
```bash
pipx uninstall ahs-compressor
```

## 📘 Usage
### Command-Line Interface (CLI)
**Encode a full project:**
```bash
ahs-cli encode ./my_project -o compressed_project.json
```
**Decode a project:**
```bash
ahs-cli decode compressed_project.json -o ./my_restored_project
```

### 🌐 Web API
Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
The server is available at `http://localhost:8000`.

**Main Endpoints:**
- `POST /compress-text`: Compresses a code snippet.
- `POST /decompress-text`: Decompresses an AHS and map.
- `GET /health`: Health check endpoint.

## 🛠️ Development
### Getting Started
```bash
git clone https://github.com/rcdrodrigo/ahs-compressor.git
cd ahs-compressor
pip install -e .
```

### 🗺️ Roadmap
- [ ] 📦 Publish package to PyPI.
- [ ] 🌐 Implement project-level compression in the API with background tasks.
- [ ] 🔧 Add support for more languages (JavaScript, Java).
- [ ] 🐍 Create a Python client for easier interaction with the API.
- [ ] 🔌 Develop a VS Code plugin.

## 💡 Best Practices
### Maximizing Efficiency
1.  **🎯 Focused Iterations:** Work on individual functions or classes, not entire projects at once.
2.  **📝 Clear Prompting:** Be explicit about the AHS format and interaction patterns.
3.  **🔄 Test-Driven Workflow:** Encode → LLM modifies → Update map → Decode → Test → Repeat.
4.  **📚 Strategic Analysis:** Use AHS for architecture analysis and dependency identification.
5.  **🔧 Version Control:** Always work in Git branches and commit after each cycle.

❤️ Support This Project
AHS-Compressor is a free and open-source project that requires time and effort to maintain and improve. If you find this tool useful, please consider supporting its development:

🌟 Ways to Support
[![GitHub Sponsors](https://img.shields.io/badge/GitHub-Sponsors-ea4aaa?style=for-the-badge&logo=github)](https://github.com/sponsors/rcdrodrigo) [![Ko-fi](https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/rcdrodrigo) [![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/rcdrodrigo) [![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/rcdrodrigo)

### 🚀 Other ways to contribute
⭐ **Star the repository:** The quickest way to show support and help the project gain visibility.
💝 **Contribute:** Found a bug? Have an idea for an improvement? Pull requests are welcome!
📢 **Spread the word:** Share the project with other developers who might find it useful.
🐛 **Report bugs:** Help us improve by reporting issues in the [Issues](https://github.com/rcdrodrigo/ahs-compressor/issues) tab.
📖 **Improve the documentation:** Documentation can always be better.

---

## 🤝 Contributing
Contributions are welcome. Please:
1.  Fork the project.
2.  Create a feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Contact
- **GitHub:** [@rcdrodrigo](https://github.com/rcdrodrigo)
- **Issues:** [Report an issue](https://github.com/rcdrodrigo/ahs-compressor/issues)

---
**Found AHS-Compressor useful?** ⭐ Give the repo a star