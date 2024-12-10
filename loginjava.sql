import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.Scanner;

public class LoginPage {
    public static void main(String[] args) {
        // Database connection details (for SQL, e.g., MySQL)
        String dbURL = "jdbc:mysql://localhost:3306/your_database_name";
        String dbUser = "your_username";
        String dbPassword = "your_password";

        // Replace the above with MongoDB details if needed

        // User input for login
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter username: ");
        String username = scanner.nextLine();
        System.out.print("Enter password: ");
        String password = scanner.nextLine();

        try {
            // Establishing a connection to the database
            Connection connection = DriverManager.getConnection(dbURL, dbUser, dbPassword);

            // SQL query to validate user
            String sqlQuery = "SELECT * FROM users WHERE username = ? AND password = ?";
            PreparedStatement preparedStatement = connection.prepareStatement(sqlQuery);
            preparedStatement.setString(1, username);
            preparedStatement.setString(2, password);

            // Execute the query
            ResultSet resultSet = preparedStatement.executeQuery();

            if (resultSet.next()) {
                // Successful login
                System.out.println("Login successful! Welcome, " + username + "!");
            } else {
                // Failed login
                System.out.println("Invalid username or password. Please try again.");
            }

            // Close the connection
            connection.close();
        } catch (Exception e) {
            System.out.println("An error occurred: " + e.getMessage());
        }

        scanner.close();
    }
}
