# Single Line Image Drawing

The traditional technique of drawing single line images required use of machine hardware or experiences artists. We present a software-based solution to this prob- lem by making use of concepts like Voronoi Diagrams, B ́ezier curves, stippling. An iterative technique acts on input images directly to produce high-quality single line drawings after stippling the input.

Our project: **Single Line Image Drawing** employs simple concepts such as Voronoi Diagrams and Stippling to generate single line image drawings of given input.

## Workflow
![Project Workflow](https://github.com/mnk343/Single-Line-Portrait-Drawing/blob/master/Interesting%20Results/Project_Workflow.png?raw=true)

The workflow of the project is as follows and can be found in various different files of the project:

- **Stippling**
    - Used implementations as discussed in the paper [Weighted Voronoi Stippling](https://www.cs.ubc.ca/labs/imager/tr/2002/secord2002b/secord.2002b.pdf) by Adrian Secord.
    - Used multi-source BFS to generate voronoi diagrams.
 - **Single Line Drawing by Straight Lines**
    -Iterated over all points and connected them to a randomly chosen point in the top 5 nearest point and simply use inbuilt OpenGL library function or simply add numerous points in between those two points using a straight line equation
  - **Single Line Drawing by Bezier Curves**
    - Iterated over points in batches of 4 and connected them using Bezier curves. This gives a better feeling of a smooth hand drawing as compared to connecting using straight lines.
    - 
## Installation
Install the dependencies.
```sh
$ pip install numpy
$ pip install Pillow
```
## Usage
##### Stipple an image:
```sh
$  cd stippling
$ python3 stippling.py
Correct file input path & number of stipples desired is given as input.
```
The stippling program generates a pickle file **generating_points** containing the centroids of the voronoi diagram of the final output. We store its path and use it in the next section.
##### Generate single hand drawing:
```sh
$  cd  generate_single_hand_drawing
$ python3 curve.py generating_points
```
This program upon execution generates the required output files.

#### Results
Below are the results we got upon execution of our program:
For **Stippling**:

![Portrait of a lady](https://github.com/mnk343/Single-Line-Portrait-Drawing/blob/master/Interesting%20Results/Image_4.1_Portrait_50000_Stiples/output.png?raw=true)

![Wolverine](https://github.com/mnk343/Single-Line-Portrait-Drawing/blob/master/Interesting%20Results/Image_6_Wolverine_50000_Stipples/output.png?raw=true)

For **Single Line Drawing**:

![Apple logo](https://github.com/mnk343/Single-Line-Portrait-Drawing/blob/master/Interesting%20Results/result_apple_logo.png?raw=true)

![Apple logo](https://github.com/mnk343/Single-Line-Portrait-Drawing/blob/master/Interesting%20Results/result_harry_potter.png?raw=true)
