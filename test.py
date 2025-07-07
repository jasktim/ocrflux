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
