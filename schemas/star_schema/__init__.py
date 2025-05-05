from .dim_cuisine import DimCuisine
from .dim_demographic import DimDemographic
from .dim_location import DimLocation
from .dim_restaurant import DimRestaurant
from .fact_feature import FactFeature
from .fact_prediction import FactPrediction
from .fact_recommendation import FactRecommendation

__all__ = [
    'DimCuisine',
    'DimDemographic',
    'DimLocation',
    'DimRestaurant',
    'FactFeature',
    'FactPrediction',
    'FactRecommendation',
]

# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')