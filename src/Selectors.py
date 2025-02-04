import random
import math

"""
    1: Linear Random Selector
"""
def linear(elements: list):
    if not elements:
        raise ValueError("The list is empty")
    return random.choice(elements)


"""
    2:  Logarithmic Weighted Random Selector
"""
def lwrs(elements: list):
    """
        Logarithmic Weighted Random Selector:

        Gets a list of elements, and using a logarithmic scale,
        selects randomly one member of the list giving a higher
        probability weight to the initial elements of the list.

        This algorithm has to select with more frecuency
        the initial members of the list, based on the
        logarithmic/exponential curve form.

        Parameters:
            - elements [list or iter]: List of elements in order of importance.
        Returns:
            - Random element selected from the input list.
    """

    #* Amount of elements: "n":
    n = len(elements)

    #* Validation cases:
    if not hasattr(elements, "__iter__"):
        raise TypeError(f"\"elements\" has to be a list or iterable, but given {type(elements)}")
    if n == 0:
        raise ValueError("\"elements\" is empty list. List")
    if n == 1:
        return elements[0]
    
    #* Throws a random float number based on the n elements:
    #? To operate the numbers, it will consider 1 as the
    #? first element; then when it selects an index of the
    #? list, it will take at 0-starting notation:
    #/ Random float between 1 and n with 4 decimals.
    #* This random represent a random point of selection
    #* in a linear axis in which all elements has the same
    #* space to be selected:
    randomLinearPoint = round(random.uniform(0, n), 4)
    # print(f"\nLineal: {randomLinearPoint}; ", end="")

    """
    This is the propuse:

        * Having a linear scale between 1 - n, all the spaces
          between elements has the same size.
        
        * Having a logarithmic scale between 1 - n, the spaces
          between elements are different; the first element has
          the biggest space, the second is smaller, etc. The
          differences between the spaces is based on logarithms.

        * When the random is selected, you get the linear scale
          element; then it has to ponderate the space with the
          logarithmic scale, to select the equivalent.

        Example:
        NOTE: E1, E2, ..., E6 are the 6 elements of the list.

        LINEAR SCALE:
            E1      E2      E3      E4      E5      E6
        0       1       2       3       4       5       6
        |-------|-------|-------|-------|-------|-------|

        RANDOM POINT:
                                  *

        LOGARITHMIC SCALE:
                E1             E2        E3    E4   E5 E6
        0                1           2       3    4   5 6
        |----------------|-----------|-------|----|---|-|

        SELECTION:

            * Linear: 3.24: [E4];
            * Logarithmic: 3: [E2];
    
    """

    #?// If the random is 1; it takes at defect the first element:
    # if randomLinearPoint == 1:
    #     return 0

    #? The formula to calculate the distance between the start of
    #? the scale, and a randomLinear point, is:
    #/ logPoint = n*log_n+1(linearPoint);
    #/ The linearPoint has to be >= 2; and <= n+1:
    #* So, it starts a loop to check if the random linear point is
    #* between the space of the first log point, or the second, or
    #* the third, etc.
    for i in range(2, (n+1)+1):
        # print((n+1) * math.log(i, n+1), end=" ")
        if randomLinearPoint <= (n * math.log(i, n+1)):
            #! Returns the selected object:
            # print(f"Logarithmic point: {i-1};")
            return elements[(i-1)-1]


"""
    3: Complexity Weighted Random Selector

"""
def cwrs(elements: list, complexity: float):
    """
    Select one element from the list "elements" based on a bias determined by the complexity value
    The weight is given by a power law decay:
        - w(i) = 1 / (i+1)^s
    where:
        - s = s_max * (1 - complexity/100)
        - s_max = (n / (n*(complexity/100))) * ((complexity/100)+1)
        - complexity is between 0 and 100
    
    For complexity=0, s = n (maximum steepness) and the first element is nearly always selected
    For complexity=1, s = 0 and all elements have weight 1 (uniform selection)
    """
    n = len(elements)
    if complexity < 0 and complexity > 1:
        raise ValueError("\"complexity\" must be between 0 and 100")

    if complexity == 0:
        s_max = n
    else:
        s_max = (n / (n*(complexity/100))) * ((complexity/100)+1)
    
    s = s_max * (1 - complexity / 100.0)
    
    # Compute weights for each element using the power law:
    weights = [1 / ((i + 1) ** s) for i in range(n)]
    
    # Normalize the weights to get a probability distribution:
    total = sum(weights)
    probabilities = [w / total for w in weights]
    
    return random.choices(elements, weights=probabilities, k=1)[0]