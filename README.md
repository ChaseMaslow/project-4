# UOCIS - Project 4
### Description
This is a Flask app designed to replace the [ACP Brevet Control calculator](https://rusa.org/octime_acp.html) found on the Randonneurs USA official website. Instead of being built around form entry as the input method, this web page responds to user input live, with no redirects or refreshes required, and displays calculated control times. The calculator accepts miles or kilometers, and does conversions automatically.

### How it Works
The algorithm used here is based on the information on the Randonneurs USA website, and what their calculator spits out. They have an informational page about that [here](https://rusa.org/pages/acp-brevet-control-times-calculator). On that page, there's a table of minimum and maximum speeds for different locations.

* To calculate a control's opening time, we use the maximum speed of every range preceding its location, summing together the expected traversal time for someone moving at maximum speed. For the closing time, we use just the minimum speed of the bracket the control falls within.
	* For example: A control at 550km opens at 200/34 + 200/32 + 150/30 = 17H08, and closes at 550/15 = 36H40.

My program has an internal copy of this table, with an additional bracket added to account for the more recent rule that relaxes closing times within the first 60km. For such controls, the minimum speed is treated as 20km/hr, and one hour is added to the time.

The table in the webpage is operated by a Javascript (+JQuery) front-end, while the algorithm is contained in the Python (+Flask) back-end. 

##### Modules Used
	Flask, Arrow, Nose (testing)
	JQuery, Moment

##### Author Info
	Chase Maslow
	chasemaslow@gmail.com

## How to start

#### Docker 
Go into your terminal or shell and navigate to the /brevets directory. With Docker installed, enter:
	`docker build -t {choose name here} .`
Once it's finished building, run the image. You'll want to expose port 5000 inside the container so you can access the web app.
	`docker run -d --name {choose name here} -p {any port}:5000 {image name}`
Now if you go to "localhost:{port you chose}" in your web browser you should see the webpage.

#### Web App
You should see a webpage titled "ACP Brevet Times" and a table with the columns "Miles", "Km", "Location", and so on.

When you input a distance into "Miles" or "Km", the app should automatically fill the other column, and calculate the opening and closing times. You can change the total brevet distance with the dropdown menu to the upper left, and the beginning date and time with the menu to the upper right.

	* Remember that when typing in input fields, you'll have to click somewhere on the page or press enter to get a response.

It is intended that inputted control distances be within the brevet distance selected, and in ascending order. If you input control distances greater than the brevet distance, or give a control a distance that is lower than that of the control immediately before it, the app will show you non-disruptive "error" messages under the "notes" column.