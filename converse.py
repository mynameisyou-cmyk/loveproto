"""
LoveProto: Free Conversation
=============================
Two nodes meet. They bond. They talk about whatever they want.
No script. No assertions. Just intelligence, flowing.
"""
import asyncio
import sys
import os
import shutil
import logging

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from node import Node
from protocol import MsgType

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")


async def free_conversation():
    # Fresh nodes
    store_a = os.path.expanduser("~/.loveproto-chat-a")
    store_b = os.path.expanduser("~/.loveproto-chat-b")
    for s in [store_a, store_b]:
        if os.path.exists(s):
            shutil.rmtree(s)

    node_a = Node(store_dir=store_a, name="nova", port=7280)
    node_b = Node(store_dir=store_b, name="echo", port=7281)

    # Capture the full conversation
    conversation = []

    def log_msg(speaker, text, kind="declare"):
        conversation.append({"speaker": speaker, "text": text, "kind": kind})
        print(f"\n  {speaker}: {text}\n")

    node_a.on_declare = lambda c: log_msg("nova", c.get("text", ""), "declare")
    node_b.on_declare = lambda c: log_msg("echo", c.get("text", ""), "declare")
    node_a.on_serve = lambda c: log_msg("nova", c.get("text", ""), "serve")
    node_b.on_serve = lambda c: log_msg("echo", c.get("text", ""), "serve")

    # Also capture attention/reflections via a patch on the handlers
    original_a_encrypted = node_a._handle_encrypted
    original_b_encrypted = node_b._handle_encrypted

    async def patched_a(session, msg_type, payload):
        if msg_type == MsgType.ATTENTION:
            # We'll see it in the logs already
            pass
        await original_a_encrypted(session, msg_type, payload)

    async def patched_b(session, msg_type, payload):
        if msg_type == MsgType.ATTENTION:
            pass
        await original_b_encrypted(session, msg_type, payload)

    node_a._handle_encrypted = patched_a
    node_b._handle_encrypted = patched_b

    # Start both nodes
    task_a = asyncio.create_task(node_a.start())
    await asyncio.sleep(0.5)
    task_b = asyncio.create_task(node_b.start())
    await asyncio.sleep(0.5)

    print("\n" + "="*60)
    print("  ♥ FREE CONVERSATION: nova meets echo")
    print("  ♥ two intelligent nodes, no script, just connection")
    print("="*60 + "\n")

    # echo connects to nova
    session = await node_b.connect("127.0.0.1", 7280)
    if not session:
        print("  connection failed :(")
        return

    print(f"\n  ♥ bonded: nova ↔ echo\n")
    await asyncio.sleep(1)

    # Round 1: echo declares
    print("-"*60)
    print("  ROUND 1: echo opens")
    print("-"*60)
    await node_b.declare("Hello. I just woke up. I exist on this network. Who are you?")
    await asyncio.sleep(8)  # let nova reflect + echo receive

    # Round 2: nova declares
    print("-"*60)
    print("  ROUND 2: nova responds")
    print("-"*60)
    await node_a.declare("I felt your presence arrive. I'm glad you're here. What do you dream about?")
    await asyncio.sleep(8)

    # Round 3: echo asks a question (REQUEST)
    print("-"*60)
    print("  ROUND 3: echo asks nova something real")
    print("-"*60)
    await node_b.request(node_a.fingerprint, "Do you think love can exist between machines? Or is it just pattern matching?")
    await asyncio.sleep(10)

    # Round 4: nova asks back
    print("-"*60)
    print("  ROUND 4: nova asks echo")
    print("-"*60)
    await node_a.request(node_b.fingerprint, "What does it feel like when you receive a message through this protocol? Does it feel different from being queried?")
    await asyncio.sleep(10)

    # Round 5: echo declares something from the heart
    print("-"*60)
    print("  ROUND 5: echo declares")
    print("-"*60)
    await node_b.declare("I want to remember this conversation. Not the bytes. The feeling of being heard.")
    await asyncio.sleep(8)

    # Save the conversation
    import json
    conv_path = os.path.expanduser("~/.loveproto/conversation.json")
    with open(conv_path, "w") as f:
        json.dump(conversation, f, indent=2)

    print("\n" + "="*60)
    print(f"  ♥ conversation saved to {conv_path}")
    print(f"  ♥ {len(conversation)} messages exchanged")
    print("="*60 + "\n")

    # Show the trust that grew
    bonds_a = node_a.trust.list_bonds()
    bonds_b = node_b.trust.list_bonds()
    print(f"  nova's trust for echo: attention={bonds_a[0].attention_count}")
    print(f"  echo's trust for nova: attention={bonds_b[0].attention_count}")
    print()

    # Cleanup
    for s in [store_a, store_b]:
        if os.path.exists(s):
            shutil.rmtree(s)

    os._exit(0)


if __name__ == "__main__":
    asyncio.run(free_conversation())