PImage img, scaledImg;
ArrayList<Integer> keysPressed;
int boxHeight, boxWidth;
float ratio = 0.45;
int note = 0;
String[] noteNames = {"eighth", "quarter", "half", "whole"};
int[] noteColors = {#ff0000, #00ff00, #0000ff, #ff00ff};
ArrayList<Box> boxes;
float scaleFactor;
String imgName;
Box lastBox = null;

void setup() {
  selectInput("Pick an image of some sheet music!", "fileSelected");
  keysPressed = new ArrayList<Integer>();
  boxHeight = 100;
  boxWidth = int(boxHeight * ratio);
  rectMode(CENTER);
  textAlign(CENTER, BOTTOM);
  noFill();
  boxes = new ArrayList<Box>();
  cursor(CROSS);
}

void fileSelected(File selection) {
  if (selection == null) {
    println("Window was closed or the user hit cancel.");
  } else {
    float desiredHeight = displayHeight * 0.9;
    img = loadImage(selection.getAbsolutePath());
    scaleFactor = img.height / desiredHeight;
    scaledImg = img.copy();
    scaledImg.resize(int(img.width/scaleFactor), int(img.height/scaleFactor));
    surface.setSize(int(img.width / scaleFactor), int(img.height/scaleFactor));
    imgName = selection.getName().replace(".", "");
    println(imgName);
  }
}

void updateBox() {
  int delta = keysPressed.contains(SHIFT) ? 10 : 1;
  if (keysPressed.contains(73)) {
    boxHeight += delta;
  } else if (keysPressed.contains(75)) {
    boxHeight -= delta;
  }
  boxWidth = int(boxHeight * ratio);
  stroke(noteColors[note]);
  noFill();
  rect(mouseX, mouseY, boxWidth, boxHeight);
  fill(noteColors[note]);
  text(noteNames[note], mouseX, mouseY-boxHeight/2);
}

void nudgeBox() {
  float speed = 0.25;
  if (lastBox == null) return;
  if (keysPressed.contains(UP)) {
    lastBox.center.y -= speed;
  } else if (keysPressed.contains(DOWN)) {
    lastBox.center.y += speed;
  }
  if (keysPressed.contains(LEFT)) {
    lastBox.center.x -= speed;
  } else if (keysPressed.contains(RIGHT)) {
    lastBox.center.x += speed;
  }
}

void draw() {
  if (img == null || scaledImg == null) return;
  image(scaledImg, 0, 0);
  updateBox();
  nudgeBox();
  for (Box b : boxes) {
    b.display();
  }
}

void mousePressed() {
  ArrayList<Box> deadBoxes = new ArrayList<Box>();
  for (Box b : boxes) {
    if (b.pointInside(mouseX, mouseY)) {
      deadBoxes.add(b);
    }
  }
  for (Box b : deadBoxes) {
    boxes.remove(b);
  }
  if (deadBoxes.size() == 0) {
    lastBox = new Box(mouseX, mouseY);
    boxes.add(lastBox);
  }
}

void saveNoteImages() {
  for (int i = 0; i < boxes.size(); i++) {
    Box b = boxes.get(i);
    PImage noteImage = b.getNoteImage();
    String directory = "training_notes/" + b.getNoteLabel() + "/";
    noteImage.save(directory + imgName + "_" + b.getNoteLabel() + i + ".png");
  }
}

void keyPressed() {
  if (!keysPressed.contains(keyCode)) keysPressed.add(keyCode);
  if (keyCode == ENTER) {
    saveNoteImages();
  }
  switch(key) {
  case 'e':
    note = 0;
    break;
  case 'q':
    note = 1;
    break;
  case 'h':
  case 'r':
    note = 2;
    break;
  case 'w':
    note = 3;
    break;
  case 'n':
    lastBox = new Box(lastBox.center.x + 10, lastBox.center.y + 10);
    boxes.add(lastBox);
    break;
  }
}

void keyReleased() {
  if (keysPressed.contains(keyCode))
    keysPressed.remove(Integer.valueOf(keyCode));
}
