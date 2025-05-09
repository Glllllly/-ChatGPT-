import os
import json
import re

# 文件路径
json_path = "conversations.json"  # 改成你的 JSON 文件名
output_dir = "chat_windows"
os.makedirs(output_dir, exist_ok=True)

# 读取 JSON 数据
with open(json_path, "r", encoding="utf-8") as f:
    conversations = json.load(f)

# 处理每个会话
for idx, convo in enumerate(conversations):
    title = convo.get("title", f"conversation_{idx+1}")
    safe_title = re.sub(r'[\\/*?:"<>|]', "_", title)[:50]

    mapping = convo.get("mapping", {})
    current = convo.get("current_node")
    message_chain = []

    # 向上追踪父节点
    while current and current in mapping:
        node = mapping[current]
        msg = node.get("message")
        if msg:
            role = msg.get("author", {}).get("role")
            if role == "user":
                prefix = "**You:**"
            elif role == "assistant":
                prefix = "**Assistant:**"
            else:
                prefix = None
            if prefix and msg.get("content") and msg["content"].get("parts"):
                part = msg["content"]["parts"][0]
                if isinstance(part, str):
                    message_chain.append(f"{prefix}\n{part.strip()}\n")
                elif isinstance(part, dict) and "text" in part:
                    message_chain.append(f"{prefix}\n{part['text'].strip()}\n")
                else:
                    message_chain.append(f"{prefix}\n[Unsupported content]\n")
        current = node.get("parent")

    # 反转顺序
    message_chain.reverse()

    # 写入 Markdown 文件
    with open(os.path.join(output_dir, f"{safe_title}.md"), "w", encoding="utf-8") as out:
        out.write(f"# {title}\n\n")
        out.write("\n\n".join(message_chain))

    print(f"已导出窗口：{title}")