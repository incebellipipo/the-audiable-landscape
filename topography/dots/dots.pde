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

int RES_WIDTH = 848;
int RES_HEIGHT = 480;

boolean should_push_scan = false;
long scan_time;
boolean inverse_colors;
Scan current_scan;

ArrayList<Scan> scans;

void setup() {
  fullScreen(2);
  frameRate(60);
  noStroke();
  colorMode(HSB, 360, 100, 100);
  
  inverse_colors = true;

  // Setup scan
  scans = new ArrayList<Scan>();

  // Setup OSC
  OscProperties properties = new OscProperties();
  // properties.setRemoteAddress("127.0.0.1", 7400);
  properties.setListeningPort(7401);
  properties.setSRSP(OscProperties.OFF);
  properties.setDatagramSize(32768);
  oscP5 = new OscP5(this, properties);
}

void draw() {
  background(0);

  for (int i = 0; i < scans.size(); i++) {
    scans.get(i).display();
  }

  for (int i = scans.size() - 1; i >= 0; i--) {
    Scan part = scans.get(i);
    if (part.birth_time > millis() + 1000) {
      scans.remove(i);
    }

    if (part.brightness < 0) {
      scans.remove(i);
    }
  }
}


/* incoming osc message are forwarded to the oscEvent method. */
void oscEvent(OscMessage msg) {

  if (msg.checkAddrPattern("/vertical_depths")) {

    //if (millis() - scan_time < 5000) {
      Scan s = new Scan();
      s.vertical_pose = msg.get(0).floatValue();
      s.inverse_colors = inverse_colors;

      for (int i = 0; i < DEPTH_SIZE; i++) {
        s.data[i] = msg.get(i+1).floatValue();
      }

      scans.add(s);
    //}
  }

  if (msg.checkAddrPattern("/button")) {
    inverse_colors = ! inverse_colors;
    scan_time = millis();
  }
}
