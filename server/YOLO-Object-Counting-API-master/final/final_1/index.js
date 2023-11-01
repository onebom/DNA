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

app.get('/', (req, res) => {
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