// backend/server.js
const express = require('express');
const greetRoutes = require('./routes/greetRoutes');
const app = express();
const port = 3001;

app.use('/api', greetRoutes);

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
