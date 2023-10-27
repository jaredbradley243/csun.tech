import ratemyprofessor
from accounts.models import ProfessorProfile
import logging


def fetch_and_update_rmp_data(professor_id):
    try:
        professor_object = ProfessorProfile.objects.get(id=professor_id)
        school = ratemyprofessor.get_school_by_name(
            "California State University - Northridge"
        )
        rmp_professor = ratemyprofessor.get_professor_by_school_and_name(
            school,
            f"{professor_object.user.first_name} {professor_object.user.last_name}",
        )

        prof_rating = rmp_professor.rating
        prof_would_take_again = rmp_professor.would_take_again
        prof_difficulty = rmp_professor.difficulty

        changes_made = False

        if prof_rating is not None:
            professor_object.rate_my_professor_rating = prof_rating
            changes_made = True
        if prof_would_take_again is not None:
            professor_object.rate_my_professor_would_take_again = prof_would_take_again
            changes_made = True
        if prof_difficulty is not None:
            professor_object.rate_my_professor_difficulty = prof_difficulty
            changes_made = True

        if changes_made:
            professor_object.save()

    except ProfessorProfile.DoesNotExist:
        logging.error(
            f"ProfessorProfile with id {professor_id} does not exist."
        )  # For debugging purposes

    except Exception as e:
        logging.error(
            f"An error occurred while updating RMP data: {str(e)}"
        )  # For debugging purposes
