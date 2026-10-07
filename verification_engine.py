from skill_verifier import create_verification_plan
from skill_evaluator import evaluate_skill, generate_follow_up


MAX_QUESTIONS = 5

class VerificationEngine:

    def __init__(self, job_description, resume_text):

        self.job_description = job_description
        self.resume_text = resume_text

        self.plan = create_verification_plan(
            job_description,
            resume_text
        )

        self.questions_asked = 0
        self.results = []
        self.current_skill = None
        self.follow_up_used = False
        
    def can_ask_question(self):
        return self.questions_asked < MAX_QUESTIONS

    def record_question(self):
        if not self.can_ask_question():
            raise RuntimeError(
                "Maximum interview question limit reached."
            )

        self.questions_asked += 1
    
    def evaluate_answer(
        self,
        skill,
        resume_claim,
        question,
        answer
    ):

        evaluation = evaluate_skill(
            skill=skill,
            resume_claim=resume_claim,
            question=question,
            candidate_answer=answer
        )

        return evaluation

    def get_follow_up(
        self,
        skill,
        resume_claim,
        question,
        answer,
        evidence
    ):

        if not self.can_ask_question():
            return None

        return generate_follow_up(
            skill=skill,
            resume_claim=resume_claim,
            original_question=question,
            candidate_answer=answer,
            evidence=evidence)
            
    def get_next_skill(self):

        for skill in self.plan.skills:

            already_evaluated = any(
                result["skill"] == skill.name
                for result in self.results
            )

            if not already_evaluated:
                return skill

        return None
        
    def process_answer(
    self,
    skill,
    question,
    answer):

        evaluation = self.evaluate_answer(
            skill=skill.name,
            resume_claim=skill.resume_claim,
            question=question,
            answer=answer
        )

        self.results.append({
            "skill": skill.name,
            "confidence": evaluation.confidence,
            "status": evaluation.status,
            "evidence": evaluation.evidence
        })

        return evaluation
    
    def get_next_question(self):

        # If we are already working on a skill,
        # continue with that skill's follow-up.
        if self.current_skill is not None:
            return self.current_skill

        # Otherwise select the next unverified skill.
        skill = self.get_next_skill()

        if skill is None:
            return None

        self.current_skill = skill
        self.follow_up_used = False

        return skill
    
    def decide_next_step(self, evaluation):

        # Strong evidence → skill is verified
        if evaluation.status == "verified":
            self.current_skill = None
            self.follow_up_used = False
            return "next_skill"

        # Weak/partial evidence → try one follow-up
        if (
            evaluation.status in ["partial", "unverified"]
            and not self.follow_up_used
            and self.can_ask_question()
        ):
            self.follow_up_used = True
            return "follow_up"

        # No follow-up available → finish this skill
        self.current_skill = None
        self.follow_up_used = False

        return "next_skill"
            

    
    
if __name__ == "__main__":

    engine = VerificationEngine(
        job_description="Backend Developer with Python and FastAPI",
        resume_text="Experienced Python developer who built FastAPI APIs."
    )

    print("\nTesting question limit:\n")

    for i in range(6):

        if engine.can_ask_question():

            engine.record_question()

            print(
                f"Question {engine.questions_asked}: "
                f"Allowed ✅"
            )

        else:

            print(
                f"Question {i + 1}: "
                f"BLOCKED ❌ — Maximum of 5 questions reached."
            )