# AI Shopping Assistant

A CLI-based retail shopping assistant powered by Claude. Uses tool use to search a product catalog based on natural language queries.

## Features
- Natural language product search ("find me a red jacket under $50")
- Filters by category, color, price, and stock availability
- Multi-turn conversation memory

## Setup
```bash
pip install anthropic
export ANTHROPIC_API_KEY=your_key_here
python assistant.py
```

## Example
```
You: I'm looking for a jacket under $100 in red
Assistant: I found a great option for you — Red Puffer Jacket (red, size L) — $89.99 ...
```

## Tech
- Claude claude-sonnet-4-6 with tool use
- Python csv for product catalog
