import http.client
import json
import base64
import time

print("Waiting 5 seconds for game to fully start...")
time.sleep(5)

print("Sending screenshot request to localhost:8765...")

try:
    conn = http.client.HTTPConnection("localhost", 8765, timeout=15)
    
    request_body = json.dumps({"tool": "get_screenshot", "arguments": {}})
    
    conn.request("POST", "/", request_body, {
        "Content-Type": "application/json",
        "Content-Length": str(len(request_body))
    })
    
    response = conn.getresponse()
    response_data = response.read().decode('utf-8')
    
    print(f"Response status: {response.status}")
    print(f"Response length: {len(response_data)} bytes")
    
    data = json.loads(response_data)
    
    if data.get('isError'):
        print(f"ERROR: {data}")
    elif data.get('content'):
        content = data['content'][0]
        if content.get('type') == 'image':
            img_data = base64.b64decode(content['data'])
            with open('current_screenshot.png', 'wb') as f:
                f.write(img_data)
            print(f"✅ Screenshot saved! Size: {len(img_data)} bytes")
            print(f"   MIME: {content.get('mimeType')}")
        else:
            print(f"Text response: {content.get('text')}")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
