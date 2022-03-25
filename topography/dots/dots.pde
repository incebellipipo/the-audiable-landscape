/**
 * oscP5message by andreas schlegel
 * example shows how to create osc messages.
 * oscP5 website at http://www.sojamo.de/oscP5
 */

/**
 * documentation: https://sojamo.de/libraries/oscP5/reference/index.html
 *
 */

import oscP5.*;

OscP5 oscP5;

int DEPTH_SIZE = 848;

boolean should_push_scan = false;

Scan current_scan;

ArrayList<Scan> scans;

void setup() {
  size(640, 360);  // Size should be the first 
  // fullScreen();
  frameRate(25);
  noStroke();


  // Setup OSC
  OscProperties properties = new OscProperties();
  // properties.setRemoteAddress("127.0.0.1", 7400);
  properties.setListeningPort(7401);
  properties.setSRSP(OscProperties.OFF);
  properties.setDatagramSize(32768);
  oscP5 = new OscP5(this, properties);

  // Setup scan
  current_scan = new Scan();
  scans = new ArrayList<Scan>();
}

void draw() {
  background(0);

  current_scan.display();

  for (int i = 0; i < scans.size(); i++) {
    scans.get(i).display();
  }
}


/* incoming osc message are forwarded to the oscEvent method. */
void oscEvent(OscMessage msg) {

  if (msg.checkAddrPattern("/depths")) {
    for (int i = 0; i < DEPTH_SIZE; i++) {
      current_scan.data[i] = msg.get(i).floatValue();
    }
  }

  if (msg.checkAddrPattern("/button")) {
    push_scan();
  }
}

void push_scan() {
  for (int i = 0; i < scans.size(); i++ ) {
    scans.get(i).push_up();
  }

  Scan n = new Scan();
  arrayCopy(current_scan.data, n.data);
  n.push_up();
  scans.add(n);

  for (int i = scans.size() - 1; i >= 0; i--) {
    Scan part = scans.get(i);
    if (part.vertical_pose > height) {
      scans.remove(i);
    }
  }
}
