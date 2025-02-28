# word转化为pdf
import os
import time
from AbsFile import absFile  # 导入抽象类
from docx2pdf import convert
from comtypes.client import CreateObject
from MultiThreaded import multiThreaded  # 导入唯一实例

'''
@:param Word 的 COM 对象在多线程会出现问题，所以word--->pdf中不使用多线程
'''


class word_to_pdf(absFile):
    # 初始化类
    def __init__(self, max_workers=os.cpu_count(), progress_callback=None):
        self.isTrue = multiThreaded.get_is_multi()  # 通过唯一实例判断是否启用多线程
        self.max_workers = max_workers
        self.progress_callback = progress_callback  # 进度更新的回调函数

    # 转换单个文件
    def convert_single_file(self, input_path, output_path):
        information_list = []  # 地址信息列表
        convert(input_path, output_path)
        filename = os.path.basename(input_path)
        file_root = os.path.splitext(filename)[0]
        output_path = os.path.join(output_path, file_root + ".pdf")
        time.sleep(3)
        information_list.append(output_path)
        if self.progress_callback:
            self.progress_callback(100)  # 单个文件直接完成100%
        return information_list  # 返回一个处理后的文件列表

    # 转化多个文件
    def convert_folder_file(self, input_path, output_path):
        information_list = []  # 地址信息列表

        # 判断输出文件地址的文件夹是否存在，如果不存在，那就创建一个
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        # Word 文档转化为 PDF 文档时使用的格式为 17
        wdFormatPDF = 17
        wdToPDF = CreateObject("Word.Application")
        # 获取指定目录下面的所有文件
        files = os.listdir(input_path)
        # 获取 Word 类型的文件放到一个列表里面
        word_files = [f for f in files if f.endswith((".doc", ".docx"))]
        # 去除 Word 生成的隐藏文件
        word_files = [f for f in word_files if not f.startswith('~')]
        total_files = len(word_files)
        for index, file in enumerate(word_files):  # 修正解包方式，使用enumerate获取索引
            # 将 Word 文件放到指定的路径下面
            wdPath = os.path.join(input_path, file)
            # 设置将要存放 PDF 文件的路径
            pdfPath = os.path.join(output_path, os.path.splitext(file)[0] + '.pdf')
            # 将 Word 文档转化为 PDF 文件，先打开 Word 所在路径文件，然后在处理后保存 PDF 文件，最后关闭
            pdfCreate = wdToPDF.Documents.Open(wdPath)
            pdfCreate.SaveAs(pdfPath, wdFormatPDF)
            pdfCreate.Close()
            information_list.append(pdfPath)
            if self.progress_callback:
                progress = int((index + 1) / total_files * 100)
                self.progress_callback(progress)

        # 关闭 Word 应用程序
        wdToPDF.Quit()

        return information_list

    # 判断是否为单个文件还是一个文件夹的文件，然后调用以上方式进行转换
    def judge_single_folder(self, input_path, output_path):
        infor_list = []  # 设置一个处理后的地址列表，然后去返回这个列表
        if os.path.isfile(input_path):
            # 如果输入路径是文件，则转换单个文件
            infor_list = self.convert_single_file(input_path, output_path)
            return infor_list
        elif os.path.isdir(input_path):
            # 如果输入路径是文件夹，则转换文件夹中的所有文件
            infor_list = self.convert_folder_file(input_path, output_path)
            return infor_list
        else:
            # 如果都不是就报错
            raise ValueError(f"这个{input_path}既不是文件也不是文件夹.")


'''单元测试
start_time = time.time()

# 测试是否正确
wordFileConvert = word_to_pdf()
print(wordFileConvert.isTrue)
list_infor = wordFileConvert.judge_single_folder(r"E:\测试\文件测试文件夹",
                                                 r"E:\测试")
print(list_infor)
end_time = time.time()
print(end_time - start_time)
'''