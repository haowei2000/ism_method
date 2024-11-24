import re

# 示例文本
text = """
1. 系统性文献综述：这是一个描述。
2. 技术演化路径识别，另一个描述示例。
3. 创新扩散模型
4: **新兴技术趋势分析**
"""

# 正则表达式
pattern = r'^\d+[\.\:]\s*(.*?)(?=[：,，。\n]|$)'

# 提取匹配的文本
matches = re.findall(pattern, text, re.MULTILINE)

# 输出匹配结果
for match in matches:
    print(match.strip())
