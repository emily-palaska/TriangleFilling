# Function that performs linear interpolation between two vectors
# Warninig: It is assumed that the target point p belongs in the given line segment (p1p2)
#
# Input:
#    p1: coordinates of vector V1
#    p2: coordinates of vector V2
#    V1: vector value of V1
#    V2: vector value of V2
#    coord: the target coordinate of p (based on dim)
#    dim: defines which coordinate of p is given (x->1, y->2)
#
# Output:
#    V: the result of the interpolation (vector value) at point p

def vector_interp(p1, p2, V1, V2, coord, dim):
    # Handle exception: vertical or horizontal line with invalid arguments
    if (p1[0] == p2[0] and dim == 1) or (p1[1] == p2[1] and dim == 2) :
        return None
            
    # Find cooordinates of p
    p = [0, 0]
    if dim == 1:
        p[0] = coord
        p[1] = p1[1] + (p[0] - p1[0])*(p2[1] - p1[1])/(p2[0] - p1[0])
    elif dim == 2:
        p[1] = coord
        p[0] = p1[0] + (p[1] - p1[1])*(p2[0] - p1[0])/(p2[1] - p1[1])
    else:
        raise ValueError("Invalid dimension. dim should be 1 or 2.")
    
    # Calculate the distance between p1 and p along the line
    dist_p1_p = ((p[0] - p1[0])**2 + (p[1] - p1[1])**2)**0.5
    # Calculate the distance between p1 and p2
    dist_p1_p2 = ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)**0.5

    # Calculate the interpolation parameter t
    t = dist_p1_p / dist_p1_p2

    # Interpolate the value based on the specified dimension
    V = (1 - t) * V1 + t * V2
    print(f'Interpolation parameter: {t}')
    return V

# Example usage:
#p1 = (0, 0)
#p2 = (10, 10)
#V1 = 0
#V2 = 100
#coord = -10
#dim = 2

#result = vector_interp(p1, p2, V1, V2, coord, dim)
#print("Interpolated value:", result)
