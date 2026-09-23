// Puck — Desk Goblin (ACT Engine)
// Parametric enclosure for snap-in assembly
// JLC3DP MJF Nylon, green dye

// Parameters
engine = "ACT";
product = "Puck";
character = "goblin";
colour = "green";

// Electronics dimensions (fixed)
esp32_width = 25.8;
esp32_length = 50.8;
esp32_height = 3.6;
oled_width = 27.3;
oled_length = 27.8;
oled_height = 4;
encoder_diameter = 7;
buzzer_diameter = 12;

// Enclosure dimensions (within constraints)
width = 80;
length = 65;
height = 45;
wall = 2.0;

// Snap-fit rails
rail_depth = 2;
rail_lip = 1;

// USB-C port
usbc_width = 8.94;
usbc_height = 3.2;

// Character features
goblin_ear_height = 15;
goblin_ear_width = 10;
goblin_eye_diameter = 12;

// Main body
module goblin_body() {
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
        
        // OLED window (front)
        translate([width/2-oled_width/2, -1, height/2-oled_length/2])
            cube([oled_width, wall+2, oled_length]);
        
        // Encoder knob (top)
        translate([width/2, length/2, height-wall-1])
            cylinder(d=encoder_diameter, h=wall+2);
        
        // Buzzer hole (back)
        translate([width/2, length+1, height/2])
            rotate([90, 0, 0])
                cylinder(d=buzzer_diameter, h=wall+2);
        
        // Goblin ears
        translate([width/4, length/3, height-wall-1])
            cylinder(d=goblin_ear_width, h=goblin_ear_height);
        translate([3*width/4, length/3, height-wall-1])
            cylinder(d=goblin_ear_width, h=goblin_ear_height);
        
        // Goblin eyes
        translate([width/3, -1, height/2])
            rotate([90, 0, 0])
                cylinder(d=goblin_eye_diameter, h=wall+2);
        translate([2*width/3, -1, height/2])
            rotate([90, 0, 0])
                cylinder(d=goblin_eye_diameter, h=wall+2);
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
module goblin_lid() {
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
module puck() {
    // Bottom half
    goblin_body();
    snap_rails();
    
    // Lid (offset for visualization)
    translate([0, 0, height+5])
        goblin_lid();
}

// Generate STL
puck();
