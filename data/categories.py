from enum import Enum

# === Enum Topik Kategori ===
class TopicCategory(Enum):
    programming_standard = "programming-standard"
    vane = "vane"
    robot_abb = "robot-abb"

# Mapping dari kategori ke ID channel forum
CATEGORY_TO_CHANNEL = {
    TopicCategory.programming_standard.value: 1359794185145684088,
    TopicCategory.vane.value: 1360061447278952529,
    TopicCategory.robot_abb.value: 1360061494389379172,
}
