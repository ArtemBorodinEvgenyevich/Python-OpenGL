# Python-OpenGL

This is my OpenGL sandbox where I test different features and techniques during studying modern OpenGL workflow.
The following repository contains examples using [PyOpenGL](https://pypi.org/project/PyOpenGL/) binding with
[GLFW](https://pypi.org/project/glfw/) and official [Qt for Python](https://pypi.org/project/PySide2/) framework.
Posted it due to a lack of working PyOpenGL examples on Github.

### Content
Here you can find code to draw from **"hello-triangle"** to more interesting stuff.
Most examples use Qt, not GLFW, but the concepts should be +/- the same. 

> Please note that I did not abstract OpenGL calls for you to see what is going on line by line, but for real projects it a must!

>Please note that work is still ongoing. I will try to update this repository as often as possible.

If you see any math mistakes or you would like to improve the code, feel free to
email me or open a new issue. Thanks!

* GLFW
    1. Viewport initialization
    2. Triangle draw
    3. Index drawing

* Qt for Python
    1. Viewport initialization
    2. Triangle draw
    3. 3D viewport mouse rotation

### TODO:
A list of examples to do in a recent future
- [X] GLFW
    - [X] Hello triangle
    - [X] Indexed drawing
- [ ] Qt for Python
    - [X] Hello triangle
    - [ ] Texturing 
    - [ ] Point sprites
    - [X] 3D Viewport rotation
    - [ ] 3D Viewport panning
    - [ ] 3D Viewport zooming
