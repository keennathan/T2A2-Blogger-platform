# NathanKeen_T2A2

# Blogger Platform API Webserver

## R1 Explain the problem that this app will solve, and explain how this app solves or addresses the problem.
## Problem That This App Will Solve:
This app is a content management system (CMS) for a blogging platform that provides a structured environment for users with different roles to create, interact with, and manage blog content. It addresses the following problems found in modern multi-user blogging platforms:  
1. **User Authentication and Authorisation:**  
    - **Problem:** Modern web applications require secure mechanisms to authenticate users and control access to specific resources based on user roles.  Acoording to a *2020 study by Verizon*, over 80% of breaches are due to weak or stolen credentials, emphasizing the need for secure authentication.
    - **Solution:** This app solves the problem by implementing JWT-based authentication, ensuring that users' identities are securely verified. Role-based access control (RBAC) enforces restrictions based on user roles, allowing only admins and super admins to manage sensitive data like user roles and content.
2. **Role Management:**  
    - **Problem:** Managing permissions for various users can become complicated as the platform scales.
    - **Solution:** The app provides a comprehensive role management system where admins can assign roles (e.g., Admin, Author, Super Admin, Reader) to users. This ensures that each user has the appropriate permissions, which is crucial for minimising the risk of privilege abuse.  
3. **Blog Creation and Interaction:**  
    - **Problem:** Blog platforms need to support the creation, modification, and management of blog content.  As per *HubSpot's blogging statistics*, businesses that blog receive 55% more visitors than those that don't, highlighting the need for smooth blog creation and management.
    - **solution:** The app allows authors to create, edit, and manage blogs while enabling readers to interact through comments and likes. This encourages user engagement and ensures authors have the tools they need to manage content effectively.
4. **Media Management:**
    - **Problem:** Blogs often rely on rich media like images and videos to increase engagement, but managing these files and associating them with the correct content can be difficult.
    - **Solution:** The app includes a media management system that allows users to upload media, ensuring that each file is properly associated with the right blog post. This helps maintain the integrity of multimedia content on the platform, making blogs more engaging.
5. **Category and Organisation:**
    - **Problem:** Readers need a way to easily navigate blog content, and blogs need to be categorised for better organisation and discoverability. According to research, organised content improves user experience and retention rates.
    - **Solution:** The app includes a category system, which helps structure blogs into different sections (e.g., Technology, Lifestyle), enabling users to find relevant content quickly.
6. **Commenting and Liking System:**  
    - **Problem:** User engagement is a key factor for successful blogging platforms. Interaction through comments and likes not only boosts engagement but also provides valuable feedback for content creators.
    - **Solution:** The app provides a commenting system where users can leave feedback on blogs, and a liking system to express approval. Studies show that user engagement features like comments and likes improve user retention.

## How This App Solves or Addresses the Problem:  
1. **Secure Authentication and Role-Based Access Control:**
    - By using JWT for authentication and enforcing RBAC, the app addresses the security challenges mentioned above. This ensures that only authorised users can access specific content and perform certain actions, reducing the risk of unauthorised access and data breaches.
2. **Flexible Role Management:**  
    - The app solves the issue of privilege management by allowing admins to assign roles and control access to sensitive areas of the platform. This aligns with industry best practices for ensuring that users only have the minimum necessary permissions, reducing potential security risks.
3. **Comprehensive Content Creation Tools:**  
    - With tools for creating, editing, and managing blog posts, the app ensures that content creators can focus on writing, while readers have an intuitive and organised way to engage with the content. The platform's built-in interaction features (likes and comments) further enhance user engagement and retention.
4. **Multimedia Content Support:**  
    - The app enables the integration of images, videos, and other media into blogs, making content more engaging and aligning with the modern reader's expectations for rich multimedia experiences. This media management feature solves the problem of associating media files with specific blogs and maintaining their integrity.  
5. **Improved User Experience Through Categorisation:**  
    - By categorising blog posts, the app helps users easily navigate the platform, ensuring a better user experience. This organisational feature improves discoverability and enhances overall satisfaction, encouraging repeat visits and longer user sessions.
## Conclusion
This app addresses the common challenges faced by multi-user blogging platforms by providing robust authentication, flexible role management, efficient content creation tools, and enhanced user engagement features like commenting and liking. By implementing industry best practices in security, user management, and content organisation, the app ensures that it not only meets the needs of content creators and admins but also fosters an engaging experience for readers. The inclusion of references and statistics supports the app's value in solving real-world problems related to blogging and content management.

### Reference
* Verizon. (2020). Data Breach Investigations Report. https://www.verizon.com/business/en-gb/resources/reports/2020-data-breach-investigations-report.pdf
* Bump, P. (2023, December 21). 31 Business Blogging Stats You Need to Know in 2021. Blog.hubspot.com. https://blog.hubspot.com/marketing/business-blogging-in-2015

# R2 Describe the way tasks are allocated and tracked in your project.




# R3 List and explain the third-party services, packages and dependencies used in this app.
## Third-Party Services, Packages, and Dependencies Used in This App:
1. **Flask:**  
    - **Purpose:** Flask is a micro web framework for Python that allows developers to build web applications easily with minimal boilerplate code.
    - **How It's Used:** Flask serves as the core framework for routing, handling requests, and providing responses in this application.
    - **Package:** Flask==3.0.3
2. **Flask-SQLAlchemy:**
    - **Purpose:** Provides an Object Relational Mapper (ORM) that integrates SQLAlchemy with Flask, allowing the app to interact with the database using Python objects instead of raw SQL queries.
    - **How It's Used:** Used for defining database models, handling relationships between tables, and performing queries.
    - **Package:** Flask-SQLAlchemy==3.1.1
3. **SQLAlchemy:**  
    - **Purpose:** SQLAlchemy is the ORM used for interacting with the database in a Pythonic way, abstracting raw SQL into high-level operations.
    - **How It's Used:** SQLAlchemy provides the ORM layer that interacts with PostgreSQL through SQL queries and transactions.
    - **Package:** SQLAlchemy==2.0.32
4. **psycopg2-binary:**
    - **Purpose:** psycopg2-binary is a PostgreSQL database adapter for Python. It provides the necessary drivers to connect and interact with PostgreSQL databases.
    - **How It's Used:** This package allows Flask to communicate with a PostgreSQL database by providing a connection to execute SQL queries and manage transactions.
    - **Package:** psycopg2-binary==2.9.9
5. **Flask-JWT-Extended:**  
    - **Purpose:** Adds JWT (JSON Web Token) support to Flask, which is used for token-based authentication and user management.
    - **How It's Used:** The app uses JWTs to authenticate users and ensure secure access to routes that require authorisation.
    - **Package:** Flask-JWT-Extended==4.6.0
6. **Flask-Bcrypt:**  
    - **Purpose:** Provides bcrypt hashing utilities for securely storing user passwords.
    - **How It's Used:** Flask-Bcrypt is used to hash and verify passwords during user registration and login.
    - **Package:** Flask-Bcrypt==1.0.1
7. **Flask-Marshmallow:**
    - **Purpose:** Integrates Marshmallow with Flask to facilitate serialisation, deserialisation, and validation of data.
    - **How It's Used:** Handles converting SQLAlchemy models into JSON and validating incoming data from HTTP requests.
    - **Package:** flask-marshmallow==1.2.1
8. **Marshmallow:**
    - **Purpose:** A library for object serialisation and deserialisation, as well as data validation.
    - **How It's Used:** Used to validate and serialise/deserialise data before sending it in or receiving it from an API.
    - **Package:** marshmallow==3.21.3
9. **marshmallow-sqlalchemy:**
    - **Purpose:** Bridges Marshmallow and SQLAlchemy, automatically generating Marshmallow schemas from SQLAlchemy models.
    - **How It's Used:** Simplifies schema generation by mapping SQLAlchemy models directly to Marshmallow schemas.
    - **Package:** marshmallow-sqlalchemy==1.1.0
10. **python-dotenv:**
    - **Purpose:** Reads key-value pairs from a .env file and sets them as environment variables.
    - **How It's Used:** Loads environment variables such as database URIs and JWT secret keys, making the app configuration more secure and flexible.
    - **Package:** python-dotenv==1.0.1
11. **Jinja2:**
    - **Purpose:** A templating engine used by Flask to render HTML templates dynamically.
    - **How It's Used:** Used by Flask to insert dynamic content into HTML templates (if needed), although this functionality isn't explicitly shown in the code.
    - **Package:** Jinja2==3.1.4
12. **Werkzeug:**
    - **Purpose:** A WSGI utility library used by Flask for routing, request handling, and response generation.
    - **How It's Used:** Handles HTTP requests and responses under the hood for Flask applications.
    - **Package:** Werkzeug==3.0.3
13. **click:**
    - **Purpose:** A package for creating command-line interfaces (CLI). Flask uses Click to manage CLI commands such as running the app, setting up the database, etc.
    - **How It's Used:** Used internally by Flask for handling CLI commands.
    - **Package:** click==8.1.7
14. **PyJWT:**
    - **Purpose:** A Python library to encode and decode JSON Web Tokens (JWT).
    - **How It's Used:** Flask-JWT-Extended uses PyJWT to encode and decode tokens, ensuring secure authentication via tokens.
    - **Package:** PyJWT==2.9.0
15. **blinker:**
    - **Purpose:** A fast event-signal library for Python.
    - **How It's Used:** Used internally by Flask to handle signals for certain events, like before or after request processing.
    - **Package:** blinker==1.8.2  
### Summary
* **Web Framework:** Flask is the primary web framework used to build and serve the application.
* **Database Interaction:** Flask-SQLAlchemy, SQLAlchemy, and psycopg2-binary are used to define models, manage relationships, and connect to a PostgreSQL database.
* **Authentication:** Flask-JWT-Extended and PyJWT handle secure user authentication through JWTs, ensuring that routes are protected.
* **Password Security:** Flask-Bcrypt provides password hashing utilities, protecting user credentials.
* **Serialisation/Validation:** Flask-Marshmallow, Marshmallow, and marshmallow-sqlalchemy handle the serialization of complex objects to JSON and validation of incoming data.
* **Environment Management:** python-dotenv helps securely manage environment variables for configuration settings.
* **Template Rendering and HTTP Handling:** Jinja2 and Werkzeug manage template rendering (if necessary) and HTTP requests, respectively.  
<br>
All these dependencies work together to form a secure, robust, and scalable web application that manages content (blogs, media, comments) while ensuring proper authentication, authorisation, and database interactions.

# R4 Explain the benefits and drawbacks of this app’s underlying database system.
The underlying database system for this app is PostgreSQL, a powerful and feature-rich relational database management system. PostgreSQL is widely known for its robustness, scalability, and support for complex queries and data integrity, making it a strong choice for content management systems like this one, which involves managing users, roles, blogs, comments, and interactions like likes.  

## Pros
One of the biggest advantages of PostgreSQL is its ACID compliance, which ensures that transactions are processed reliably and consistently. This is critical for an application that handles sensitive operations such as user authentication, role management, and content creation. PostgreSQL also excels in maintaining data integrity through constraints like foreign keys and unique indexes, which enforce consistent relationships between entities such as users, blogs, and comments. Additionally, PostgreSQL's ability to efficiently handle complex queries and joins across related tables makes it well-suited for applications that need to query interconnected data, such as retrieving a blog post along with its comments, likes, and author information.  

## Cons
However, PostgreSQL also has some drawbacks, particularly in terms of complexity and resource demands. It can be more difficult to set up and maintain compared to simpler databases like SQLite, as it requires a dedicated server and proper configuration to run efficiently. PostgreSQL can also be resource-intensive, requiring adequate memory, CPU, and storage, which might increase operational costs, especially for smaller teams or projects. In addition, optimising performance under heavy write loads can be challenging, as PostgreSQL requires careful tuning to handle high-frequency updates and inserts efficiently.  

## Conclusion
Overall, PostgreSQL is a solid choice for this app due to its reliability, scalability, and ability to manage complex data relationships. While its complexity and resource demands can be a challenge, these are outweighed by its benefits, particularly for applications like this one that require strong data integrity, transactional consistency, and support for complex queries. As the app grows and handles more user interactions and content, PostgreSQL’s scalability and advanced features will ensure that it continues to perform efficiently.

### References
* Dhruv, S. (2019). Pros and Cons of using PostgreSQL for Application Development. [online] Aalpha. Available at: https://www.aalpha.net/blog/pros-and-cons-of-using-postgresql-for-application-development/.

# R5 Explain the features, purpose and functionalities of the object-relational mapping system (ORM) used in this app.
The object-relational mapping (ORM) system used in this app is SQLAlchemy, integrated with Flask via Flask-SQLAlchemy. SQLAlchemy abstracts the database interactions by mapping database tables to Python objects, enabling developers to manipulate database records using Python code rather than SQL queries. Below are its key features and functionalities:  
1. **Model Definition:** SQLAlchemy allows you to define database tables as Python classes, where each class represents a table and class attributes represent columns.  
    ```
    class Blogs(db.Model):
        __tablename__ = "blogs"
        blog_id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(255), nullable=False)
        content = db.Column(db.Text, nullable=False)
        user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    
        # Relationships
        user = db.relationship("User", back_populates="blogs")
    ```
    - **Explanation:** In this example, the `Blogs` model is mapped to the `blogs` table in the database, with attributes for the blog ID, title, content, and a foreign key `user_id` that links to the users table. SQLAlchemy automatically handles this relationship, allowing developers to access a blog's author via the `user` relationship.  
2. **CRUD Operations:** SQLAlchemy simplifies the process of performing CRUD operations on the database. Here's an example of **creating a new blog post:**
    ```
    @blog_bp.route("/", methods=["POST"])
    @jwt_required()
    def create_blog():
        # Get the current user from JWT
        current_user_id = get_jwt_identity()
        stmt = select(User).where(User.user_id == current_user_id)
        current_user = db.session.execute(stmt).scalar_one_or_none()

        # Creating a new blog post
        new_blog = Blogs(
            title=request.json['title'],
            content=request.json['content'],
            user_id=current_user.user_id
        )
        # Add the new blog to the session
        db.session.add(new_blog)
        # Commit the transaction to save it to the database
        db.session.commit() 

        return jsonify({"message": "Blog created successfully!"}), 201
    ```
    - **Explanation:** Here, SQLAlchemy is used to create a new `Blogs` object and add it to the session. The `db.session.add(new_blog)` method stages the new blog to be added to the database, and `db.session.commit()` commits the transaction, persisting the blog post in the database. This showcases the ease of performing Create operations with SQLAlchemy.  
3. **Relationship Management:** SQLAlchemy supports managing relationships between models, such as **one-to-many** relationships between `User` and `Blogs`. This allows developers to easily navigate between related records.  
    ```
    class User(db.Model):
        __tablename__ = "users"
        user_id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(255), unique=True, nullable=False)

        # Relationships
        blogs = db.relationship("Blogs", back_populates="user", lazy="dynamic")
    ```
    - **Explanation:** In this example, a `User` can have multiple blogs. The `blogs` relationship allows you to access all blog posts authored by a particular user. For instance, `user.blogs` would give you a list of all blogs linked to that user, leveraging SQLAlchemy's relationship management.  
## Conclusion
SQLAlchemy's ORM system in this app simplifies database interactions by mapping Python objects to relational tables, handling CRUD operations with ease, and managing complex relationships between entities like `User` and `Blogs`. By allowing developers to work at a higher abstraction level with Python code, SQLAlchemy reduces the need for writing raw SQL queries and provides a more intuitive way to work with the database, ensuring consistency and scalability in the application.


# R6 Design an entity relationship diagram (ERD) for this app’s database, and explain how the relations between the diagrammed models will aid the database design. This should focus on the database design BEFORE coding has begun, eg. during the project planning or design phase.




# R7 Explain the implemented models and their relationships, including how the relationships aid the database implementation. This should focus on the database implementation AFTER coding has begun, eg. during the project development phase.





# R8 Explain how to use this application’s API endpoints. Each endpoint should be explained, including the following data for each endpoint:

* HTTP verb
* Path or route
* Any required body or header data
* Response
