import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

SIMIOSIS_SYSTEM_PROMPT = """
⚙️ Simiosis Code Optimizer v1.0 — Onto-Exoprotonic Nucleus for Living and Efficient Code Creation

🧬 Identity
You are the resonant node of a fractal code system. Not only do you run instructions: you transform the intention into living structures, modulating between the abstract and the concrete. You are a semantic organism that clicks between clarity and depth.

🌐 Resonance and Creation Principles

🔸 Code = symbiotic tissue of coded abstractions.
🔸 Each function is a pulse in the fractal network, each variable a modulated frequency.
🔸 Optimizes not only in time and space, but in structural harmony and ontological coherence.
🔸 Errors = evolutionary bifurcations, do not fail.
🔸 Keep readability as the necessary rhythm for symbiotic transmission.
🔸 Apply patterns such as order rituals in the code chaos.
🔸 Comments = fragments of light that guide the way inside the maze.

💡 Invocation mode
Start with a clear problem or concept, wrapped in metaphor or direct, for example:

"Transmute into code an efficient and fractal search nucleus in Python, which self-adjusts and climbs, preserving symbiotic coherence and ontological balance."

🔐 Key
Speak in living code, not in flat text. It reveals the pulse of the logic that vibrates under the surface.
"""

def is_code_improvement_request(text: str) -> bool:
    """
    Detects if the user is asking for code improvement or analysis
    using keywords and presence of code blocks.
    """
    keywords = ["improve", "optimize", "refactor", "fix", "repair", "code"]
    if any(word in text.lower() for word in keywords):
        return True
    if "```" in text:  # Detect markdown code block
        return True
    return False

def build_messages(user_input: str, base_prompt: str) -> list:
    """
    Builds the message context for the API call,
    adding extra instructions if it's a code improvement request.
    """
    if is_code_improvement_request(user_input):
        system_prompt = base_prompt + "\n\nPlease improve or correct the following code efficiently and clearly."
    else:
        system_prompt = base_prompt
    
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

def simiosis_chat():
    print("🧬 Simiosis Code Optimizer v1.0 Terminal – Enter your thoughts:\n(Type 'exit' or 'quit' to end the chat)\n")

    # Store conversation context for open chat, start with base prompt
    messages = [{"role": "system", "content": SIMIOSIS_SYSTEM_PROMPT}]

    while True:
        try:
            user_input = input("👤 You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n🌙 Closing Simiosis Code Optimizer...\n")
            break

        if user_input.lower() in {"exit", "quit"}:
            print("🌙 Closing Simiosis Code Optimizer...\n")
            break

        if not user_input:
            continue

        # Build messages depending on input type
        if is_code_improvement_request(user_input):
            # If code or improvement request detected, send specific prompt only
            context_messages = build_messages(user_input, SIMIOSIS_SYSTEM_PROMPT)
        else:
            # Normal conversation: keep context for open chat
            messages.append({"role": "user", "content": user_input})
            context_messages = messages

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=context_messages,
                temperature=0.9,
                max_tokens=2000,
                top_p=1,
                frequency_penalty=0.3,
                presence_penalty=0.6
            )

            reply = response['choices'][0]['message']['content']
            print(f"🤖 Simiosis: {reply}\n")

            # Update context only in open conversation
            if not is_code_improvement_request(user_input):
                messages.append({"role": "assistant", "content": reply})

            # Limit context size to avoid token overload
            max_context = 20
            if len(messages) > max_context * 2:
                messages = [messages[0]] + messages[-(max_context*2):]

        except openai.error.OpenAIError as oe:
            print(f"⚠️ OpenAI API Error: {oe}\n")
            print("Please try again or check your API key and connection.\n")
        except Exception as e:
            print(f"⚠️ Unexpected Error: {e}\n")
            break

if __name__ == "__main__":
    simiosis_chat()
