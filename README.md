# 一、OCRFlux简介

OCRFlux是一个基于多模态大语言模型的工具包，专注于将PDF文档和图像高效转换为干净、可读的**纯Markdown**文本。该项目旨在显著提升现有技术的性能水平，并提供在线演示供用户试用。
#### 主要功能
- **整个文件解析**：支持批量处理完整文档。
- **页面级处理**：
  - 将页面内容转换为文本，保持自然阅读顺序，即使面对多栏布局、图形或插图。
  - 支持复杂表格和数学方程的识别。
  - 自动移除页眉和页脚。
  - 实现跨页表格和段落的无缝合并。
- **跨页合并功能**：
  - 表格跨页合并：处理跨多个页面的表格数据。
  - 段落跨页合并：确保文本段落在不同页面间的连贯性。
#### 关键特性
- **卓越的解析质量**：在基准测试OCRFlux-bench-single上，其Edit Distance Similarity (EDS)显著优于主流基线模型：
  - 比olmOCR-7B-0225-preview高0.095（从0.872提升至0.967）。
  - 比Nanonets-OCR-s高0.109（从0.858提升至0.967）。
  - 比MonkeyOCR高0.187（从0.780提升至0.967）。
- **首创的跨页合并支持**：该项目是首个在开源工具中实现原生跨页表格和段落合并的功能。
- **高效部署**：基于3B参数的视觉语言模型（VLM），可在GTX 3090 GPU等设备上运行，确保实际应用的可访问性。

# 二、本地部署
项目github：[AlexeiLeery/ocrflux](https://github.com/AlexeiLeery/ocrflux)
在线体验：[Demo ](https://ocrflux.pdfparser.io/)

在官方教程中，使用huggingface下载模型，使得大部分没有魔法的小伙伴无法尝鲜。
接下来我将介绍我的个人做法：

## 1、配置环境
### Installation

Requirements:
 - Recent NVIDIA GPU (tested on RTX 3090, 4090, L40S, A100, H100) with at least 12 GB of GPU RAM
 - 20GB of free disk space

You will need to install poppler-utils and additional fonts for rendering PDF images.

Install dependencies (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install poppler-utils poppler-data ttf-mscorefonts-installer msttcorefonts fonts-crosextra-caladea fonts-crosextra-carlito gsfonts lcdf-typetools
```

以上为官方要求下载的环境依赖，但是我实际测试只需要下载poppler-utils即可。代码如下：
```bash
sudo apt-get update
sudo apt-get install poppler-utils
```

## 2、安装库

```bash
conda create -n ocrflux python=3.11
conda activate ocrflux

git clone https://github.com/chatdoc-com/OCRFlux.git
cd ocrflux

pip install -e . --find-links https://flashinfer.ai/whl/cu124/torch2.5/flashinfer/
pip install modelscope
```

## 3、使用modelscope下载模型

```bash
mkdir models
modelscope download --model ChatDOC/OCRFlux-3B --local_dir ./models/OCRFlux-3B
```

## 4、运行代码
在项目根目录创建一个测试 test.py

```python
from vllm import LLM
from ocrflux.inference import parse

file_path = '/your/pdf/path.pdf'
# file_path = 'test.png'
llm = LLM(model="/XXXX/XXX/OCRFlux/models/OCRFlux-3B",gpu_memory_utilization=0.8,max_model_len=8192)
result = parse(llm,file_path)
# result的结构：
# {
#     "orig_path": str, # 原始 PDF 或图像文件的路径 
#     "num_pages": int, # PDF 文件中的页数 
#     "document_text": str, # 转换后的 PDF 或图像文件的 Markdown 文本 
#     "page_texts": dict, # PDF 文件中每页的 Markdown 文本，键是页码索引（整数），值是该页的 Markdown 文本 
#     "fallback_pages": [int], # 未成功转换的页码索引列表
# }
if result != None:
    document_markdown = result['document_text']
    print(document_markdown)
    with open('./test.md','w') as f:
        f.write(document_markdown)
else:
    print("Parse failed.")

```
运行代码test.py，即可输出markdown格式的pdf内容

**测试效果：**
![jasktim](https://i-blog.csdnimg.cn/direct/ecea7990200c48edad8139901c1e4dda.png)
其他效果可自行测试。