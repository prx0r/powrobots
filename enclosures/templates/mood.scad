// Template: TEMPLATE_NAME
// Parametric enclosure for snap-in assembly
// JLC3DP MJF Nylon

// Parameters
engine = "ENGINE_TYPE";
product = "PRODUCT_NAME";
character = "CHARACTER_TYPE";
colour = "DEFAULT_COLOUR";

// Electronics dimensions (fixed)
esp32_width = 25.8;
esp32_length = 50.8;
esp32_height = 3.6;

// Enclosure dimensions (within constraints)
width = WIDTH;
length = LENGTH;
height = HEIGHT;
wall = 2.0;

// Snap-fit rails
rail_depth = 2;
rail_lip = 1;

// USB-C port
usbc_width = 8.94;
usbc_height = 3.2;

// Main body
module body() {
    difference() {
        hull() {
            translate([wall, wall, wall])
                cube([width-2*wall, length-2*wall, height-2*wall]);
        }
        translate([wall+rail_lip, wall+rail_lip, wall+rail_lip])
            cube([width-2*wall-2*rail_lip, length-2*wall-2*rail_lip, height-2*wall-2*rail_lip]);
        translate([-1, length/2-usbc_width/2, height/2-usbc_height/2])
            cube([wall+2, usbc_width, usbc_height]);
    }
}

// Snap-fit rails
module snap_rails() {
    translate([wall, wall, wall])
        cube([rail_depth, length-2*wall, rail_lip]);
    translate([width-wall-rail_depth, wall, wall])
        cube([rail_depth, length-2*wall, rail_lip]);
    translate([wall, wall, height-wall-rail_lip])
        cube([rail_depth, length-2*wall, rail_lip]);
    translate([width-wall-rail_depth, wall, height-wall-rail_lip])
        cube([rail_depth, length-2*wall, rail_lip]);
}

// Lid
module lid() {
    difference() {
        hull() {
            translate([wall, wall, wall])
                cube([width-2*wall, length-2*wall, wall]);
        }
        translate([wall+rail_lip, wall+rail_lip, wall])
            cube([width-2*wall-2*rail_lip, length-2*wall-2*rail_lip, wall]);
    }
}

// Assembly
module product() {
    body();
    snap_rails();
    translate([0, 0, height+5])
        lid();
}

product();
