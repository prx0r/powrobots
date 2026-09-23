// Mosswick — Garden Frog (SENSE Engine)
// Parametric enclosure for snap-in assembly
// JLC3DP MJF Nylon, green dye

// Parameters
engine = "SENSE";
product = "Mosswick";
character = "frog";
colour = "green";

// Electronics dimensions (fixed)
esp32_width = 25.8;
esp32_length = 50.8;
esp32_height = 3.6;

sensor_diameter = 12;  // DHT22
light_window = 8;      // BH1750

// Enclosure dimensions (within constraints)
width = 70;
length = 55;
height = 40;
wall = 2.0;

// Snap-fit rails
rail_depth = 2;
rail_lip = 1;

// USB-C port
usbc_width = 8.94;
usbc_height = 3.2;

// Sensor holes
moisture_hole = 6;  // For sensor probe
led_window = 5;     // For WS2812B

// Character features
frog_eye_diameter = 8;
frog_mouth_width = 15;

// Main body
module frog_body() {
    difference() {
        // Outer shell (rounded box)
        hull() {
            translate([wall, wall, wall])
                cube([width-2*wall, length-2*wall, height-2*wall]);
        }
        
        // Inner cavity
        translate([wall+rail_lip, wall+rail_lip, wall+rail_lip])
            cube([width-2*wall-2*rail_lip, length-2*wall-2*rail_lip, height-2*wall-2*rail_lip]);
        
        // USB-C port
        translate([-1, length/2-usbc_width/2, height/2-usbc_height/2])
            cube([wall+2, usbc_width, usbc_height]);
        
        // Moisture sensor hole (bottom)
        translate([width/2, length/2, -1])
            cylinder(d=moisture_hole, h=wall+2);
        
        // LED window (front)
        translate([width/2, -1, height/3])
            cylinder(d=led_window, h=wall+2);
        
        // Light window (top)
        translate([width/2, length/2, height-wall-1])
            cylinder(d=light_window, h=wall+2);
        
        // Frog eyes
        translate([width/4, length/4, height-wall-1])
            cylinder(d=frog_eye_diameter, h=wall+2);
        translate([3*width/4, length/4, height-wall-1])
            cylinder(d=frog_eye_diameter, h=wall+2);
        
        // Frog mouth
        translate([width/2, length/4, height/2])
            rotate([90, 0, 0])
                cylinder(d=frog_mouth_width, h=wall+2);
    }
}

// Snap-fit rails
module snap_rails() {
    // Bottom rails
    translate([wall, wall, wall])
        cube([rail_depth, length-2*wall, rail_lip]);
    translate([width-wall-rail_depth, wall, wall])
        cube([rail_depth, length-2*wall, rail_lip]);
    
    // Top rails
    translate([wall, wall, height-wall-rail_lip])
        cube([rail_depth, length-2*wall, rail_lip]);
    translate([width-wall-rail_depth, wall, height-wall-rail_lip])
        cube([rail_depth, length-2*wall, rail_lip]);
}

// Lid
module frog_lid() {
    difference() {
        // Outer shell
        hull() {
            translate([wall, wall, wall])
                cube([width-2*wall, length-2*wall, wall]);
        }
        
        // Inner cavity
        translate([wall+rail_lip, wall+rail_lip, wall])
            cube([width-2*wall-2*rail_lip, length-2*wall-2*rail_lip, wall]);
    }
}

// Assembly
module mosswick() {
    // Bottom half
    frog_body();
    snap_rails();
    
    // Lid (offset for visualization)
    translate([0, 0, height+5])
        frog_lid();
}

// Generate STL
mosswick();
