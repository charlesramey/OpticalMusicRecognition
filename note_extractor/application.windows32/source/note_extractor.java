import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class note_extractor extends PApplet {

PImage img, scaledImg;
ArrayList<Integer> keysPressed;
int boxHeight, boxWidth;
float ratio = 0.45f;
int note = 0;
String[] noteNames = {"eighth", "quarter", "half", "whole"};
int[] noteColors = {0xffff0000, 0xff00ff00, 0xff0000ff, 0xffff00ff};
ArrayList<Box> boxes;
float scaleFactor;
String imgName;
Box lastBox = null;

public void setup() {
  selectInput("Pick an image of some sheet music!", "fileSelected");
  keysPressed = new ArrayList<Integer>();
  boxHeight = 100;
  boxWidth = PApplet.parseInt(boxHeight * ratio);
  rectMode(CENTER);
  textAlign(CENTER, BOTTOM);
  noFill();
  boxes = new ArrayList<Box>();
  cursor(CROSS);
}

public void fileSelected(File selection) {
  if (selection == null) {
    println("Window was closed or the user hit cancel.");
  } else {
    float desiredHeight = displayHeight * 0.9f;
    img = loadImage(selection.getAbsolutePath());
    scaleFactor = img.height / desiredHeight;
    scaledImg = img.copy();
    scaledImg.resize(PApplet.parseInt(img.width/scaleFactor), PApplet.parseInt(img.height/scaleFactor));
    surface.setSize(PApplet.parseInt(img.width / scaleFactor), PApplet.parseInt(img.height/scaleFactor));
    imgName = selection.getName().replace(".", "");
    println(imgName);
  }
}

public void updateBox() {
  int delta = keysPressed.contains(SHIFT) ? 10 : 1;
  if (keysPressed.contains(73)) {
    boxHeight += delta;
  } else if (keysPressed.contains(75)) {
    boxHeight -= delta;
  }
  boxWidth = PApplet.parseInt(boxHeight * ratio);
  stroke(noteColors[note]);
  noFill();
  rect(mouseX, mouseY, boxWidth, boxHeight);
  fill(noteColors[note]);
  text(noteNames[note], mouseX, mouseY-boxHeight/2);
}

public void nudgeBox() {
  if (lastBox == null) return;
  if (keysPressed.contains(UP)) {
    lastBox.center.y -= 1;
  } else if (keysPressed.contains(DOWN)) {
    lastBox.center.y += 1;
  }
  if (keysPressed.contains(LEFT)) {
    lastBox.center.x -= 1;
  } else if (keysPressed.contains(RIGHT)) {
    lastBox.center.x += 1;
  }
}

public void draw() {
  if (img == null || scaledImg == null) return;
  image(scaledImg, 0, 0);
  updateBox();
  nudgeBox();
  for (Box b : boxes) {
    b.display();
  }
}

public void mousePressed() {
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

public void saveNoteImages() {
  for (int i = 0; i < boxes.size(); i++) {
    Box b = boxes.get(i);
    PImage noteImage = b.getNoteImage();
    String directory = "training_notes/" + b.getNoteLabel() + "/";
    noteImage.save(directory + imgName + "_" + b.getNoteLabel() + i + ".png");
  }
}

public void keyPressed() {
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
  }
}

public void keyReleased() {
  if (keysPressed.contains(keyCode))
    keysPressed.remove(Integer.valueOf(keyCode));
}
class Box {

  PVector center;
  PVector size;
  int label;

  Box(float x, float y) {
    center = new PVector(x, y);
    size = new PVector(boxWidth, boxHeight);
    label = note;
  }

  public void display() {
    stroke(noteColors[label]);
    noFill();
    rect(center.x, center.y, size.x, size.y);
    fill(noteColors[label]);
    ellipse(center.x, center.y, size.x/4, size.x/4);
  }

  public boolean pointInside(float x, float y) {
    return pointInside(new PVector(x, y));
  }

  public boolean pointInside(PVector point) {
    return center.x - size.x/2 < point.x && center.x + size.x/2 > point.x &&
      center.y - size.y/2 < point.y && center.y + size.y/2 > point.y;
  }

  public PImage getNoteImage() {
    return img.get(PApplet.parseInt(scaleFactor * (center.x - size.x/2)), PApplet.parseInt(scaleFactor * (center.y - size.y/2)), 
      PApplet.parseInt(scaleFactor * size.x), PApplet.parseInt(scaleFactor * size.y));
  }
  
  public String getNoteLabel() {
    return noteNames[label];
  }
}
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "note_extractor" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
