def build_string_score(entity, length):
    """
    Generate the string that represent the score formula of string fields
    Usage:
        >>> Called by generate_query method
    Params:
        - metadata: {
            entity: string,
            query_director: integer
        }
    Return: String
    """
    
    return "*((_score))/(((1-_score/doc['providerData." + entity + ".length'].value)*doc['providerData." + entity + ".length'].value)+" + length + ")"