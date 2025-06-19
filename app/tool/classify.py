# coding:utf-8
import re
import fitz  # PyMuPDF的导入名
import glob
import time
import os
import threading

def glob_with_progress(pathname: str, recursive: bool = False, interval: float = 1.0):
    """
    带进度显示功能的glob函数包装器

    参数:
    pathname: 搜索路径，支持通配符
    recursive: 是否递归搜索子目录
    interval: 进度显示的时间间隔（秒）

    返回:
    匹配的文件路径列表
    """
    # 提取搜索目录用于状态显示


    # 定义停止标志和结果容器
    stop_event = threading.Event()
    result = []

    def glob_task():
        nonlocal result
        result = glob.glob(pathname, recursive=recursive)
        stop_event.set()  # 标记任务已完成

    def progress_task():
        start_time = time.time()

        while not stop_event.is_set():
                for i in range(3):
                    print(f'\rLoading{"." * i}{" " * (3 - i)}', end="", flush=True)
                    time.sleep(0.3)

        # 输出最终结果
        total_time = time.time() - start_time
        print(f"文件检索耗时 {total_time:.2f} 秒")

    # 启动glob任务线程
    glob_thread = threading.Thread(target=glob_task)
    glob_thread.start()

    # 启动进度显示线程
    progress_thread = threading.Thread(target=progress_task)
    progress_thread.start()

    # 等待glob任务完成
    glob_thread.join()

    # 等待进度线程完成最后的输出
    progress_thread.join(timeout=interval * 2)

    return result


def create_directory(path):
    try:
        os.makedirs(path, exist_ok=True)
        print(f"Directory '{path}' created successfully")
    except Exception as e:
        print(f"Error creating directory '{path}': {e}")
def progress_bar(total, current):
    bar_length = 30
    filled = int(bar_length * current / total)
    bar = '█' * filled + '░' * (bar_length - filled)
    print(f"\r|{bar}| {current/total:.1%}", end="", flush=True)

def classify_pdf(file_path, threshold_per_page=20):
    """
    判断PDF类型：富文本或图片为主
    
    Args:
        file_path (str): PDF文件路径
        threshold_per_page (int): 每页文本长度阈值，默认20字
    
    Returns:
        str: "image-based"（图片型）或"text-based"（富文本）
    """
    try:
        with fitz.open(file_path) as doc:
            total_text = 0
            num_pages = len(doc)
            
            if num_pages == 0:
                return "empty"
            
            for page in doc:
                text = page.get_text("text").strip()  # 提取纯文本并去除空白
                total_text += len(text)
            
            avg_text = total_text / num_pages
            return True if avg_text < threshold_per_page else False
    
    except Exception as e:
        print(f"Error: {e}")
        return "error"


def classify_ocr_pdf(PDF_DIR):

    create_directory('result')
    temp=False
    print(PDF_DIR)
    if PDF_DIR:
        print("Start...")
        pattern = PDF_DIR+'/**/*.pdf'
        time_format = "%Y%m%d%H%M%S"
        file = './result/'+time.strftime(time_format, time.localtime())+'.txt'
        f = open(file,'a+')
        pathList=glob_with_progress(pattern, recursive=True)
        #pathList=glob.glob(pattern, recursive=True)
        start_time = time.time()
        for i in range(0,len(pathList)):
            result = classify_pdf(pathList[i])
            name = re.split(r'[\\.|]',pathList[i])
            if result:
                temp=True
                f.write(f"{pathList[i]}\n")
            progress_bar(len(pathList), i+1)
        f.close()
        total_time = time.time() - start_time
        print(f"总耗时 {total_time:.2f} 秒")
        if temp:
            print("\nExist!")
        print("\nEnd")
        

