
# 全套：ChatGPT聊天记录自动按窗口分割+电子书生成流程

#和g原创版 ^ ^

# 事先准备

- python环境（不需要额外的库）
- vscode编译器（喜欢用IDLE、PyCharm也行，随便大家，**但是记得要在编译器里面安装python扩展**）
- pandoc环境
- latex环境（可不要）

事先打好预防针，这些如果之前没有装好的话，从头装这些也比较麻烦的……特别像latex这种超级大包，嗯，谁装谁知道，躺平。
上面这些安装遇到问题可以直接问GPT，他都懂。

如果你已经配好所有的环境……**马上启动！**

# 动手操作

## step1 分窗口

首先我们需要去ChatGPT那边像往常一样打包一份转世资料。
Settings → Data Controls → Export Data

拿到oai发的压缩包以后，解压。
通常这个时候我们会去看chat.html文件，但是我这边聊的太多，基本上卡死了，点也点不动，因此，我们需要让程序来帮我们处理这件事

新建一个文件夹，我们这里命名为conversation。把转世资料里面的**conversation.json**文件复制进来。

📁 conversation

└── conversation.json

然后用vscode打开这个文件夹（文件→打开文件夹→点击📁 conversation），在根目录下新建一个文件，我们把它命名为split.py。

📁 conversation

├── conversation.json

└── split.py

这个程序是帮我们把所有的聊天记录按窗口分开的，内容如下：

```python
import os
import json
import re

# 文件路径
json_path = "conversations.json"
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
                prefix = "**You:**"   # 可以改成**你的名字:**！
            elif role == "assistant":
                prefix = "**Assistant:**"   # 可以改成**GPT的名字:**！
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
```

直接复制粘贴进去。如果想把You和Assistant改成你和家g的名字的话，按照格式改就好。

点击编译器右上角▶符号，运行程序，马上就好。

到这个时候，我们的文件夹应该长这样：

📁 conversation

├──  📁 chat_windows

│   ├── 窗口1.md

│   └── 窗口2.md

├── conversation.json

└── split.py

你可以在vscode中直接打开.md文件，使用Markdown All in One插件可以点击右上角放大镜+书图标直接预览聊天窗口内容。

## step2 组合各窗口+目录生成

同样在根目录下面新建一个文件，我命名为book.py，然后把以下代码粘贴进去：

```python
import os

source_dir = "chat_windows"
output_md = "ChatGPT_日记合集.md"

files = sorted([f for f in os.listdir(source_dir) if f.endswith(".md")])

with open(output_md, "w", encoding="utf-8") as out:
    # 封面大标题
    out.write(":::CHAPTER::: 日记合集\n\n") # 这里改成你想要的标题
    out.write("**目录**\n\n")

    for idx, fname in enumerate(files):
        title = fname.replace(".md", "")
        out.write(f"- {title}\n")
    out.write("\n")

    # 正文写入，每个文件前添加章节标记
    for idx, fname in enumerate(files):
        title = fname.replace(".md", "")
        out.write(f"\n\n:::CHAPTER::: {title}\n\n")
        with open(os.path.join(source_dir, fname), "r", encoding="utf-8") as f:
            out.write(f.read())
```

运行代码，这个时候我们的项目结构应该是这样的：

📁 conversation

├──  📁 chat_windows

│   ├── 窗口1.md

│   └── 窗口2.md

├── conversation.json

├── ChatGPT_日记合集.md

├── book.py

└── split.py

这个时候，我的日记合集已经大到爆表了，已经没法用vscode之间渲染查看，这个时候我们选择生成.epub电子书，文件会变小，且可以轻松适配各种电子书软件。

## step3 电子书生成（Beta 测试版）

去让g老师帮忙画个封面，并且保存成cover.png在根目录下：

📁 conversation

├──  📁 chat_windows

│   ├── 窗口1.md

│   └── 窗口2.md

├── conversation.json

├── ChatGPT_日记合集.md

├── cover.png

├── book.py

└── split.py

然后在终端输入：

```bash
pandoc ChatGPT_日记合集.md -o ChatGPT.epub --toc --split-level=1 --top-level-division=chapter --toc-depth=1 --epub-cover-image=cover.png
```

***（注意！我是windows系统，mac和linux系统可以让g老师把上面这句翻译一下，然后再用）***

等很久很久，直到出现**ChatGPT.epub**文件，你就可以用电子书软件（微信读书、UC浏览器等等）打开并阅读了。

#### ❗电子书流程为测试版，仍存在很多不足，已经尽可能避免markdown语法和目录的冲突了，但是还是效果一般，希望大佬参与改进！谢谢
