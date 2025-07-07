from vllm import LLM
from ocrflux.inference import parse

file_path = '/your/pdf/path.pdf'
# file_path = 'test.png'
llm = LLM(model="/XXXX/XXX/OCRFlux/models/OCRFlux-3B",gpu_memory_utilization=0.8,max_model_len=8192)
result = parse(llm,file_path)
# result�Ľṹ��
# {
#     "orig_path": str, # ԭʼ PDF ��ͼ���ļ���·�� 
#     "num_pages": int, # PDF �ļ��е�ҳ�� 
#     "document_text": str, # ת����� PDF ��ͼ���ļ��� Markdown �ı� 
#     "page_texts": dict, # PDF �ļ���ÿҳ�� Markdown �ı�������ҳ����������������ֵ�Ǹ�ҳ�� Markdown �ı� 
#     "fallback_pages": [int], # δ�ɹ�ת����ҳ�������б�
# }
if result != None:
    document_markdown = result['document_text']
    print(document_markdown)
    with open('./test.md','w') as f:
        f.write(document_markdown)
else:
    print("Parse failed.")
