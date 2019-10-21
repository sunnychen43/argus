ARGUS is a website designed to help users stay informed in the upcoming Senate elections both within and outside their state. Log into ARGUS to keep track of what type of policies and motions you value. Then, take a quiz where you follow through different past policies and motions to see where you stand. ARGUS takes your votes and compares it to how other Senators voted, so you can see how  similar your views are. 

We incorporated HTML, Bootstrap, Javascript and CSS in front-end development of our application via a website. We used flask, a python-based solution for our backend, because it is both lightweight and accomplishes what we want: store user data and process requests from the frontend.

To collect our data, we downloaded the source from various government databases and used BeautifulSoup to parse the results. We stored the data in a SQLite database file, it can be accessed by our backend server.
