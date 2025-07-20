# AHS-Compressor v2.0
[![Sponsor](https://img.shields.io/badge/Sponsor-❤️-ff69b4?style=for-the-badge)](https://github.com/sponsors/rcdrodrigo)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A tool to compress Python code into an **Abstract Hierarchical Structure (AHS)**, designed to optimize code analysis and interaction for Large Language Models (LLMs).

*Read this in other languages: [Español](./README_es.md)*

![AHS-Compressor Demo](https://raw.githubusercontent.com/rcdrodrigo/ahs-compressor/main/docs/demo.gif)

---

## Quick Start

```bash
# 1. Install the tool
pipx install git+[https://github.com/rcdrodrigo/ahs-compressor.git](https://github.com/rcdrodrigo/ahs-compressor.git)

# 2. Compress your project
ahs-cli encode ./my_project -o compressed_project.json

# 3. Decompress it after modifications
ahs-cli decode compressed_project.json -o ./restored_project

How It Works & Why It's Useful
LLMs have a limited context window. Analyzing or modifying large code repositories is inefficient because the full source code doesn't fit into the model's prompt.

AHS-Compressor solves this with "context compression." It transforms your code into:

An "Architecture Map" (the AHS): A compact JSON structure showing all files, classes, and functions. This is small enough for an LLM to see the entire project's structure.

A "Code Snippet Dictionary" (the Code Map): Contains the exact code for each item in the map, accessible via a reference ID (e.g., @5).

This allows an LLM to see the project's "big picture" and then request only the specific code it needs, all while preserving 100% of the original formatting and comments thanks to libCST.

The Workflow
Using AHS-Compressor is an iterative process between you and an LLM.

Encode the Project (You)

Run ahs-cli encode ./my_project -o context.json to generate the AHS and the Code Map.

Interact with the LLM (You + LLM)

You: Give the LLM the AHS structure (the "ahs" part of the JSON).

You: Assign a task, like "Refactor the calculate_total function."

LLM: It identifies the function in the AHS and requests its code using its ref ID (e.g., "Please provide the code for @10").

You: Provide the code snippet from the Code Map (the "map" part of the JSON).

LLM: Returns the modified code snippet.

You: Update the Code Map in your JSON file with the new snippet.

Decode the Project (You)

Run ahs-cli decode context.json -o ./restored_project to rebuild your project with the applied changes.

LLM Interaction Template
Here is a recommended system prompt to use with any LLM.

You are an expert Python code analysis and refactoring assistant. I will provide you with a project's structure in a special format called AHS (Abstract Hierarchical Structure).

Your task is to help me understand and modify the code based on this structure. First, I will give you the complete AHS. Then, you can request the code for any part by asking for its `ref` (e.g., `@5`). You must not invent code; only request it using its `ref`.

---
PROJECT STRUCTURE (AHS):
[INSERT_YOUR_AHS_HERE]
---

Now, wait for my first instruction.

Por supuesto. Aquí tienes la versión final y completa, solo en inglés, lista para copiar y pegar en tu archivo README.md.

Markdown

# AHS-Compressor v2.0
[![Sponsor](https://img.shields.io/badge/Sponsor-❤️-ff69b4?style=for-the-badge)](https://github.com/sponsors/rcdrodrigo)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A tool to compress Python code into an **Abstract Hierarchical Structure (AHS)**, designed to optimize code analysis and interaction for Large Language Models (LLMs).

*Read this in other languages: [Español](./README_es.md)*

![AHS-Compressor Demo](https://raw.githubusercontent.com/rcdrodrigo/ahs-compressor/main/docs/demo.gif)

---

## Quick Start

```bash
# 1. Install the tool
pipx install git+[https://github.com/rcdrodrigo/ahs-compressor.git](https://github.com/rcdrodrigo/ahs-compressor.git)

# 2. Compress your project
ahs-cli encode ./my_project -o compressed_project.json

# 3. Decompress it after modifications
ahs-cli decode compressed_project.json -o ./restored_project
How It Works & Why It's Useful
LLMs have a limited context window. Analyzing or modifying large code repositories is inefficient because the full source code doesn't fit into the model's prompt.

AHS-Compressor solves this with "context compression." It transforms your code into:

An "Architecture Map" (the AHS): A compact JSON structure showing all files, classes, and functions. This is small enough for an LLM to see the entire project's structure.

A "Code Snippet Dictionary" (the Code Map): Contains the exact code for each item in the map, accessible via a reference ID (e.g., @5).

This allows an LLM to see the project's "big picture" and then request only the specific code it needs, all while preserving 100% of the original formatting and comments thanks to libCST.

The Workflow
Using AHS-Compressor is an iterative process between you and an LLM.

Encode the Project (You)

Run ahs-cli encode ./my_project -o context.json to generate the AHS and the Code Map.

Interact with the LLM (You + LLM)

You: Give the LLM the AHS structure (the "ahs" part of the JSON).

You: Assign a task, like "Refactor the calculate_total function."

LLM: It identifies the function in the AHS and requests its code using its ref ID (e.g., "Please provide the code for @10").

You: Provide the code snippet from the Code Map (the "map" part of the JSON).

LLM: Returns the modified code snippet.

You: Update the Code Map in your JSON file with the new snippet.

Decode the Project (You)

Run ahs-cli decode context.json -o ./restored_project to rebuild your project with the applied changes.

LLM Interaction Template
Here is a recommended system prompt to use with any LLM.

You are an expert Python code analysis and refactoring assistant. I will provide you with a project's structure in a special format called AHS (Abstract Hierarchical Structure).

Your task is to help me understand and modify the code based on this structure. First, I will give you the complete AHS. Then, you can request the code for any part by asking for its `ref` (e.g., `@5`). You must not invent code; only request it using its `ref`.

---
PROJECT STRUCTURE (AHS):
[INSERT_YOUR_AHS_HERE]
---

Now, wait for my first instruction.
Installation
The recommended method is using pipx to keep your system clean and ensure ahs-cli is always available.

1. Install pipx
(You only need to do this once.)

pip install pipx
pipx ensurepath

(You may need to restart your terminal after this step.)

2. Install AHS-Compressor
pipx install git+[https://github.com/rcdrodrigo/ahs-compressor.git](https://github.com/rcdrodrigo/ahs-compressor.git)

3. Verify Installation
# Encodes the 'my_project' directory and saves the output to 'compressed.json'
ahs-cli encode ./my_project -o compressed.json
Usage
Command-Line Interface (CLI)
Encode a project:
# Encodes the 'my_project' directory and saves the output to 'compressed.json'
ahs-cli encode ./my_project -o compressed.json

Decode a project:
# Reads 'compressed.json' and restores the code in the 'my_project_restored' directory
ahs-cli decode compressed.json -o ./my_project_restored

Web API
The application includes a FastAPI for integrations.

To start the server:
uvicorn app.main:app --reload

The server will be available at http://localhost:8000. API documentation can be found at http://localhost:8000/docs.

Contributing
Contributions are welcome! If you want to improve the tool, please feel free to fork the repository and submit a pull request. For more detailed guidelines, please see the CONTRIBUTING.md file (coming soon).

Roadmap
[ ] Publish the package to PyPI.

[ ] Add support for more languages (e.g., JavaScript, Java).

[ ] Create a Python client to interact with the API more easily.

[ ] Develop a VS Code extension for a seamless workflow.

❤️ Support This Project
AHS-Compressor is a free, open-source project. If you find this tool useful, please consider supporting its development.

⭐ Star the repository: This is the easiest way to show your support and helps the project gain visibility.

💝 Sponsor the author: You can also support the project financially. Every contribution is appreciated!

GitHub Sponsors

Buy Me a Coffee * Ko-fi ```

