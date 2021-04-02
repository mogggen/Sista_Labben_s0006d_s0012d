from enum import Enum


class ItemEnum(Enum):
    NONE = 0
    WOOD = 1
    IRON_ORE = 2


class GoalEnum(Enum):
    WOOD_GOAL = 0
    IRON_GOAL = 1
    SCOUT_GOAL = 2
    KILN_GOAL = 3
    SMITH_GOAL = 4
    SMELT_GOAL = 5
    SOLDIER_GOAL = 6
    BUILD_KILNS_GOAL = 7
    BUILD_SMITH_GOAL = 8
    BUILD_SMELTER_GOAL = 9
    BUILD_TRAINING_CAMP_GOAL = 10


class LaneEnum(Enum):
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2


class UpdateState(Enum):
    TREES = 0
    IRON = 1
    ENEMIES = 2


updateOrder = [
    UpdateState.IRON,
    UpdateState.ENEMIES,
    UpdateState.TREES,
    UpdateState.TREES,
    UpdateState.TREES,
    UpdateState.TREES,
    UpdateState.TREES,
    UpdateState.TREES,
    UpdateState.TREES,
    UpdateState.TREES,
    UpdateState.TREES,
    UpdateState.TREES]
