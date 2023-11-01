const express = require('express');
const app = express();
const port = 3000

var mysql      = require('mysql');

var connection = mysql.createConnection({
  host     : '192.168.0.63',
  user     : 'root',
  password : 'pi',
  database : 'mysql'
});

// app.use(express.json());

app.get('/backflow', (req, res) => {
        connection.query('SELECT * FROM backflow_distance ORDER BY DATETIME DESC LIMIT 1', function(err, rows, fields) {
        if (err) throw err;
        result= {datetime: rows[0].datetime, backflow_minute: rows[0].backflow_minute, distance_minute : rows[0].distance_minute}
        console.log(result);
        res.jsonp(result);
    });
});

app.get('/counting', (req, res) => {
        connection.query('SELECT * FROM counting ORDER BY DATETIME DESC LIMIT 1', function(err, rows, fields) {
        if (err) throw err;
        data= {datetime: rows[0].datetime, counting : rows[0].counting}
        console.log(data);
        res.jsonp({datetime: rows[0].datetime, counting : rows[0].counting});
    });
  });

app.listen(port, () => {
  console.log(`Example app listening at http://127.0.0.1:${port}`);
});