"""
综合测试脚本 - 测试所有 MCP 功能
Comprehensive Test Script - Test all MCP features
"""

import socket
import json
import sys
from pathlib import Path

# 配置
MCP_HOST = "127.0.0.1"
MCP_PORT = 8765

def send_mcp_request(tool_name, arguments=None):
    """发送 MCP 请求"""
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments or {}
        }
    }
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(10)
            sock.connect((MCP_HOST, MCP_PORT))
            
            request_json = json.dumps(request) + "\n"
            sock.sendall(request_json.encode('utf-8'))
            
            response_data = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response_data += chunk
                if b"\n" in response_data:
                    break
            
            response = json.loads(response_data.decode('utf-8'))
            return response
    except Exception as e:
        return {"error": str(e)}

def test_scene_tree():
    """测试 1: 获取场景树结构"""
    print("\n" + "="*60)
    print("测试 1: 获取场景树结构 (get_scene_tree)")
    print("="*60)
    
    response = send_mcp_request("get_scene_tree")
    
    if "error" in response:
        print(f"❌ 失败: {response['error']}")
        return False
    
    result = response.get("result", {})
    content = result.get("content", [])
    
    if content:
        text = content[0].get("text", "")
        print(f"✅ 成功获取场景树")
        print(f"场景树预览 (前200字符):")
        print(text[:200] + "...")
        return True
    else:
        print("❌ 失败: 无内容返回")
        return False

def test_simulate_click():
    """测试 2: 模拟点击"""
    print("\n" + "="*60)
    print("测试 2: 模拟点击 (simulate_click)")
    print("="*60)
    
    # 点击屏幕中心
    response = send_mcp_request("simulate_click", {"x": 640, "y": 360})
    
    if "error" in response:
        print(f"❌ 失败: {response['error']}")
        return False
    
    result = response.get("result", {})
    content = result.get("content", [])
    
    if content:
        text = content[0].get("text", "")
        print(f"✅ 成功: {text}")
        return True
    else:
        print("❌ 失败: 无内容返回")
        return False

def test_game_state():
    """测试 3: 获取游戏状态"""
    print("\n" + "="*60)
    print("测试 3: 获取游戏状态 (get_game_state)")
    print("="*60)
    
    response = send_mcp_request("get_game_state")
    
    if "error" in response:
        print(f"❌ 失败: {response['error']}")
        return False
    
    result = response.get("result", {})
    content = result.get("content", [])
    
    screenshot_found = False
    game_state_found = False
    
    for item in content:
        if item.get("type") == "image":
            screenshot_found = True
            data_len = len(item.get("data", ""))
            print(f"✅ 截图: {data_len} 字符 (base64)")
        elif item.get("type") == "text":
            game_state_found = True
            text = item.get("text", "")
            try:
                game_data = json.loads(text)
                grid_state = game_data.get("gridState", {})
                icons = grid_state.get("icons", [])
                print(f"✅ 游戏状态: {len(icons)} 个图标")
                
                # 统计图标类型
                icon_types = {}
                for icon in icons:
                    icon_type = icon.get("iconType", "Unknown")
                    icon_types[icon_type] = icon_types.get(icon_type, 0) + 1
                
                print(f"图标类型分布:")
                for icon_type, count in sorted(icon_types.items()):
                    print(f"  - {icon_type}: {count}")
            except:
                print(f"✅ 游戏状态数据 (前100字符): {text[:100]}...")
    
    if screenshot_found and game_state_found:
        print("✅ 测试通过: 截图和游戏状态都已获取")
        return True
    else:
        print(f"❌ 失败: 截图={screenshot_found}, 游戏状态={game_state_found}")
        return False

def main():
    """主测试函数"""
    print("="*60)
    print("MCP 功能综合测试")
    print("="*60)
    print(f"目标服务器: {MCP_HOST}:{MCP_PORT}")
    print("\n请确保:")
    print("1. Godot 游戏正在运行 (F5)")
    print("2. MCP 服务器已启动 (端口 8765)")
    print("\n按 Enter 开始测试...")
    input()
    
    results = []
    
    # 运行所有测试
    results.append(("场景树结构", test_scene_tree()))
    results.append(("模拟点击", test_simulate_click()))
    results.append(("游戏状态捕获", test_game_state()))
    
    # 总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status}: {name}")
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
        return 0
    else:
        print(f"\n⚠️  {total - passed} 个测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
