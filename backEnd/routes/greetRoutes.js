// backend/routes/greetRoutes.js
const express = require('express');
const { greet } = require('../controllers/greetController');
const router = express.Router();

router.get('/greet', greet);

module.exports = router;
