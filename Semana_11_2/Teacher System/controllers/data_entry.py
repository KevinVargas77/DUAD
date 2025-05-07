from models.professor import Professor
from controllers.data_loader import load_sections_for_professor
from controllers.professor_utils import get_professor_name

def login_professor():
    prof_id = input("Enter your professor ID (e.g., prof02): ").strip()
    name = get_professor_name(prof_id)

    if not name:
        print("ID not found in the system.")
        return None

    sections = load_sections_for_professor(prof_id)
    if not sections:
        print("No sections found for this professor.")
        return None

    prof = Professor(prof_id, name, sections)
    print(f"\nWelcome, {prof.full_name}! {len(sections)} sections loaded.")
    return prof
