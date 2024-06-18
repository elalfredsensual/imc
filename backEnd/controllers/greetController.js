// backend/controllers/greetController.js
const greet = (req, res) => {
    res.json({ message: 'Hello from Express!' });
  };
  
  module.exports = { greet };
  