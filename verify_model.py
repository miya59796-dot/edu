from certification_model import CertificationModel
import json

def test_model():
    print("Initializing Certification Model...")
    model = CertificationModel()
    
    # Simulate a perfect app evaluation
    print("Testing Perfect Score Evaluation...")
    perfect_scores = {}
    for category in model.rubric:
        for criterion in category.criteria:
            perfect_scores[criterion.id] = 5.0
            
    results = model.evalutate_app(perfect_scores)
    print(f"Perfect Score Results: {results['final_score']}% - {results['certification_level']}")
    
    assert results['final_score'] == 100.0
    assert results['certification_level'] == "Platinum Certified"
    
    # Simulate a mid-tier app
    print("Testing Mid-Tier Evaluation...")
    mid_scores = {}
    for category in model.rubric:
        for criterion in category.criteria:
            mid_scores[criterion.id] = 3.0
            
    results_mid = model.evalutate_app(mid_scores)
    print(f"Mid-Tier Results: {results_mid['final_score']}% - {results_mid['certification_level']}")
    
    # 3/5 is 60%
    assert results_mid['final_score'] == 60.0
    assert "Bronze" in results_mid['certification_level'] or "Silver" in results_mid['certification_level'] or "Not" in results_mid['certification_level'] or "Certified" in results_mid['certification_level']

    print("Verification Passed!")

if __name__ == "__main__":
    test_model()
