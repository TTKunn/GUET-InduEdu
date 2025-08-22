# PDF解析API测试

这个文件夹包含了用于测试PDF解析API的脚本。

## 文件说明

### 1. `simple_test.py` - 简单测试脚本
最简单的测试脚本，直接指定PDF文件路径进行测试。

**使用方法:**
```bash
# 确保API服务已启动
python start_api.py

# 在新的终端窗口中运行测试
cd test
python simple_test.py
```

**功能:**
- 健康检查
- PDF解析测试
- 显示解析结果和文档片段预览

### 2. `test_api.py` - 完整测试脚本
更完整的测试脚本，包含所有API接口的测试。

**使用方法:**
```bash
cd test
python test_api.py
```

**功能:**
- 健康检查
- PDF解析（不返回内容）
- PDF解析（返回内容）
- PDF解析并存储到Milvus（可选）
- 文档搜索（可选）

## 测试前准备

1. **启动API服务**
   ```bash
   python start_api.py
   ```
   确保看到类似输出：
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000
   INFO:     Application startup complete.
   ```

2. **准备PDF文件**
   - 准备一个或多个PDF文件用于测试
   - 记录文件的完整路径

3. **安装测试依赖**
   ```bash
   pip install requests
   ```

## 快速测试示例

```python
# 修改 simple_test.py 中的路径
pdf_paths = [
    r"C:\Users\YourName\Documents\your_test_file.pdf",
    # 添加更多PDF文件路径...
]
```

然后运行：
```bash
python test/simple_test.py
```

## 测试输出示例

```
开始测试PDF文件: C:\Users\test\document.pdf
1. 测试API健康状态...
✓ API服务正常
2. 开始解析PDF...
✓ PDF解析成功!
  - 任务ID: 12345678-1234-1234-1234-123456789abc
  - 文档片段数: 15
  - 总字符数: 12500

前3个文档片段预览:

--- 片段 1 ---
长度: 850 字符
内容: 这是PDF文档的第一段内容...
元数据: {"page": 1, "source": "document.pdf"}
```

## 注意事项

1. **API服务必须先启动** - 确保 `python start_api.py` 正在运行
2. **PDF文件路径** - 使用完整的绝对路径，避免相对路径问题
3. **文件格式** - 确保文件是有效的PDF格式
4. **网络连接** - 测试脚本通过HTTP请求与API通信

## 故障排除

### 常见错误

1. **连接错误**
   ```
   requests.exceptions.ConnectionError
   ```
   **解决方案:** 确保API服务已启动

2. **文件不存在**
   ```
   错误: 文件不存在 - /path/to/file.pdf
   ```
   **解决方案:** 检查文件路径是否正确

3. **API错误**
   ```
   PDF解析失败: 500
   ```
   **解决方案:** 检查API服务日志，确认PDF文件有效
