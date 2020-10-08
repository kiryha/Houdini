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

// VEX Hash Table implementation for {string:float} pairs
struct hash_table{
    int array_len;  // Limit array size
    float data[];  // Init data

    int build_index(string key){
        // Build and return index for array from string
        int index = random_shash(key) % this.array_len*10;

        return index;
    }

    void add_item(string key; float value){
        // Place item value in array at index position
        int index = this -> build_index(key);
        this.data[index] = value;
    }

    float get_item(string key){
        // Get item from array by position
        int index = this -> build_index(key);
        float value = this.data[index];

        return value;
    }
}

