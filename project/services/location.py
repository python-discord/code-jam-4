import pandas as pd
from Levenshtein import distance


df = pd.read_csv('data/world-cities.csv')


def get_similar_location(city: str, threshold: int = 2) -> str:
    """Returns an similar location to the given location.

    :param city: A city as a string.
    :param threshold: The number of characters which can miss match
    :returns A similar location or if no similar location (regarding the
             threshold) has been found then the given location
    """
    df['distance'] = df.apply(func=lambda row: distance(city, row['name']),
                              axis=1)

    df.sort_values(by=['distance'], inplace=True)
    max_distance = df['distance'].min() + threshold
    nearest_locations = df[df['distance'] <= max_distance]

    if nearest_locations.shape[0] == 0:
        return city

    result = nearest_locations.sample(1).to_dict('records')[0]
    output = "{name}, {country}".format(**result)
    return output
