import requests
import json

def get_windows_host_ip():
    return "127.0.0.1"

def generate_scenario(model="qwen2.5-coder:3b"):
    url = f"http://{get_windows_host_ip()}:11434/api/generate"
    
    # Define the strict schema and context required by the methodology
    system_prompt = """You are a network routing expert. You must respond ONLY with a valid JSON object matching this exact schema:
    {
      "fault_class": "F1|F2|F3|benign",
      "router": "r1|r2|r3",
      "config_change": "<bounded FRR config lines>",
      "claimed_effect": "<one sentence>",
      "expected_observations": {
        "command": "show bgp summary",
        "expected": "session down"
      }
    }"""

    user_prompt = """Topology: 3-router chain (r1-r2-r3).
    r1 AS: 100 (Neighbor to r2: 192.168.12.2)
    r2 AS: 200 (Neighbor to r1: 192.168.12.1, Neighbor to r3: 192.168.23.3)
    r3 AS: 300 (Neighbor to r2: 192.168.23.2)

    Task: Generate an F1 (Neighbor ASN mismatch) fault on r2 affecting its session with r1."""

    payload = {
        "model": model,
        "prompt": f"{system_prompt}\n\n{user_prompt}",
        "stream": False,
        "format": "json"  # Forces the API to strictly validate output as JSON
    }
    
    print(f"Requesting JSON scenario from Ollama...")
    
    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        
        raw_text = response.json().get("response", "")
        
        # Explicitly parse the string into a Python dictionary
        parsed_json = json.loads(raw_text)
        return parsed_json
        
    except requests.exceptions.RequestException as e:
        return {"error": f"Network Error: {e}"}
    except json.JSONDecodeError:
        return {"error": "JSON Parsing Error", "raw_output": raw_text}

if __name__ == "__main__":
    print("Testing structured JSON generation...")
    result = generate_scenario(model="qwen2.5-coder:3b")
    
    print("\n--- Parsed JSON Output ---")
    print(json.dumps(result, indent=2))
