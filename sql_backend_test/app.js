// app.js (your main app file)
const pool = require('./db');

async function runQueries() {
    try {
        // Example query 1
        const res1 = await pool.query('SELECT NOW()');
        console.log('Current time from DB:', res1.rows[0].now);

        // Example query 2
        const res2 = await pool.query('SELECT 1 + 1 AS result');
        console.log('1 + 1 =', res2.rows[0].result);

    } catch (err) {
        console.error('Error executing query:', err);
    }
}

// Run queries
runQueries();

// Optional: close pool when the app exits
process.on('exit', async () => {
    await pool.end();
    console.log('Pool connections closed on app exit.');
});