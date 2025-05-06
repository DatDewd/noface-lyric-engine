from flask import Flask, request, jsonify
import json
from pathlib import Path

app = Flask(__name__)

# Path to your rap config JSON file
CONFIG_PATH = Path("rap_config.json")

@app.route("/update-config", methods=["POST"])
def update_config():
    try:
        # Load the existing config
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r") as f:
                config = json.load(f)
        else:
            return jsonify({"error": "rap_config.json not found"}), 404

        # Get JSON input from the request
        updates = request.get_json()

        # Update bpm_target
        if "bpm_target" in updates:
            config["bpm_target"] = updates["bpm_target"]

        # Update tone (set only one to true, others to false)
        if "tone" in updates:
            if "tone" in config:
                for key in config["tone"]:
                    config["tone"][key] = (key == updates["tone"])

        # Update temperature in generation_parameters
        if "temperature" in updates:
            if "generation_parameters" in config:
                config["generation_parameters"]["temperature"] = updates["temperature"]

        # Save the updated config
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)

        return jsonify({"message": "Config updated successfully", "updated_config": config})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
