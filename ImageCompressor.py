
from concurrent.futures import ThreadPoolExecutor

from PIL import Image
import os
from AbsImage import absImage
from MultiThreaded import multiThreaded

'''
图片大小压缩类
@:param input_path 输入图片的地址 可以是文件地址 也可以是文件夹地址
@:param output_path 输出图片地址 必须是文件夹地址
@:*args 继承自抽象图片处理类的参数，在本类中为图片压缩参数 用来实现压缩图片的问题
数据流为 input_path，output_path,*args输入 处理的图片输出到output_path中 
同时 countCompressor(self, in_path, out_path)函数将会计算压缩结果 以一个列表的形式返回到外观接口界面
返回的列表
facade_list.append({
                'file_name': file,
                'original_size': original_size,
                'compressed_size': compressed_size,
                'compression_percentage': compression_percentage
            })
'''


class imageCompressor(absImage):
    def __init__(self, *args):
        self.is_open = multiThreaded.get_is_multi()

    def imageProcess(self, input_path, output_path, *args):
        if len(args) != 1:
            raise ValueError("必须提供一个图像压缩参数")
        image_compressor = args[0]
        if os.path.isdir(output_path):
            if os.path.isfile(input_path):
                self.convert_single_file(input_path, output_path, image_compressor)
            elif os.path.isdir(input_path):
                self.convert_folder_file(input_path, output_path, image_compressor)
            else:
                raise ValueError(f"这个{input_path}既不是文件也不是文件夹.")
        else:
            raise ValueError(f"输出地址{output_path}必须为文件夹[ImageFormat.py]")

    # 单张图片压缩
    def convert_single_file(self, in_path, out_path, image_compressor):
        if not os.path.exists(in_path):
            print(f"输入文件不存在: {in_path}")
            return
        try:
            with Image.open(in_path) as img:
                img = img.convert("RGB")
                filename = os.path.basename(in_path)
                output_file_path = os.path.join(out_path, filename)
                output_file_path = os.path.abspath(output_file_path)  # 获取绝对路径
                output_file_path = os.path.normpath(output_file_path)  # 标准化路径格式
                img.save(output_file_path, quality=image_compressor)
                # print(f"图像已成功压缩并保存到: {out_path}\{filename}")
        except Exception as e:
            print(f"处理图像时出错: {e}")

    def convert_folder_file(self, in_path, out_path, image_compressor):
        # 处理压缩文件夹内的所有图片方法
        # PIL支持压缩的图片格式
        image_extensions = [
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.ico', '.webp',
            '.ppm', '.pgm', '.pcx', '.eps', '.tga', '.im', '.msp', '.sgi', '.spi', '.pdf'
        ]
        # 判断是否开启多线程
        if self.is_open:  # 开启多线程
            with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                # 遍历输入文件夹中的所有文件
                for imageName in os.listdir(in_path):
                    file_path = os.path.join(in_path, imageName)
                    # 检查文件扩展名是否为图片格式
                    if any(imageName.lower().endswith(ext) for ext in image_extensions):
                        executor.submit(self.convert_single_file, file_path, out_path, image_compressor)
                        print(f"{imageName}压缩成功并保存到: {out_path}/{imageName}")
                    else:
                        print(f"{imageName} 不是图片，跳过压缩")
        else:  # 不开启多线程
            # 整个文件夹压缩图片
            for imageName in os.listdir(in_path):
                # 检查文件扩展名是否为图片格式
                if any(imageName.lower().endswith(ext) for ext in image_extensions):
                    path = os.path.join(in_path, imageName)
                    self.convert_single_file(path, out_path, image_compressor)
                    print(f"{imageName}压缩成功并保存到: {out_path}\{imageName}")
                else:
                    print(f"{imageName} 不是图片，跳过压缩")

    def countCompressor(self, in_path, out_path):  # 返回外观接口进行显示的函数

        facade_list = []
        total_original_size = 0
        total_compressed_size = 0

        if os.path.isfile(in_path):  # 如果压缩的是一个图片的话
            file = os.path.basename(in_path)
            out_file_path = os.path.join(out_path, file)
            compressed_size = os.path.getsize(out_file_path)  # 压缩后的文件
            original_size = os.path.getsize(in_path)  # 压缩前的文件
            # 计算压缩百分比
            compression_percentage = ((original_size - compressed_size) / original_size) * 100

            facade_list.append({
                'file_name': file,
                'original_size': original_size,
                'compressed_size': compressed_size,
                'compression_percentage': compression_percentage
            })

            total_original_size += original_size
            total_compressed_size += compressed_size
        else:
            # 遍历文件夹中的所有文件
            for file in os.listdir(in_path):
                file_path = os.path.join(in_path, file)
                out_file_path = os.path.join(out_path, file)
                if os.path.isfile(file_path) and os.path.isfile(out_file_path):  # 确保文件存在
                    compressed_size = os.path.getsize(out_file_path)  # 压缩后的文件
                    original_size = os.path.getsize(file_path)  # 压缩前的文件
                    # 计算压缩百分比
                    compression_percentage = ((original_size - compressed_size) / original_size) * 100

                    facade_list.append({
                        'file_name': file,
                        'original_size': original_size,
                        'compressed_size': compressed_size,
                        'compression_percentage': compression_percentage
                    })

                    total_original_size += original_size
                    total_compressed_size += compressed_size

        # 计算整体压缩比
        if total_original_size > 0:
            overall_compression_percentage = ((total_original_size - total_compressed_size) / total_original_size) * 100
        else:
            overall_compression_percentage = 0

        print(f"未压缩之前的总文件大小: {total_original_size} 字节")
        print(f"压缩后的总文件大小: {total_compressed_size} 字节")
        print(f"整体压缩百分比: {overall_compression_percentage:.2f}%")

        for item in facade_list:
            print(f"文件: {item['file_name']}")
            print(f"原始大小: {item['original_size']} 字节")
            print(f"压缩后大小: {item['compressed_size']} 字节")
            print(f"压缩百分比: {item['compression_percentage']:.2f}%")

        # 返回压缩统计信息和整体压缩比
        return {
            'files': facade_list,
            'total_original_size': total_original_size,
            'total_compressed_size': total_compressed_size,
            'overall_compression_percentage': overall_compression_percentage
        }

'''
# --------------单元测试---------------
input_path = r"D:\test"
output_path = r"D:\accept"

image = imageCompressor()
time.sleep(10)
start_time = time.time()
image.is_open = False
print(image.is_open)
image.imageProcess(input_path, output_path, 50)
end_time = time.time()
print("总耗时:" + str(end_time - start_time))
information = image.countCompressor(input_path, output_path)
print(str((0.13486099243164062-0.06808209419250488)/0.13486099243164062)+"%")
print(information)
# 多线程总耗时:0.06808209419250488
# 单线程总耗时:0.13486099243164062
# 多线程模式下 使用测试例子 快了0.495168373263938%
'''