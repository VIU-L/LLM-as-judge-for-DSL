from utils import CfgNode
from pathlib import Path

BASE_PATH = Path(__file__).parent.parent
print("Config loaded, base_path=",BASE_PATH)    

CONFIG = CfgNode(
    TUTO_PATH = BASE_PATH / 'docs',
    REF_PATH = BASE_PATH / 'reference' / 'reference',
    CHALLENGES_PATH = BASE_PATH / 'mychallenges',
)