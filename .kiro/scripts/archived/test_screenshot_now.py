import requests
import json
import base64
import sys

print("Taking screenshot from Godot game...")

try:
    response = requests.post(
        'http://localhost:8765',
        json={'tool': 'get_screenshot', 'arguments': {}},
        timeout=15
    )
    
    data = response.json()
    print(f"Response received!")
    print(f"isError: {data.get('isError')}")
    
    if data.get('content'):
        content = data['content'][0]
        print(f"Content type: {content.get('type')}")
        
        if content.get('type') == 'image':
            print(f"✅ Image received! Data length: {len(content.get('data', ''))} chars")
            print(f"MIME type: {content.get('mimeType')}")
            
            # Save to file for verification
            img_data = base64.b64decode(content['data'])
            with open('current_screenshot.png', 'wb') as f:
                f.write(img_data)
            print(f"✅ Screenshot saved to current_screenshot.png")
        else:
            print(f"Text response: {content.get('text')}")
    else:
        print("No content in response")
        
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
