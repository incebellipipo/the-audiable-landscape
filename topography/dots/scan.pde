class Scan {

  float[] data = new float[DEPTH_SIZE];

  float vertical_pose = 0;

  float brightness;

  float birth_time;

  boolean inverse_colors;

  Scan() {
    birth_time = millis();
    brightness = 255;
  }

  void display() {

    float step = width / float(DEPTH_SIZE);

    float max_data = max(data);

    float min_data = min(data);

    float n_points = 80;

    float s = DEPTH_SIZE / n_points;

    float sum = 0;

    int j = 0;

    for (int i = 1; i < DEPTH_SIZE; i++) {
      sum += (data[i]);

      if (i % int(s) == 0) {
        float thing = map(sum / s, 0.35, 0.685, 360, 0);
        
        if (inverse_colors) {
          // thing = 360 - thing;
          fill(thing, 100, 100, brightness);
        } else {
          fill(thing / 360 * 255, brightness);
        }

        square(width - j * (width / n_points), height -  (vertical_pose / RES_HEIGHT) * height, 15);

        j += 1;
        sum = 0;
      }
    }

    brightness = brightness - 2;
  }

  void age() {
    
  }
}
