import urllib.request
import json
import websocket
import sys

def get_json(url):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        return None

def main():
    port = None
    ws_url = None
    
    for p in range(9222, 9235):
        data = get_json(f'http://127.0.0.1:{p}/json/list')
        if data:
            for page in data:
                url = page.get('url', '')
                if 'stage-admin.mygnjoy.com' in url:
                    port = p
                    ws_url = page.get('webSocketDebuggerUrl')
                    break
        if ws_url:
            break
            
    if not ws_url:
        print("Could not find the target page on CDP.")
        sys.exit(1)
        
    print(f"Found on port {port}: {ws_url}")
    
    ws = websocket.WebSocket()
    ws.connect(ws_url, suppress_origin=True)
    
    # We need to evaluate JS to get the outerHTML of the sidebar.
    js_code = """
        (function() {
            const logo = Array.from(document.querySelectorAll('*')).find(el => el.textContent.trim() === 'Admin Tools' || el.textContent.trim() === 'Gravity Admin Tools');
            const primaryLink = document.querySelector('a[href*="/member"]');
            const secondaryLink = document.querySelector('a[href*="/setting/profile"]');
            
            function getLCA(nodes) {
                if (nodes.length === 0) return null;
                let curr = nodes[0];
                while (curr) {
                    if (nodes.every(node => curr.contains(node))) {
                        return curr;
                    }
                    curr = curr.parentElement;
                }
                return null;
            }
            
            const container = getLCA([logo, primaryLink, secondaryLink].filter(Boolean));
            return container ? container.outerHTML : document.body.outerHTML;
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
    
    try:
        html = result['result']['result']['value']
        with open('C:\\Users\\GRAVITY\\Desktop\\Anti\\GM Tool\\exact_sidebar.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Extraction successful.")
    except KeyError:
        print("Failed to get HTML from evaluation result:", result)
        sys.exit(1)
        
if __name__ == "__main__":
    main()
