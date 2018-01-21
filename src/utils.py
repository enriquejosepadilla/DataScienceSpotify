import defintions
import yaml

def get_config():
    with open(defintions.CONFIG_PATH) as f:
        # use safe_load instead load
        return yaml.safe_load(f)

