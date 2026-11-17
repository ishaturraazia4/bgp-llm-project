import subprocess
import time
import json
from generate import generate_scenario

def check_bgp_status(router):
    # (Keep your existing check_bgp_status code here)
    cmd = f"docker exec -it clab-topo3-{router} vtysh -c 'show bgp summary'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def apply_fault(router, config_lines):
    """
    Pipes the LLM's configuration changes directly into the router's vtysh shell.
    """
    full_config = f"configure terminal\n{config_lines}\nexit\nwrite\n"
    cmd = f"docker exec -i clab-topo3-{router} vtysh"
    
    # We use 'input' to pass the multi-line string directly to standard input
    result = subprocess.run(cmd, shell=True, input=full_config, text=True, capture_output=True)
    return result.stdout

import json # Add this at the very top of validate.py with the other imports

if __name__ == "__main__":
    print("1. Requesting F1 fault scenario from LLM...")
    scenario = generate_scenario()

    if "error" in scenario:
        print("Pipeline stopped due to generation error:", scenario)
    else:
        # NEW: Save the JSON file to the scenarios/llm directory
        file_path = "../scenarios/llm/latest_scenario.json"
        with open(file_path, "w") as f:
            json.dump(scenario, f, indent=2)
        print(f"-> Scenario successfully saved to {file_path}")

        target_router = scenario.get("router", "r2")
        config_change = scenario.get("config_change", "")

        print(f"\n2. LLM generated the following mutation for {target_router}:")
        print(config_change)

        print(f"\n3. Applying configuration to {target_router}...")
        apply_fault(target_router, config_change)

        print("4. Waiting 3 seconds for BGP hold timers to trigger a session flap...")
        time.sleep(3)

        print(f"\n5. Checking independent BGP truth on {target_router}:")
        output = check_bgp_status(target_router)
        print(output)
