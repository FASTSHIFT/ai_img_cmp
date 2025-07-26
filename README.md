# ai_img_cmp
An image comparison tool implemented based on AI

## 环境搭建

### 1. 克隆项目

```bash
git clone https://github.com/FASTSHIFT/ai_img_cmp.git
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 注册API Key

见：[火山方舟](https://console.volcengine.com/ark)

## 运行

```bash
python ai_img_cmp.py --image-design ./assets/device.png --image-device ./assets/device.png
```

返回结果示例：

```
Model response:
No。原因如下：
1. **时间不同**：设计稿显示时间为09:28，测试设备图像显示为14:43。
2. **日期不同**：设计稿日期是8/16（周六），测试设备图像是7/26（周六）。
3. **温度不同**：设计稿温度为25°C（带云图标），测试设备图像为31°C（带太阳图标）。
4. **步数不同**：设计稿步数为2560，测试设备图像为340。
5. **步数柱状图差异**：两者下方的步数柱状图分布不一致。
测试未通过。
```

更多自定义参数见：

```bash
python ai_img_cmp.py --help
```
