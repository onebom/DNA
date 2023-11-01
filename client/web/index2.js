const express = require('express');
const app = express();
const ejs = require("ejs");
const port = 3000
const router = express.Router();
var mysql      = require('mysql');

var connection = mysql.createConnection({
  host     : '192.168.0.63',
  user     : 'root',
  password : 'pi',
  database : 'mysql'
});

app.set("view engine", "ejs");
app.set('views', __dirname + '/views');
app.engine('html', require('ejs').renderFile);
app.use(express.urlencoded({extended: false}));
app.use(express.json());
app.use(express.static(__dirname+'/'));

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
  
app.get("/", function(req, res)
  {
      res.render("kongmojun_ver1.html", {});
  });

app.post("/postTest", function(req,res)
  {
      length = req.body.test
      if((parseInt(length) > 0) && (parseInt(length) < 80))
      {
          result = connection.query('INSERT INTO motor(motorlength) VALUES(?)', req.body.test);
          console.log(length)
          res.json({ok:true});
      }
  });

app.post("/postTestUp", function(req,res)
  {
      
      length = req.body.test
      if(parseInt(length) < 80)
      {
          result = connection.query('INSERT INTO motor(motorlength) VALUES(?)', (parseInt(req.body.test)+parseInt(1)));
          console.log(length)
          res.json({ok:true});
      }
  });
  
app.post("/postTestDown", function(req,res)
  {
      length = req.body.test
      if(parseInt(length) > 0)
      {
          result = connection.query('INSERT INTO motor(motorlength) VALUES(?)', (parseInt(req.body.test)-parseInt(1)));
          console.log(length)
          res.json({ok:true});
      }
  });
 
app.listen(port, () => {
  console.log(`Example app listening at http://127.0.0.1:${port}`);
});