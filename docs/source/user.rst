Glitter user documentation 
=====
Getting started
=====
**Logging in**

1. Start by visiting the home page of your website. Let’s, for the sake of argument, say that your site’s URL is http://www.example.org
2. To get to the administration dashboard (admin for short) all you have to do is add /admin/ to that URL - http://www.example.org/admin/ - and hit return.
3. You’ll then see a login screen with *Username* and *Password* fields. Type these details in and click *log in*.
4. If all is well, you should now be looking at a page headed *Django administration*.
5. If this is the first time you’ve logged in, it might be a good idea to update your password with something super-memorable and equally secure. You can do this by clicking *Change password*, located in the top right of the screen. See the 'Changing your password' section below for more.

**Apps and models**

All the functionality in Glitter breaks down into individual applications (apps) which deal with specific areas of functionality. The apps installed with the core Django Church package which you have access to, are listed in white text in the black bars. These are things like *Assets*, *Banners* and *Documents*.

Beneath each app, you’ll see individual models which relate to more granular areas of functionality. Typically these contain lists of things, so for example, the *Images* model under the *Assets* app contains a list of all the images that have been uploaded for use on the website.

You can either click on the app name which will drill you into a refined view of the models available to you, or click directly on the model names to jump to their list views.

Glitter allows admin Super-users to restrict access of particular features of the site to other users of the site. The typical example might be that several users are commissioned to keep the website up to date - and so need access to edit pages etc. - but won’t need to add events to the system.

Having the right access is important, because the apps and model you see when you log in will depend on the actions your profile has been given access to.

**UI basics**

Glitter’s UI is entirely consistent. If you see a button that’s called the same thing as one you’ve seen elsewhere, it’s a sure bet that it will do what you expect it to do. In our experience, this means that once a user has understood one section of the site, the rest of the system tends to be an open book to them.

It’s worth noting that the majority of the UI conventions we’ll talk about here are stock Django conventions which we inherit. Here’s a few of the UI conventions it’s helpful to bear in mind…

**Required/Options**

One of the simplest things to point to and one of the easiest things to overlook. When you’re looking at a form, for example let’s use the news post form (Home > News > Posts > Add post). Look at the the field labels running down the left side of the form. Note that 'Title', 'Category' and 'Date' are all bold while 'Image' and 'Teaser' are not. That’s because bold field labels denote required form elements while non-bold ones are optional.

**The green +**

In short, a green + symbol next to an object gives you quick access to dialogues that allow you to add one more of this kind of thing to the system. You can find them on each model row on the admin dashboard, giving you quick access to adding things without having to first click through to the list view.

You may also see them within larger forms where apps and models are cross-referencing each other. A good example of this is to be found with the *Add image* form in the Assets app (Home > Assets > Images > Add image). Alongside the *Category* combo-box, you’ll see the green +, clicking it will let you quickly add a new category to the combo-box without having to back out of adding the image and go back into the *Categories* model.

**The three saves**

At the bottom of every form you’ll find the same three save options, and they all have their uses…

*Save*, typically highlighted in pink. Clicking this button saves the form and takes you back to the model list.
*Save and continue editing* is incredibly useful. It’s like hitting control-S while you’re working on a Word doc; it saves the contents of the form, but keeps you on the form so you can continue your work without fear of losing it.
*Save and add another* saves the form and then takes you to a fresh, empty form ready for you to add another. This is particularly useful when you are adding multiple instances of a type of thing in a single session.

**What? No cancel button?**

Nope. Glitter doesn’t bother cluttering up your window with redundant buttons. If you’ve started something and you realise you don’t want to bother saving it, just navigate away from the page by hitting your browser back button. Nothing is saved until you save.

**Changing your password**

It’s a really, really good idea to keep your password safe, secret and as cryptic and/or random as you can manage. We can’t help you with that bit, but here’s how you get there…

1. From any page within the admin, click *Change password* in the top-right of the screen.
2. You’ll be presented with a form - start by typing your new password. 
3. Then type it a second time to make sure that there aren’t any typos.
4. You then need to enter your old password, which will confirm that you are who you say you are.
5. Click *Change my password* and you’re done!

Apps - Assets 
=====
If you want to add an image to a page, or link to a PDF - a newsletter for example - from a page, you first need to upload it to the CMS. *Assets* is where you do that.

**Asset models**

Assets are broken down into two groups, files and images. Images are exactly as you’d expect - typically photos of one form or another with file types such as JPG, GIF and PNG. Files are literally everything else: DOC, PDF, PPT, XLS, TXT etc. The models here are paired, in that files and images each have a counterpart category model where you can manage the categories for each. These two pairs are functionally identical as far as their management is concerned, so we’ll use files as the example case here…

**File categories**

1. Click Home > Assets > File categories
2. Here are listed all the categories that can be applied to files.
3. To edit an existing category, click the category name.
4. To add a new category, click *Add file category*.
Note - the only field available for editing is the category title itself.


**Files**

1. Click Home > Assets > Files. You should see a list of all the files currently available in the system.
2. Each file presents the following bits of meta information, from left to right:
	 - File title (click here to view)
	 - Category (as defined by the File categories model above)
	 - The URL of the asset (clicking lets you preview the file)
3. To edit an existing file, click the file name.
4. To add a new file, click *Add file*.

**Add a file**

1. Click Home > Assets > Files > Add file
2. Category defines the category the file as tagged with
3. Title defines the title of the image - for admin use
4. File defines the file to be uploaded. Click *Choose File* and browse to the asset you wish to upload.
When saving and uploading an asset, the page will appear to be inactive for the duration of the upload. 

**Editing files**

1. Click Home > Assets > Files > [file title]
2. When editing an existing asset, this field contains two further elements. *Currently* denotes the file currently uploaded, clicking previews the asset and *Change* lets you replace the existing asset with another.

Apps - Auth 
======

An abbreviation of 'Authentication', *Auth* is where you manage user profiles, who can log in and what they can edit when they do.

**Auth models**

Auth contains two models, *Groups* and *Users*. The latter contains individual profiles for users with all their associated privileges, the former allows admins to assign privileges to defined groups. Users can then be added to those groups and inherit their privileges from them. Creating Groups makes it very quick and easy to set up quite specific levels of privileges initially, and then apply those privileges in bulk quickly and easily.

**Groups**

1. Click Home > Auth > Groups
2. Here are listed all of the groups that can be applied to user profiles.
3. To edit an existing group, click the group name.
4. To add a new group, click *Add group*.
5. *Name* defines the tag that can later be applied to user profiles
6. *Permissions* defines what permissions a group has. The left column contains all the available permissions in the system, while the right contains all the permissions assigned to the current group.
7. Individual permissions can be moved between the columns by selecting items and then clicking the arrow icons; or by double clicking an item.

**Users**

1. Click Home > Auth > Users

2. Here are listed all the user profiles registered with the system.

3. Each user presents the following bits of meta, from left to right…
	 - Username (click here to view)
	 - Email address for this user
	 - First Name
	 - Last name
	 - Staff status (a tick here indicates that the user has access to the admin dashboard)
	 
4. To edit an existing user, click the username.

5. To add a new user, click *Add user”*. 

**Adding a user**

Adding users is a two stage process. It’s recommended that you undertake both in order to fully create a user profile in a single sitting, but this isn’t strictly required…

1. Click Home > Auth > Users > Add user

2. *Username* is the name that a user uses to access the admin. It must be 30 characters or fewer, consisting of letters, digits and @/./+/-/_ only.

3. *Password* and *Password confirmation* should be identical for verification purposes.

4. Click *Save and continue editing* -  the page will refresh with the second tier of options. You will note that the username value previously filled in is reproduced here. The password will look broken - don’t panic! It’s not broken, it’s encrypted so that other users can’t abuse other user’s passwords.

5. Personal info
	- First name
	- Last name
	- Email address for ease access and support.

6. Permissions
	- Active checkbox designates whether this user should be treated as active. Unselect this instead of deleting accounts.
	- Staff status checkbox designates whether the user can log into the admin site.
	- Superuser status checkbox gives you super powers! No, seriously it designates that this user has all permissions without explicitly assigning them.
	- Groups defines whether the user belongs to a group, inheriting that group’s permissions.
	- User permissions defines what permissions a user has in addition to inherited group permissions. The left column contains all the available permissions in the system, while the right contains all the permissions assigned to the current user.
	- Individual permissions can be moved between the columns by selecting items and then clicking the arrow icons; or by double clicking an item.

7. Important dates
		- *Last login* denotes the date and time of this users last use of the CMS.
		- *Date joined* denotes the creation date of the users profile.
		- Both these fields can be edited, but are included largely for reference purposes.

**Editing a user**

1. Click Home > Auth > Users > [username]
2. This has the effect of dropping you directly into the second of the two stages, point 5. under 'Adding a user' above.

Apps - Events 
=====
Structuring events generally isn’t easy, and so we’ve sought to break it down into a structure that would make sense to most users - on both the admin and on the public sides of your site.

**Events tree view**

Click Home > Events. Here’s a list of all of the events currently available in the system. Each event presents the following bits of meta, from left to right…
	- Title (click here to view)
	- Start - the start date and time of the event
	- End - the end date and time of the event 
	- Category - to group certain events together 
To edit an existing event, click the event title.

To add a new event, click *Add special event*.

**Adding an event** 

Click Home > Events > Events > Add event +

1. *Title* defines the title of the event. Note that this is the publicly visible title that users of the site will see. 
2. *Category* to add the event to a group of similar events.
3. *Location* is an optional field for defining where the event will take place (some of these are  fairly self-explanatory) 
4. *Image* is another optional field that allows you to include a key image to associate with the event. Clicking the drop-down menu will reveal a list of images from the Image Assets app; you just need to choose the most appropriate for the event.
5. *Summary* is where you enter the descriptive text about the event, which is seen when users navigate through to the event’s detail page.
6. *Start* and *End*, which define the event’s start and end date and time.


**Advanced option**

*Slug* - This is the human-readable portion of the event's URL once it's live. For example, an event with the slug 'coffee-morning', the resulting URL would be http://www.example.org/events/view/special-event/.Note that standard URL character limitations apply here.

Apps - News
=====
Call it news, call it a blog, call it a journal for your organisation. Whatever you call it, *News* is an area to store individual articles as a generic, date-ordered content type.

**News models**
News contains two models, *Categories* and *Posts*. The latter contains individual news articles, and the former contains categories which can be applied to individual posts. These categories are automatically reflected in your site’s navigation to help users find the kind of content they are most interested in.

**Categories**
1. Click Home > News > Categories
2. Here are listed all the categories that can be applied to news.
3. To edit an existing category, click the category name.

**Add a category**

To add a new category, click *Add category*. There are two fields available for editing…

- *Title* which is the label visible to the public, so this needs to be short and descriptive of the kind of news users will find tagged with it.

- *Slug* which refers to the human-readable portion of the articles URL once it’s live. For example as article with the slug 'newsletter', the resulting URL would be http://www.example.org/news/2014/05/18/newsletter/
(Note that standard URL character limitations apply here)

**Posts**

1. Click Home > News > Posts

2. Here’s a list of all the news articles posted to the system.

3. Each post presents the following bits of meta, from left to right…
	- *Title* click on these to view the posts themselves
	- *Date* the post date
	- *Category* to add the event to a group of similar events.
	- *Published* denoting whether the post is visible to the public
	
4. To edit an existing post, click the title.

5. To add a new post, click *Add post*.

**Add post**

1. Click Home > News > Posts > Add post

2. *Title* defines the title of the post (publicly visible)

3. *Category* defines the category the post is tagged with

4. *Date* defines the date at which the post is visibly published to the site. Note that this value can be in the future as well as the past, meaning it can be used to set a post to ‘go live’ automatically at a particular date and time.

5. *Image* defines an optional key image for the post which is automatically included on the news pages where the story appears.

6. *Summary* represents the body of the article. Please refer to the section called 'WYSIWYG text editing' above for more details on how to get the most out of this field.

7. Advanced options

	- *Slug* which refers to the human-readable portion of the articles URL once it’s live. For example as article with the slug 'newsletter', the resulting URL would be this “http://www.example.org/news/2014/05/18/newsletter/”. Note that standard URL character limitations apply here.
	- The *Published* checkbox defines whether the post is visible to the public or not. This option can be used to keep private posts which are in draft-form and not quite ready to be seen by the world at large. It can also be used to retrospectively hide posts.

Apps - Pages
=====
In the majority of cases, pages within a site will account for the vast majority of your content. The Pages app gives you the tool, not only to manage the content on a given page, but to manage the structure of those pages and how they appear to the user.

**Managing page and page structures**

1. Click Home > Pages > Pages

2. The Pages app has only one model, itself called ‘Pages’. It differs from many of the other apps, in that the default tree view of the app’s contents is functional. 

3. Each row in the tree represents a page on your site. Each row (for example /sunday/ – This Sunday (edit) ) will contain the following elements…
		- /sunday/ which relates to the pages slug within the site’s URL
		- Sunday which relates to the pages title as it will appear in navigation
		- (edit) click to edit the page’s content
		- If a page has related sub-pages, these appears as ‘nested’ trees within their parent. Sub-pages are indicated by the presence of an arrow to the left of the page. Clicking this arrow shows/hides the sub-pages which, when visible, are indented to indicate their parentage.


**Adding a page**

1. Click Home > Pages > Pages > Add page

2. *URL* defines the portion of the page’s URL that appears after your site’s domain name, /about/ for example where the full URL is http://www.example.org/about/. Note that the URL requires leading and trailing slashes!

3. *Title* defines the publicly visible title which users will see on the site. Try to keep this short and to the point.

4. *Parent* enables you to define the page’s location directly, rather than using the drag-and-drop tool found in the 'Tree view' noted above. Clicking the combo box with give you a list of ALL the pages in the CMS. Moving a page is as simple as clicking the page you want to be the current page’s parent.

5. *Login required* determines whether users need to have a user profile and login before they can view a page. Check the box to enforce the login.

6. The *show in navigation* checkbox enables you to hide pages by unchecking. Note that the page is still live, but won’t appear in public navigation. This means that users of your site can still see the page if they have it bookmarked or, for example, if you email them a link to it.

Support
This documentation was produced by Kerrie Malone, account executive at Blanc Limited, the open source publishers of Glitter.

It is accurate at the time of publishing, but we’re sure that you good people will find gaps and will have questions we haven’t anticipated. With that in mind, please don’t hesitate to direct any questions you have to support@blanc.ltd.uk and we’ll see how we can assist you. Moreover, when we are asked a question about the platform that isn’t covered here, we’ll add the answer to these documents with the aim of growing and developing content over time.
