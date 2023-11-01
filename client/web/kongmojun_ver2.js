const express = require('express');
const ejs = require("ejs");
const app = express();
var mysql = require('mysql');

var connection = mysql.createConnection({
    host     : 'db-dna.crfn1h2rbeew.ap-northeast-2.rds.amazonaws.com',
    port     :  3306,
    user     : 'admin',
    password : 'Dna*1234',
    database : 'mysql2'
  });
  

// var connection = mysql.createConnection({
//   host     : '192.168.0.63',
//   port     :  3306,
//   user     : 'root',
//   password : 'pi',
//   database : 'mysql'
// });

connection.connect(function(err)
{
    if(err) throw err;
    console.log("마리아 DB 연동중..");
});

app.set("view engine", "ejs");
app.set('views', __dirname + '/views');
app.engine('html', require('ejs').renderFile);
app.use(express.urlencoded({extended: false}));
app.use(express.json());
app.use(express.static(__dirname+'/'));

app.get("/", function(req, res)
{
    res.render("kongmojun_ver2.html", {});
});

app.get('/backflow', (req, res) => {
    connection.query('SELECT * FROM backflow_distance ORDER BY DATETIME DESC LIMIT 1', function(err, rows, fields) {
    if (err) throw err;
    result= {datetime: rows[0].datetime, backflow_minute: rows[0].backflow_minute, distance_minute : rows[0].distance_minute}
    console.log(result);
    res.jsonp(result);
});
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

app.get('/counting', (req, res) => {
    connection.query('SELECT * FROM counting ORDER BY DATETIME DESC LIMIT 1', function(err, rows, fields) {
    if (err) throw err;
    data= {datetime: rows[0].datetime, counting : rows[0].counting}
    console.log(data);
    res.jsonp(data);
    //res.jsonp({datetime: rows[0].datetime, counting : rows[0].counting});
});
});

app.get('/iv_info', (req, res) => {
    connection.query('SELECT * FROM iv_info ORDER BY DATETIME DESC LIMIT 1', function(err, rows, fields) {
    if (err) throw err;
    data= {totalvalue: rows[0].totalvalue, infusionvalue : rows[0].infusionvalue, remaintime : rows[0].remaintime, gtt : rows[0].gtt}
    console.log(data);
    res.jsonp(data);
    //res.jsonp({datetime: rows[0].datetime, counting : rows[0].counting});
});
});

app.listen(3000, function()
{
    console.log("실행중..");
});
