class Scan {

  float[] data = new float[DEPTH_SIZE];
  
  float vertical_pose = 0;

  void display() {
    float step = width / float(DEPTH_SIZE);
    
    float max_data = max(data);
    
    float n_points = 100;
  
    float s = DEPTH_SIZE / n_points;
    
    float sum = 0;
    
    int j = 0;
    for (int i = 0; i < DEPTH_SIZE ; i++) {
      sum += (max_data - data[i]);
      
      if(i % int(s) == 0) {
        j += 1;
        ellipse(j * (width / n_points), height / 2 + vertical_pose, sum, sum);
        sum = 0;
      }  
      
      
    }
  }
  
  void push_up() {
     vertical_pose += 15; 
  }
}
