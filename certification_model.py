from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class Criterion:
    id: str
    name: str
    description: str
    weight: float = 1.0

@dataclass
class Category:
    id: str
    name: str
    description: str
    criteria: List[Criterion]
    weight: float = 1.0

class CertificationModel:
    def __init__(self):
        self.rubric = self._define_rubric()

    def _define_rubric(self) -> List[Category]:
        return [
            Category(
                id="cognitive",
                name="Cognitive Development",
                description="Alignment with cognitive science principles.",
                weight=0.30,
                criteria=[
                    Criterion("cog_1", "Age Appropriateness", "Content matches the target age group's cognitive stage.", 1.2),
                    Criterion("cog_2", "Scaffolding", "Provides support that fades as competence increases.", 1.0),
                    Criterion("cog_3", "Cognitive Load", "Avoids overwhelming the user with too much information at once.", 1.0),
                    Criterion("cog_4", "Active Learning", "Promotes active engagement rather than passive consumption.", 0.8),
                ]
            ),
            Category(
                id="instructional",
                name="Instructional Design",
                description="Pedagogical soundness and teaching methodology.",
                weight=0.30,
                criteria=[
                    Criterion("inst_1", "Learning Goals", "Clear and measurable learning objectives.", 1.0),
                    Criterion("inst_2", "Feedback", "Timely, specific, and constructive feedback.", 1.2),
                    Criterion("inst_3", "Adaptability", "Adapts to the learner's pace and performance.", 1.0),
                    Criterion("inst_4", "Content Accuracy", "Information is accurate and up-to-date.", 0.8),
                ]
            ),
            Category(
                id="motivation",
                name="Motivation & Engagement",
                description="Mechanisms to sustain interest and effort.",
                weight=0.20,
                criteria=[
                    Criterion("mot_1", "Intrinsic Motivation", "Fosters curiosity and interest in the subject.", 1.2),
                    Criterion("mot_2", "Extrinsic Rewards", "Uses badges/points effectively without undermining intrinsic value.", 0.8),
                    Criterion("mot_3", "Autonomy", "Measurable user control and choice.", 1.0),
                ]
            ),
            Category(
                id="outcomes",
                name="Learning Outcomes",
                description="Evidence of learning and assessment capability.",
                weight=0.20,
                criteria=[
                    Criterion("out_1", "Assessment", "Valid assessment of learning progress.", 1.2),
                    Criterion("out_2", "Skill Transfer", "Ability to apply learning to new contexts.", 1.0),
                ]
            ),
        ]

    def evalutate_app(self, scores: Dict[str, float]) -> Dict:
        """
        Calcuates the weighted score based on input scores (1-5 scale).
        scores: Dict mapping criterion_id to score (float).
        """
        total_weighted_score = 0.0
        total_possible_weight = 0.0
        
        category_scores = {}

        for category in self.rubric:
            cat_weighted_score = 0.0
            cat_weight_sum = 0.0
            
            for criterion in category.criteria:
                score = scores.get(criterion.id, 0.0)
                # Normalize score to 0-1 range for calculation first, then scale back or keep as %
                # Let's assume input score is 1-5.
                # Contribution = (Score / 5) * Criterion Weight
                
                cat_weighted_score += (score / 5.0) * criterion.weight
                cat_weight_sum += criterion.weight
            
            # Category score in percentage (0.0 to 1.0)
            if cat_weight_sum > 0:
                cat_score_normalized = cat_weighted_score / cat_weight_sum
            else:
                cat_score_normalized = 0.0
                
            category_scores[category.name] = cat_score_normalized * 100 # stored as percentage 0-100
            
            # Add to total
            total_weighted_score += cat_score_normalized * category.weight
            total_possible_weight += category.weight

        # Final score 0-100
        if total_possible_weight > 0:
            final_percentage = (total_weighted_score / total_possible_weight) * 100
        else:
            final_percentage = 0.0

        return {
            "final_score": round(final_percentage, 2),
            "category_scores": {k: round(v, 2) for k, v in category_scores.items()},
            "certification_level": self._get_certification_level(final_percentage)
        }

    def _get_certification_level(self, percentage: float) -> str:
        if percentage >= 90:
            return "Platinum Certified"
        elif percentage >= 80:
            return "Gold Certified"
        elif percentage >= 70:
            return "Silver Certified"
        elif percentage >= 60:
            return "Bronze Certified"
        else:
            return "Not Certified"
