from dataclasses import dataclass, field


@dataclass
class Database_manager:
    courses: list = field(default_factory=list)
    lecturers: list = field(default_factory=list)
    buildings: list = field(default_factory=list)