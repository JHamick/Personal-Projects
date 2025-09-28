// server.js
const express = require('express');
const pool = require('./db');
const path = require('path');

const app = express();
const PORT = 3000;

// Serve static frontend files
app.use(express.static(path.join(__dirname, 'public')));

// API endpoint to get current time from PostgreSQL
app.get('/api/time', async (req, res) => {
    try {
        const result = await pool.query('SELECT NOW()');
        res.json({ currentTime: result.rows[0].now });
    } catch (err) {
        console.error('Database query error:', err);
        res.status(500).json({ error: 'Database query failed' });
    }
});

// Optional: another API endpoint example
app.get('/api/testsql', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM testsqlnbackendconnection');
        res.json(result.rows);
    } catch (err) {
        console.error('Error fetching testsqlnbackendconnection:', err);
        res.status(500).json({ error: 'Failed to fetch data' });
    }
});

// Add this middleware before your static file serving
app.use((req, res, next) => {
    res.set({
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    });
    next();
});

// Then your existing static file serving
app.use(express.static(path.join(__dirname, 'public')));

// Start the server
app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
