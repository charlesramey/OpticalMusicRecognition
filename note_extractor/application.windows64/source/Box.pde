class Box {

  PVector center;
  PVector size;
  int label;

  Box(float x, float y) {
    center = new PVector(x, y);
    size = new PVector(boxWidth, boxHeight);
    label = note;
  }

  void display() {
    stroke(#ff0000);
    noFill();
    rect(center.x, center.y, size.x, size.y);
    fill(#ff0000);
    text(noteNames[label], center.x, center.y - size.y/2);
  }

  boolean pointInside(float x, float y) {
    return pointInside(new PVector(x, y));
  }

  boolean pointInside(PVector point) {
    return center.x - size.x/2 < point.x && center.x + size.x/2 > point.x &&
      center.y - size.y/2 < point.y && center.y + size.y/2 > point.y;
  }

  PImage getNoteImage() {
    return img.get(int(scaleFactor * (center.x - size.x/2)), int(scaleFactor * (center.y - size.y/2)), 
      int(scaleFactor * size.x), int(scaleFactor * size.y));
  }
  
  String getNoteLabel() {
    return noteNames[label];
  }
}
