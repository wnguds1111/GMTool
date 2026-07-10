import urllib.request
import json
import websocket
import time
import sys

def get_json(url, method='GET'):
    req = urllib.request.Request(url, method=method)
    with urllib.request.urlopen(req, timeout=5) as response:
        return json.loads(response.read().decode('utf-8'))

def main():
    target_url = "https://gravity.dooray.com/share/pages/bGeuw48xRmaHvaAzHK13Ww/4372058128209637381"
    
    # Check if we can find a port
    port = None
    for p in range(9222, 9235):
        try:
            data = get_json(f'http://127.0.0.1:{p}/json/list')
            if isinstance(data, list):
                port = p
                break
        except Exception:
            pass
            
    if not port:
        print("No CDP port found.")
        sys.exit(1)
        
    print(f"Using CDP port {port}")
    
    # Open new tab
    new_page_info = get_json(f'http://127.0.0.1:{port}/json/new?{urllib.parse.quote(target_url)}', method='PUT')
    ws_url = new_page_info['webSocketDebuggerUrl']
    page_id = new_page_info['id']
    
    ws = websocket.WebSocket()
    ws.connect(ws_url, suppress_origin=True)
    
    # Wait for the page to load
    time.sleep(5)
    
    js_code = """
        (function() {
            return document.body.innerText;
        })();
    """
    
    msg = {
        "id": 1,
        "method": "Runtime.evaluate",
        "params": {
            "expression": js_code,
            "returnByValue": True
        }
    }
    
    ws.send(json.dumps(msg))
    result = json.loads(ws.recv())
    
    text = result.get('result', {}).get('result', {}).get('value', '')
    if not text:
        print("Failed to get text content.")
        print(result)
        sys.exit(1)
        
    with open('C:\\Users\\GRAVITY\\Desktop\\Anti\\GM Tool\\api_spec.md', 'w', encoding='utf-8') as f:
        f.write("# API 명세서\n\n")
        f.write(text)
        
    print("API Specification saved to api_spec.md")
    
    # Close tab
    req = urllib.request.Request(f'http://127.0.0.1:{port}/json/close/{page_id}', method='PUT')
    try:
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass

if __name__ == "__main__":
    main()
