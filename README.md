# Deep Privacy 🔒

Deep-Privacy is a tool for creating privacy reports about online tools. It uses a combination of web scraping and an LLM pipeline to autonomously search the internet for information and aggregate it into a personalized privacy report.

<img src="./docs/ui.jpg" alt="Deep Privacy UI" width="400">

## Usage

This project uses [pixi](https://pixi.sh/latest/) for dependency management.

To start off, set your OpenAI API key in <code>.env</code>.

Install dependencies:

```bash
pixi install
```

Start the UI:

```bash
pixi run ui
```

Alternatively, you can run the app in the terminal:

```bash
pixi run cli
```
