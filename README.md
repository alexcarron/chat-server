# **Chat Server**

A backend system for a hypothetical chat application, featuring a PostgreSQL database and Python Flask API. This project provides robust server-side functionality for managing users, communities, channels, messages, and user authentication. Developed as part of the *SWEN-344 Engineering of Web-Based Software Systems* course.

---

## **Features**
- **User Management**: Create, update, and manage user accounts.
- **Community and Channel Management**: Create and manage communities and their channels.
- **Messaging**: Enable users to send and retrieve messages within specific channels.
- **Authentication and Sessions**: Handle secure user authentication, session management, and hashing.
- **Database Operations**: Utilize PostgreSQL for schema design and SQL-based interactions.
- **API Functionality**: Provide RESTful API endpoints for various chat app operations.
- **Testing**: Include modules to validate API endpoints and database operations.

---

## **Technologies Used**
- **Programming Language**: Python
- **Framework**: Flask
- **Database**: PostgreSQL
- **Testing**: Unit tests for API endpoints and database interactions
- **Other Tools**: SQL scripts for schema setup and test data insertion

---

## **Setup and Installation**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/alexcarron/chat-server.git
   cd chat-server
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Configuration**:
   - Create a `db.yml` file in the `config/` directory with your PostgreSQL credentials.
   - Example `db.yml` file:
     ```yaml
     # Configuration file for connecting to PostgreSQL
     host: localhost
     database: chat_server
     user: yourusername
     password: <password>
     port: 5432
     ```

4. **Run the Server**:
   ```bash
   python src/server.py
   ```

5. **Access API Endpoints**:
   - Use tools like Postman or cURL to test API endpoints.

6. **Run Unit Tests**:
   - Unit tests are provided to validate the API and database functionality. To run the tests using Python’s built-in `unittest` framework:
   ```bash
   python -m unittest
   ```
---

## **Modules Overview**

### **db_utils**
Contains functions for:
- Executing SQL queries.
- Managing database tables.

### **sql_files**
Includes SQL scripts for:
- Defining the database schema.
- Inserting initial test data.

### **apis**
Defines Flask routes for:
- User and community management.
- Channel and messaging operations.

### **auth_utils**
Handles:
- User authentication.
- Session key management.
- Password hashing.

### **tests**
Provides:
- Unit tests for API endpoints.
- Database functionality validation.


## **Future Enhancements**
- Add a front-end client for a complete chat application experience.
- Implement real-time messaging using WebSockets.
- Enhance security with OAuth or JWT-based authentication.

---

## **Acknowledgments**
This project was developed as part of the *SWEN-344 Engineering of Web-Based Software Systems* course at RIT.