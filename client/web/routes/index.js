// routes/index.js

var express = require('express');
var router = express.Router();

const maria = require('../maria');

/* GET home page. */
router.get('/', function(req, res, next) {
// 전에 만들어놨던 쿼리문을 아래와 같이 바꿔준다.
// 'select * from test' 를 'select * from user' 로 바꿔주면 된다.
  maria.query('select * from backflow_distance ORDER BY DATETIME DESC LIMIT 1', function(err, rows, fields) { // 쿼리문을 이용해 데이터를 가져온다.
    if(!err) {
      console.log(rows[0].distance_minute, rows[0].backflow_minute);
      res.send([rows[0].backflow_minute, rows[0].distance_minute]);
    } else {
      console.log("err : " + err);
      res.send(err);
    }
  });
});

module.exports = router;