from enum import Enum


class ContextMode(dict, Enum):
    MINIMAL = {"max_dim": 600, "quality": 30}
    NORMAL = {"max_dim": 800, "quality": 50}
    DETAILED = {"max_dim": 1200, "quality": 70}