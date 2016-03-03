var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/*', function(req, res, next) {
  console.log("Receive new video request");
  res.render('video', { roomid: req.query.roomid });
});


module.exports = router;
