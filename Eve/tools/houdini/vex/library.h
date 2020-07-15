void hello(){
    printf('Hello, Eve!\n');
}

// Create array from point positions (Detail mode)
function vector[] get_point_positions(){
    vector points[];
    for(int i=0; i<npoints(0); i++){
        vector point_position = point(0, 'P', i);
        append(points, point_position);
    }
    return points;
}

// Custom data type for space colonisation: {vector, int, int}
struct node{
    vector p;
    int n;
    int branch = 0;
    float width = 1;
}