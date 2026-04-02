# Frontend-Only Migration Options (No-JS Stack)

This document outlines three strategies to convert the `smart-investor` application into a Single Page Application (SPA) that runs entirely in the browser without a traditional backend. This approach allows for easy, free deployments (GitHub Pages, Cloudflare Pages, etc.) while keeping the core logic in Python.

---

## 1. PyScript (Easiest Migration)
PyScript allows you to run Python code directly in HTML using WebAssembly (via Pyodide or MicroPython).

*   **How it works:** You include the PyScript runtime in your `<head>`. You replace your Vanilla JS logic with a `<script type="py">` block that calls your existing Python agents.
*   **Implementation Strategy:**
    *   **UI:** Keep your existing `index.html` and Tailwind CSS.
    *   **Logic:** Move your `agents/` folder into the root of your static site. Use `<py-config>` to list dependencies like `openai` and `pyodide-http` (to patch requests for browser compatibility).
    *   **DOM Interaction:** Use the `pyscript` Python module to read inputs and write the markdown results back to your existing `div` containers.
*   **Best for:** Developers who want to keep their current UI design and reuse their existing Python agent files with minimal modifications.

---

## 2. Brython (Fastest Performance)
Brython is a Python 3 implementation for client-side web programming that translates Python code into JavaScript on the fly.

*   **How it works:** It provides a `browser` module that allows for highly Pythonic DOM manipulation (e.g., `document["btn"].bind("click", handler)`).
*   **Implementation Strategy:**
    *   **UI:** Keep your existing HTML and CSS.
    *   **Logic:** Instead of using the official OpenAI/Google SDKs (which might have complex C-dependencies incompatible with Brython), you would use Brython's `browser.ajax` module to make standard HTTP REST calls directly to the AI providers.
*   **Best for:** Applications where fast initial load times are critical and the developer is comfortable writing raw API requests instead of using specialized SDKs.

---

## 3. Flet (Pure Python - No HTML/CSS)
Flet is a framework based on Flutter that enables building interactive web apps using only Python.

*   **How it works:** You build the UI by assembling Python objects. Flet handles the translation to a WebAssembly/Flutter frontend during the build process (`flet publish`).
*   **Implementation Strategy:**
    *   **UI:** Completely remove `index.html` and `style.css`. Rebuild the layout using Flet controls (`ft.View`, `ft.TextField`, `ft.Column`).
    *   **Logic:** Import and call your agents directly within the Flet event handlers.
*   **Best for:** Developers who want to avoid HTML/CSS/JS entirely and prefer a structured, component-based UI framework written purely in Python.

---

## Deployment Summary (Frontend-Only)

| Option | Keeps Current HTML? | Uses Official SDKs? | Initial Load Speed | Python Style |
| :--- | :--- | :--- | :--- | :--- |
| **PyScript** | Yes | Yes (most) | Slow (1-3s) | Standard Python |
| **Brython** | Yes | No (use REST) | Fast | Browser-centric Python |
| **Flet** | No | Yes | Moderate | UI-as-Code |

### Recommendation
For `smart-investor`, **PyScript** is the most logical choice as it preserves the existing Tailwind design and allows for direct reuse of the complex agent logic and official SDKs.