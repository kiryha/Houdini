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

// Space Colonisation
// Custom data type "node"
struct node{
    vector p;
    int n;
    int branch = 0;
    float width = 1;
    float u;
    float v;
    matrix3 xform;
}

// Create and return "node" from point number
node create_node(int point_number){
    node item;

    item.n = point_number;
    item.p = point(0, 'P', point_number);
    item.width = point(0, 'width', point_number);
    item.xform = vertex(0, 'trs_matrix', pointvertex(0, point_number));

    return item;
}
