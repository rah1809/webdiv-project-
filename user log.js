const mongoose = require('mongoose');
const express = require('express');
const app = express();

// MongoDB connection string
mongoose.connect('mongodb://localhost:27017/LoginSystem', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => console.log("Connected to MongoDB"))
.catch((err) => console.log("Connection error:", err));

// User schema to store login data
const userSchema = new mongoose.Schema({
  username: String,
  password: String,
  email: String,
});

const User = mongoose.model('User', userSchema);

// Route to handle login
app.get('/login', (req, res) => {
  const { username, password } = req.query;

  // Find the user with matching username and password
  User.findOne({ username, password }, (err, user) => {
    if (err) return res.status(500).send("Error occurred.");
    if (!user) return res.status(404).send("User not found.");
    
    // If the user is found
    res.status(200).send(`Welcome, ${user.username}!`);
  });
});

// Start the server on port 3000
app.listen(3000, () => {
  console.log("Server running on port 3000");
});
