"""
纯视觉分析截图 - 读取图像并转换为 base64 供 AI 视觉分析
"""
import base64
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
SCREENSHOT_PATH = PROJECT_ROOT / "current_screenshot.png"

def analyze_screenshot_visually():
    """读取截图并准备供视觉分析"""
    print("=" * 60)
    print("视觉截图分析")
    print("=" * 60)
    
    if not SCREENSHOT_PATH.exists():
        print(f"\n❌ 截图不存在: {SCREENSHOT_PATH}")
        return None
    
    # 读取图像
    with open(SCREENSHOT_PATH, 'rb') as f:
        image_data = f.read()
    
    # 转换为 base64
    base64_image = base64.b64encode(image_data).decode('utf-8')
    
    print(f"\n📸 截图文件: {SCREENSHOT_PATH.name}")
    print(f"📊 文件大小: {len(image_data)} 字节 ({len(image_data)/1024:.2f} KB)")
    print(f"🔤 Base64 长度: {len(base64_image)} 字符")
    print(f"\n✅ 图像已加载，准备进行视觉分析")
    print(f"\n📋 Base64 数据 (前100字符):")
    print(f"   {base64_image[:100]}...")
    
    print("\n" + "=" * 60)
    print("请 AI 分析此图像中的图标数量和位置")
    print("=" * 60)
    
    return base64_image

if __name__ == "__main__":
    analyze_screenshot_visually()
