/*
Create sphere
Equator is latitude (horizontal)
*/

int h_resolution = 12;
int v_resolution = 6;
int points[];


function vector get_cartesian_position(float h_angle, v_angle){
    vector position;
    position.x = sin(v_angle)*cos(h_angle);
    position.y = sin(v_angle)*sin(h_angle);
    position.z = cos(v_angle);
    return position;
}

function void add_face(int points[]; int upper_left, upper_right, lower_right, lower_left){
    int prim = addprim(geoself(), "poly");
    addvertex(0, prim, points[lower_left]);
    addvertex(0, prim, points[lower_right]);
    addvertex(0, prim, points[upper_right]);
    addvertex(0, prim, points[upper_left]);

}


// Create sphere points
for (int v_index=0; v_index<=v_resolution; v_index++){
    float v_angle=v_index*(M_PI/v_resolution);

    // Handle poles
    if(v_index==0 || v_index==v_resolution){
        vector position=get_cartesian_position(0, v_angle);
        int pt = addpoint(0, position);
        append(points, pt);
    }

    // All horizontal circles
    else{
        for (int h_index=0; h_index<h_resolution; h_index++){
            float h_angle=h_index*(2* M_PI/h_resolution);
            vector position=get_cartesian_position(h_angle, v_angle);
            int pt = addpoint(0, position);
            append(points, pt);
        }
    }
}

// Create polygons based on point indices
for (int v_index = 0; v_index < v_resolution; v_index++) {
    for (int h_index = 0; h_index < h_resolution; h_index++) {
        int lower_left, lower_right, upper_left, upper_right;

        // Upper pole
        if (v_index == 0) {
            upper_left = 0;
            upper_right = upper_left;
            lower_right = h_index + 1;
            lower_left = (h_index + 1) % h_resolution + 1;
        }
        // Lower pole
        else if (v_index == v_resolution - 1) {
            int bottom_pole_index = len(points) - 1;
            upper_left = bottom_pole_index - (h_resolution - h_index);
            if(h_index==0){
                upper_right = bottom_pole_index - 1;
            }
            else{
                upper_right = upper_left - 1;
                }
            lower_left = bottom_pole_index;
            lower_right = lower_left;

        // Middle rows
        } else {
            lower_left = 1 + (v_index - 1) * h_resolution + h_index;
            lower_right = lower_left + 1;
            if (h_index == h_resolution - 1) {
                lower_right = 1 + (v_index - 1) * h_resolution;
            }
            upper_left = lower_left + h_resolution;
            upper_right = lower_right + h_resolution;
        }

        add_face(points, upper_left, upper_right, lower_right, lower_left);
    }
}
