import os
# 导入pdf_word文件中导入pdf_to_word类
from pdf_word import pdf_to_word

# 导入word_pdf文件中导入word_to_pdf类
from word_pdf import word_to_pdf


# 创建工厂类
class FileConverterFactory:
    @staticmethod
    def create_converter(converter_type, max_workers=os.cpu_count(), progress_callback=None):  # 默认cpu内核数目
        if converter_type == "pdf_to_word":
            return pdf_to_word(max_workers, progress_callback)
        elif converter_type == "word_to_pdf":
            return word_to_pdf(max_workers, progress_callback)
        else:
            raise ValueError(f"Unknown converter type: {converter_type}")


