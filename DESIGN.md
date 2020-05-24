ABOUT
=======
Dataplotter is a web application built with Python and HTML/CSS to analyze and plot the data that comes from an Instron tensile machine. It takes a .csv file (or multiple .csv files) with three columns: time in seconds, extension in mm, and load in N. It returns a plot of stress (MPa) vs. strain, Young's modulus (which both appears as the red line tangent to the graph at the origin and as a number under the plot), and the standard deviation of Young's modulus across the files -- if you uploaded multiple files. Otherwise, the standard deviation would be zero, because, well, you only uploaded one file. If you uploaded multiple files, each individual plot is gray while the plot of the average stress vs. strain is given in black. You can also choose to download a .png of the plot.

THE CODE
=======

randid()
-----------
This function randomly selects 8 letters from the string I gave it (qwertyuiopasdfghjklzxcvbnm) for the purpose of forming the name of the .png file (I'll call it later in index()). The chances of two randomly-generated names being the same would be low, meaning that if two users run the application at once, there's a low chance of them saving two sets of data to the same .png (since plt.savefig from matplotlib only adds data to the file with the given name every iteration).

Extract(filename)
-----------
This function extracts the necessary data for running the analysis. Because the .csv files passed in have time, extension, and load, I pretty much had the function open the file and strip the quotation marks from each line, because the .csv file from the Instron came with those. Then I appended each part of the data to their respective lists, which would become important when I called it later. The reason why I divided every entry in the extensions column by 1000 was because the Instron gave extension in mm, and for SI unit purposes, I needed to convert the extension to meters. The try/except is for lines that don't have data (like the headers), in which case the program would just continue reading.

Plot_Process()
-----------
Calls the extract function to extract the time, extension, and load, then converts them each to NumPy arrays. The first part of this function is converting the extension and force into strain and stress, respectively, using global constants declared some lines above. The rest is pretty straightforward: we set up the graph and plot the data points using matplotlib functions.

download(filename)
-----------
To download the file. I chose to use `send_from_directory` instead of `send_file` to avoid security attacks -- like the user accessing other code in the implementation folder and changing things up. `send_from_directory` would guarantee that the file comes from the directory listed. As for the previous step, I make the path to the uploads folder absolute by joining `current_app.root_path` using `os.path.join`, in case for some reason I end up changing the folder `application.py` is in (in which case a relative path to uploads would no longer work, and would require lots of time spent debugging).

info()
-----------
Just a function that calls the `info.html` template to display the instructions for the tool.

index()
-----------
I open with `plt.clf()`, in case there are any plots originally existing. If the request method is GET, the template `index.html` appears, which has the simple upload file form. If the user doesn't upload anything, I give them an error, because you have to upload a file for Dataplotter to work! Then I generate a random name for the file and save it to the uploads folder, which will be important later on. Then I made lists for stress, Young's modulus, and strain, which would be a convenient way to store the analyzed data. Then I called Plot_Process to plot the data. I plotted the average curve in black for clarity. Finally, I called `plt.savefig()` to save the .png.

apology(), errorhandler(e)
-----------
These were functions I kept from CS50 Finance because they conveniently displayed error messages when something went wrong, and I thought the grumpy cat was cute.

THE OTHER THINGS IN THE FOLDER
=======

data
-----------
These are data samples I collected from the Instron for 4 different elastomer films for the TFs' convenience when testing Dataplotter. You don't have to use these, however, if you have a file with the same format. `class1`, `class2`, `class3`, and `class4` all refer to different materials, and each .csv in those folders is the data for one sample.

static
-----------
Contains the aesthetic elements. `favicon.png` is the little snake that I got from Icons8; no particular reason other than the fact that I thought it was cute, plus most of this project was written in Python. `styles.css` is the stylesheet. I chose Nanum Gothic for the main font of the website because I like that font, but I did keep some of the major structures from CS50 Finance because I thought they looked clean and neat, like the navigation bar. I just played around with font sizes and colors until I found combinations that looked aesthetically pleasing and resonated with me.

templates
-----------
1. `apology.html` is mostly borrowed from CS50 Finance. 
2. `index.html` contains the formatting for the Upload File page. I used `enctype=multipart/form-data` because I was accepting files, and that was the way HTML encoded files. I only allowed the Upload File function to accept .csv files, because I figured the alternative (generating an error message for every non-csv file) would be an enormous headache to code, and besides, would waste the time of the user with the apology messages when they could instead just see that the non-compatible files are grayed out and not select them. I allowed multiple file selection because it's likely that the user would have run tests on multiple samples, and would want everything analyzed at once.
3. `info.html` just gives the instructions for using the app. I thought otherwise the homepage would look a little blank. And usually websites have an info section/how to use anyway.
4. `layout.html` is mostly borrowed from CS50 Finance, but I tweaked a couple things, like the name, the navigation bar, and the footer. Again, I thought the CS50 Finance layout was pretty clean, and I wanted to keep the website as minimalist and usable as possible.
5. `results.html` displays results and allows the user to download the image. Pretty straightforward. I put the chart above the Young's modulus and standard deviation stats because the user probably primarily wanted to see their data visualized, as that would be the first clue as to whether or not the data is usable. Also, I just felt like one line of text before an image would look weird. On the results page, there's also the download-png capability.

uploads
-----------
This is the folder I assigned to store all the files uploaded, as well as the .pngs created. `application.py` would call both the uploaded files and the images from this folder where necessary. I did this mainly to have a set directory for all the user-facing things to go into and come out of, separate from the rest of the website framework.