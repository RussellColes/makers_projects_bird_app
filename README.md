# WELCOME TO THE BIRD APP #

This is the final large project I completed at Makers Academy. We had complete free reign to create anything we wanted for the duration of the 2 week project. Our group decided that we wanted to consolidate some things we didn't feel we had learnt well enough, as well as consolidating our understanding of the link between the front end and the back end of the project. For these reasons, we focused on technologies rather than an app which would have a true real world application. We chose to focus on:
- A JavaScript / React frontend linking to a python backend to enable us to practise the newly acquired JavaScript knowledge while revising our python knowledge from earlier in the course.
- Improved test coverage (we all felt that this was something that had fallen by the wayside in the previous project as we ran out of time)
- ensuring that all of us understood what each part of the codebase was doing (in previous projects, we felt like we had sometimes accepted code other colleagues had written without understanding its purpose / syntax)
- api calls to external services, which none of us had done before.

The aim of the project decided upon was to create an app which allowed users to upload photos they have taken of birds. In its initial design, the app would send the image to google image lookup via an api call and return the name of the bird, the app would also use location services to note the location the bird was spotted in. As an MVP, we decided we would allow the user to state the name of the bird and the location of the bird on upload and look to add the additional functionality later on. As a comedic extra feature, we wanted to return a recipe that the user could use to cook said bird.

## Review of the project ##
Having used a pre set up MERN stack for the previous project, we had not realised how much time and effort goes into setting up the project before starting to write the code. Getting the python backend talking to the database and the JavaScript frontend took a lot more time than we had realised due to the need to get python to deal with asynchronous requests from the JavaScript frontend. This was a steep learning curve, but a worthwhile one. It did delay other aspects of the project and we had to stick with our MVP, thus not adding the api calls. Overall we created a functioning app and really learnt a huge amount, which is what it is all about. The test coverage for the backend is good, but I've definitely got some more learning to do when it comes to testing React components. This will be starting as soon as the course is over!

# Information from the start of the project #


## Please run these (in the parent directory) to get started

```bash
chmod +x start.sh

./start.sh
```

This makes a venv if there isn't one and install all the backend and frontend dependencies/libraries. Might need to install Node Package Manager if prompted.
