/*
Create a handle shape
*/

float depth = chf("depth"); 
float length = chf("length"); 
float radius = chf("radius");
int steps = chi("steps"); 

function int addPos(vector P)
{
    return addpoint(0, P);
}

int pts[];
append(pts, addPos(set(0, 0, 0)));
append(pts, addPos(set(0, depth, 0)));

// left quarter-arc  (180° → 90°)
for (int i = 1; i < steps; i++)
{
    float u   = float(i) / steps;
    float ang = radians(180 - 90*u);
    vector pos = set(radius*cos(ang) + radius, depth + radius*sin(ang), 0);
    append(pts, addPos(pos));
}

append(pts, addPos(set(radius, depth+radius, 0)));
append(pts, addPos(set(radius+length, depth+radius, 0)));

// right quarter-arc (90° → 0°)
for (int i = 1; i < steps; i++)
{
    float u   = float(i) / steps;
    float ang = radians(90 - 90*u); 
    vector pos = set(radius+length + radius*cos(ang), depth + radius*sin(ang), 0);
    append(pts, addPos(pos));
}   

append(pts, addPos(set(radius+length+radius,  depth, 0)));
append(pts, addPos(set(radius+length+radius,  0, 0)));

// Build polygon
int prim = addprim(0, "polyline");
foreach (int id; pts)
    addvertex(0, prim, id);