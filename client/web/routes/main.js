module.exports = function(app)
{
    app.get('/',function(req,res)
    {
        res.render('motor.html',{});
        console.log(1);
    });

    app.post("/postTest", function(req,res)
    {
        length = req.body.test
        result = con.query('INSERT INTO motor(motorlength) VALUES(?)', req.body.test);
        console.log(length)
        res.json({ok:true});
        console.log(result);
        console.log(2);
    });

    app.get('/backflow', (req, res) => 
    {
        connection.query('SELECT * FROM backflow_distance ORDER BY DATETIME DESC LIMIT 1', function(err, rows, fields) {
        if (err) throw err;
        result= {datetime: rows[0].datetime, backflow_minute: rows[0].backflow_minute, distance_minute : rows[0].distance_minute}
        console.log(result);
        res.jsonp({datatime: rows[0].datetime, backflow_minute: rows[0].backflow_minute, distance_minute : rows[0].distance_minute});
        console.log(3);
        });
    });

    app.get('/counting', (req, res) => 
    {
        connection.query('SELECT * FROM counting ORDER BY DATETIME DESC LIMIT 1', function(err, rows, fields) {
        if (err) throw err;
        data= {datetime: rows[0].datetime, counting : rows[0].counting}
        console.log(data);
        res.jsonp({datetime: rows[0].datetime, counting : rows[0].counting});
        console.log(4);
        });
    });
}