import random
import math

import matplotlib.pyplot as plt

'''
    Logarithmic Random Poderated Selector
'''

def logselector(elements: list):

    '''
        Logarithmic Random Poderated Selector:

        This mini-algorithm gets a list of elements,
        and using a logarithmic scale, selects randomly
        one member of the list giving a higher probability
        weight to the initial elements of the list.

        This algorithm has to select with more frecuency
        the initial members of the list, based on the
        logarithmic/exponential curve form.
    '''

    #* Amount of elements: "n":
    n = len(elements)

    #* Validation cases:
    if n == 0:
        # return "List cannot be empty :c"
        return
    if n == 1:
        # return elements[0]
        return 0
    
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

    '''
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
    
    '''

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
            #! Returns the selected element:
            # return elements[i-1]
            # print(f"Log: {i-1};")
            return (i-1)-1


if __name__ == "__main__":

    #* It counts and verifies the bias on the selections,
    #* repeating the selection experiment a lot of times:
    #/ counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    n = int(input("\nNumber of elements: "))
    times = int(input("Repetitions: "))

    #? Example list of 10 elements;
    #* The algorithm has to recieve this list and select randomly one element;
    #* By repeating the selection a lot of times, the result has to be that the
    #* first element "E1" is the most frecuent selected, and then "E2", etc.
    #/ elements: list = ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10"]
    counter: list = []
    elements: list = []
    for i in range(0, n):
        counter.append(0)
        elements.append(f"E{i+1}")

    for _ in range(0, times):
        selected = logselector(elements)
        counter[selected] += 1
    
    print("\nSelected times:")
    for i in range(0, len(elements)):
        print(f"Element {i+1}: {counter[i]}")
    

    # Draws the line in a graph:
    plt.rcParams["figure.figsize"] = [10, 5]
    plt.rcParams["figure.autolayout"] = True
    
    # Points with:
    # (element, amountOfSelections ):
    # points: list = []
    x_values: list = []
    y_values: list = []

    # Put all the points:
    for i in range(0, len(elements)):
        # points.append([i+1, counter[i]])
        x_values.append(i+1)
        y_values.append(counter[i])
    
    # Shows the graphic:
    plt.title("LOGARITHMIC RANDOM PONDERATED SELECTOR")
    plt.ylabel("Amount of selected times")
    plt.xlabel("Number of element")
    info = f"For {n} elements;\nWith {times} choices;"
    plt.annotate(info,
    xy=(0.96, 0.8), xytext=(0, 12),
    xycoords=("axes fraction", "figure fraction"),
    textcoords="offset points",
    size=10, ha="right", va="top",
    bbox=dict(boxstyle="square,pad=1.0", fc="white", ec="b", lw=2))

    plt.plot(x_values, y_values, "bo", linestyle="-")
    plt.savefig("logselection.png", dpi="figure")
    plt.show()
    print()