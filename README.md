DATAPLOTTER
=======

About
-----------
Dataplotter is a web application built with Python and HTML/CSS to analyze and plot the data that comes from an Instron tensile machine. It takes a .csv file (or multiple .csv files) with three columns: time in seconds, extension in mm, and load in N. It also takes area and thickness of the sample. It returns a plot of stress (MPa) vs. strain, Young's modulus (which both appears as the red line tangent to the graph at the origin and as a number under the plot), and the standard deviation of Young's modulus across the files -- if you uploaded multiple files. Otherwise, the standard deviation would be zero, because, well, you only uploaded one file. If you uploaded multiple files, each individual plot is gray while the plot of the average stress vs. strain is given in black. You can also choose to download a .png of the plot.

How to Use
-----------
Instructions are also on the homepage, which you visit when first navigating to the page through flask run (and, subsequently, if you click on the big "Dataplotter" heading on the top left anytime you navigate off the homepage). They're also included below.

1. Download the files.
2. You should make sure the path to the uploads folder is '/home/ubuntu/project/implementation/uploads', otherwise the tool won't work. 
3. Type `flask run` into your terminal.
4. Click on the link provided. You will land on the Dataplotter homepage.
5. To analyze data, click on Upload File, the only other option in the navigation bar. This brings you to a page where you can choose files to upload.
6. You can choose to upload one file or multiple, but if you don't submit any file you'll get an error message with the grumpy cat. So, select a file to upload! I included some formatted files already in the submission. They're under the `data` folder. I got these files from running Instron tests on samples of 4 different types of elastomer films in my research, and each type is marked as class1, class2, class3, or class4. You'd upload all the files in, say, class1 together. Or you can choose to upload 1 file in class1. 
7. Moving on, after you decide what to upload, you select them (you can select multiple files using shift + click) and hit "open". Once uploaded, there should be an indication in the text box on the Upload Files page that you've uploaded the files.
8. Enter the area and the thickness. The area is the area of the sample that is stressed when tested, and the thickness is the width of the sample. For area, I typically use 3.81E-7 (because that happens to be the area of the samples I test), and for thickness I typically use 0.01 (because that happens to be the thickness of the samples I test). Make sure to not put units, though, just the number, or else you'll get an internal server error. But for reference, for the tool to return accurate results, area must be in m^2 and thickness must be in m.
9. Hit "submit" for results!
10. Hitting submit directs you to the results page, which first provides a chart. Under that is Young's modulus as well as the standard deviation across the files. As I explained earlier, if you uploaded only 1 file, the standard deviation would be zero because a file's standard deviation with itself is zero.
11. Under all that information is a "click `here` to download the image", so click on that button if you want to do that. The chart should download onto your computer as a .png.

Possible Questions
-----------
Q: Why can't I upload non .csv files?

A: The software from the Instron machine happens to return .csv files, so that's what we're sticking with.

Q: What if I don't use the .csv files provided?

A: If you have your own Instron data, or if you want to make your own data to verify Dataplotter's effectiveness, you can still run it. Just make sure the files are in the exact three-column format you see in the .csv files I provided, or else it won't go through the software properly. I provided the files for ease of use, but you don't _have_ to use them.

Q: Ah! I don't see anything!

A: Probably because the graph isn't within the xlim and ylim set. But with the sample pieces of data I provided, they should be. Usually the samples would have area of 3.81E-7 m^2 and thickness/width 0.01 m, so the dimensions I set would check out.