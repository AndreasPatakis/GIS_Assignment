def get_points(df, mmsi):
    '''Returns all the points of a specific vestel.'''
    return df[df['mmsi'] == mmsi]