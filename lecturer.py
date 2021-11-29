from dataclasses import dataclass
import json 

@dataclass
class Lecturer:
    name: str
    id: int
    availability_matrix: dict
    
def lecturer_factory(file_path: str):
    lecturers = []
    with open(file_path, 'r') as file:
        data = json.load(file)
    for lecturer in data:
        lecturers.append(Lecturer(lecturer['name'], lecturer['id'], lecturer['matrix']))
    return lecturers
if __name__ == "__main__":
    print(lecturer_factory('lecturer_data.json'))