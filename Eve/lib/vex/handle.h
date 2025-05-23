/*
Create a handle shape poly line
*/

float height = chf("height"); 
float width = chf("width");   
float radius = chf("radius"); 
int steps = chi("steps"); 

// Clamp so the corners can still fit
radius = clamp(radius, 0.001, min(height, width*0.5));

// Inside straight lengths adjusted 
float depth  = height - radius; 
float length = width - 2*radius; 
depth  = max(depth, 0);
length = max(length, 0);

// Build points (same logic as before)
function int addPos(vector P){ 
    return addpoint(0, P); 
}

int pts[];
append(pts, addPos(set(0, 0, 0)));
append(pts, addPos(set(0, depth, 0)));

for(int i=1;i<steps;i++){
    float u=float(i)/steps;
    float ang=radians(180-90*u);
    append(pts, addPos(set(radius*cos(ang)+radius, depth+radius*sin(ang),0)));
}

append(pts, addPos(set(radius, depth+radius, 0)));
append(pts, addPos(set(radius+length, depth+radius, 0)));

for(int i=1;i<steps;i++){
    float u=float(i)/steps;
    float ang=radians(90-90*u);
    append(pts, addPos(set(radius+length+radius*cos(ang), depth+radius*sin(ang),0)));
}

append(pts, addPos(set(width, depth, 0)));  
append(pts, addPos(set(width, 0, 0)));

int prim = addprim(0,"polyline");
foreach(int id; pts){
    addvertex(0, prim, id);
}

