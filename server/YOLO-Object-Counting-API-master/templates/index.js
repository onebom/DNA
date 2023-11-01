const express = require('express')
const app = express()
// const fs = require('fs');
// const ejs = require('ejs');
const port = 3000

var mysql      = require('mysql');
var connection = mysql.createConnection({
  host     : '192.168.0.63',
  user     : 'root',
  password : 'pi',
  database : 'mysql'
});

app.get('/', (req, res) => {
  connection.query('SELECT * FROM counting ORDER BY DATETIME DESC LIMIT 1', function(err, rows, fields) {
    if (err) throw err;
    console.log('The count number is: ', rows[0].counting);
    res.send([rows[0].counting]);

    });

});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
