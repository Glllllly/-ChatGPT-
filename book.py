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