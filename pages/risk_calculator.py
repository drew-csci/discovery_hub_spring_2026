"""
Simple risk calculator for company evaluation
"""


def calculate_risk(company_profile):
    """
    Calculate risk level based on company profile.
    Returns: 'Low', 'Medium', or 'High'
    """
    risk_score = 0
    
    # Patent count scoring
    if company_profile.patent_count >= 10:
        risk_score -= 2  # Reduces risk
    elif company_profile.patent_count >= 5:
        risk_score -= 1
    else:
        risk_score += 1  # Increases risk
    
    # Stage scoring
    if company_profile.stage == 'experienced':
        risk_score -= 1  # Reduces risk
    else:
        risk_score += 1  # Increases risk (new companies are riskier)
    
    # Description completeness
    if len(company_profile.description) > 100:
        risk_score -= 1  # Reduces risk
    else:
        risk_score += 1  # Increases risk
    
    # Determine risk level
    if risk_score <= -2:
        return 'Low'
    elif risk_score >= 1:
        return 'High'
    else:
        return 'Medium'
