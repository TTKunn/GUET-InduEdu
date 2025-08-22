"""
日志工具模块
基于loguru的日志配置
"""
import sys
import os
from loguru import logger
try:
    from config import LOG_DIR, LOG_LEVEL, LOG_FORMAT
except ImportError:
    # 如果无法导入配置，使用默认值
    import os
    LOG_DIR = "./logs"
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "detailed"
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR, exist_ok=True)

# 确保日志目录存在
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)

class PDFAnalyserLogger:
    """PDF分析器日志类"""
    
    def __init__(self):
        self.logger = logger
        # 清空所有默认设置
        self.logger.remove()
        
        # 根据配置设置日志格式
        if LOG_FORMAT == 'simple':
            format_str = "<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>"
        else:  # detailed
            format_str = (
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                "{process.name} | "
                "{thread.name} | "
                "<cyan>{module}</cyan>.<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                "<level>{level}</level>: "
                "<level>{message}</level>"
            )
        
        # 添加控制台输出
        self.logger.add(
            sys.stdout,
            level=LOG_LEVEL,
            format=format_str,
            colorize=True
        )
        
        # 添加文件输出
        log_file_path = os.path.join(LOG_DIR, "pdf_analyser.log")
        self.logger.add(
            log_file_path,
            level=LOG_LEVEL,
            encoding='UTF-8',
            format='{time:YYYY-MM-DD HH:mm:ss} - {process.name} | {thread.name} | {module}.{function}:{line} - {level} - {message}',
            rotation="10 MB",  # 日志文件大小限制
            retention=20,      # 保留文件数量
            compression="zip"  # 压缩旧日志
        )
    
    def get_logger(self):
        """获取日志器实例"""
        return self.logger

# 创建全局日志实例
log = PDFAnalyserLogger().get_logger()

if __name__ == '__main__':
    # 测试日志功能
    log.debug("这是一个调试消息")
    log.info("这是一个信息消息")
    log.warning("这是一个警告消息")
    log.error("这是一个错误消息")
    
    # 测试异常捕获
    @log.catch
    def test_exception():
        return 1 / 0
    
    test_exception()
