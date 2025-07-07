# Module 2 - Getting started

In this module you will:

- Create a Spanner instance
- Scale a Spanner instance
- Create a database
- Explore the Console and Spanner Studio

## Create an instance

First step is to create a new Spanner instance.

Open Spanner in the Console. You can do so by searching Spanner in the search box and selecting Spanner from the result list.

![alt text](images/image.png)

After selecting Spanner, the Console may take a few seconds to enable the Spanner API.

Click `CREATE PROVISIONED INSTANCE`

![alt text](images/image-1.png)

Under `Select an edition` select `Enterprise` and click `CONTINUE`.

![alt text](images/image-2.png)

Insert a name for the instance in the field `Instance name`. The `Instance ID` field is populated automatically.

Take note of the `Instance ID`; you need it for later tasks.

Click `CONTINUE`.

![alt text](images/image-3.png)

Under `Choose a configuration` select `Regional`.

In `Select a configuration` select a Google Cloud region.

Click `CONTINUE`.

![alt text](images/image-4.png)

Under `Select unit` select `Processing units (PU)`.

Select `Manual allocation` and insert `1000` in `Quantity`.

Click `CREATE`

![alt text](images/image-5.png)

Congratulations! Your new Spanner instance is ready to use.

![alt text](images/image-6.png)

## Scale an instance

Next step is to scale the instance down.

Click `EDIT INSTANCE` at the top of the Console.

![alt text](images/image-7.png)

Scroll down to the `Configure compute capacity` section.

Select `Processing units (PUs)`.

Select `Manual allocation`.

Insert `100` in the `Quantity` field.

Click `SAVE`.

![alt text](images/image-8.png)

Verify that the instance was properly scaled checking that `Compute capacity` now says `100 PUs (0 nodes)`.

![alt text](images/image-9.png)

## Create a database

Next we need a database.

Click `+ CREATE DATABASE`.

![alt text](images/image-10.png)

Insert a name for the database in the `Database name` field. Take note of the name for later tasks.

Under `Select database dialect` select `Google Standard SQL`.

Click `CREATE`.

![alt text](images/image-11.png)

The database is now ready.

![alt text](images/image-12.png)

## Explore the Console and Spanner Studio

Open Spanner in the Console. You can do so by searching Spanner in the search box and selecting Spanner from the result list.

![alt text](images/image.png)

The instance you have just created is listed at the bottom of the window.

Click on the name of the instance to open it.

![alt text](images/image-13.png)

The database you have just created is listed under `Databases` at the bottom of the window.

Click on the name of the database to open it.

![alt text](images/image-14.png)

Click `Spanner Studio` on the left of the window.

![alt text](images/image-15.png)

Click `QUICK TOUR` to review the elements of Spanner Studio's interface.

When prompted to try Gemini, simply close the message.

![alt text](images/image-16.png)

Type the following query in the empty Untitled query.

```sql
SELECT 'Hello Spanner' as message;
```

Click `RUN`.

The `RESULTS` tab at the bottom of the window displays the output of the query.

![alt text](images/image-17.png)

Click `EXPLANATION` to access they graphical query plan.

Click the `Expand` icon to expand the query output.

![alt text](images/image-18.png)

![alt text](images/image-19.png)

You can close the query tab by clicking on the X near "Untitled query".