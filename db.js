// db.js
const { Pool } = require('pg');

const pool = new Pool({
    user: 'postgres',          // your PostgreSQL username
    host: 'localhost',
    database: 'postgres',      // your database name
    password: 'Sun49chicago',  // your PostgreSQL password
    port: 5432,                // default PostgreSQL port
});

module.exports = pool;