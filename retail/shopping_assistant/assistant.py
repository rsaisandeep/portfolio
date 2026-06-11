import os
import json
import csv
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def load_products(path="products.csv"):
    with open(path) as f:
        return list(csv.DictReader(f))


def filter_products(products, category=None, color=None, max_price=None, in_stock_only=True):
    results = []
    for p in products:
        if category and category.lower() not in p["category"].lower():
            continue
        if color and color.lower() not in p["color"].lower():
            continue
        if max_price and float(p["price"]) > float(max_price):
            continue
        if in_stock_only and p["in_stock"].lower() != "true":
            continue
        results.append(p)
    return results


tools = [
    {
        "name": "search_products",
        "description": "Search the product catalog based on filters like category, color, max price, and stock availability.",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "description": "Product category e.g. jacket, shirt, shoes"},
                "color": {"type": "string", "description": "Color of the product"},
                "max_price": {"type": "number", "description": "Maximum price in USD"},
                "in_stock_only": {"type": "boolean", "description": "Only return in-stock items", "default": True}
            }
        }
    }
]


def run_tool(name, inputs, products):
    if name == "search_products":
        results = filter_products(products, **inputs)
        if not results:
            return "No products found matching your criteria."
        lines = [f"- {p['name']} ({p['color']}, size {p['size']}) — ${p['price']}" for p in results[:5]]
        return "\n".join(lines)


def chat():
    products = load_products()
    messages = []
    system = (
        "You are a helpful retail shopping assistant. "
        "When the user describes what they're looking for, use the search_products tool to find matching items. "
        "Be friendly and suggest alternatives if nothing matches exactly."
    )

    print("Shopping Assistant ready. Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit"):
            break

        messages.append({"role": "user", "content": user_input})

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=system,
            tools=tools,
            messages=messages
        )

        # handle tool use loop
        while response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = run_tool(block.name, block.input, products)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                system=system,
                tools=tools,
                messages=messages
            )

        reply = next((b.text for b in response.content if hasattr(b, "text")), "")
        messages.append({"role": "assistant", "content": reply})
        print(f"\nAssistant: {reply}\n")


if __name__ == "__main__":
    chat()
