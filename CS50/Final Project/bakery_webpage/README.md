# Bakery Webpage
### **Video Demo:**  <https://youtu.be/FgvryvI32UI>
### **Description:**
---
#### _**Client side:**_
The first thing we can see is the navbar. While hovering on it, it's padding increases. All the links only work inside of the webpage. In the center of the navbar there is the brand's name, which on hover there would be a shadow coming from it, while the other links underline on hover. While scrolling down, the navbar hides and while scrolling up, it appears using JavaScript.

Next we can see the slideshow, with three images, which was implemented using bootstrap.

Then, there is the welcoming division, which appears with an animation while scrolling down using the AOS library, as well as most of the following sections.

After that we can see the products section, which includes three options: breads, cakes and desserts. While hovering on the images we see its' text appearing and the image on the background becoming blury. When the client clicks any of them, they would be redirected to another page where will be displayed the products the bakery has.

Coming back to the homepage, we will see the client references section which has three messages.

Next there is the location division which includes the brands logo, the location, the dates the bakery is closed, the directions and the location map.

Finally, there is the contacts section which includes the company’s phone and the social media.

The homepage and the products display page are responsive.


---
#### _**Admin side:**_
The webpage also includes an external link where the owner of the bakery can edit some things of the webpage.

First, there is the registration page, which includes the username, password, password confirmation and the bakery password so not any kind of person has access to this side of the webpage. Then, the user can login normally in the admins webpage side.

On the homepage side, they can currently only edit the slideshow section, and can see the preview of the images they submit, as well as the current images inside the slideshow.

They can also delete or add any product inside of the breads, cake and desserts section. They also have a preview of the products in the section they would like to change. When adding a new product, they must provide the image, title, price and description.

Finally they can log out at any time and would be redirected to the login page.

The webpage can support “hackers” or malicious people who would like to change the required attribute inside the forms.

---
#### _**App.py:**_
It is the back-end of the wep app and includes all the libraries needed for the images, session, templates side of the webpage.

I decided to recycle some of the configuration needed from the finance pSet as my webpage was also going to include some of it's programs. (Some of the libraries, login function and the login required function)

It includes the location the images will be located and the bakery password.

Then, there is the homepage which includes of the files and text needed from the sql bakery database so the owner of the webpage can change some things if wanted, as well as the products section.

Next, it includes the registration function which is almost the same as the finance section but including the bakery password input for security. It saves the user inside of the sql database.

The edit function includes the necessary code to change the images from the slideshow. As well as the images from the database so the user can see the current images inside the slideshow.

Next, there is the products edition function, which first gets the amount of products there is inside of the database so then it can loop through the post requests and see if the user wants to delete an image. If it does, the code would delete the file, the row inside of the database and reduce the counts table. If the user doesn't want to delete an image (and they reached via POST), the code will asume hey want to add a new product, so it asks for all the necessary input and add the image inside the static file, adds into the count table and update the database for the product.

#### _**HTML, CSS & JavaScript files:**_
For this wepage I decided to keep most of the necessary things for the client inside one page. (As I got the inspiration from my aunts' bakery there wasn't much things I could do with it, so making multiple pages for little information wasn't the best idea for me).

The main colors inside the homepage are: some sort of bread color, pink and white. And the divisions are separated by a stripes division.

For the products pages I decided to change a little bit, keeping the main information in a smaller division so it looks better.

In the admin's page I decided to keep the format from the products page so it looks a little different from the main homepage. With some JavaScript the user can see the preview from the image they want to submit.