var socket = io.connect(window.location.protocol + '//' + document.domain + ':' + location.port);

window.onload = function(){
  //var img = document.getElementById('feed');
  var canvas = document.getElementById('canvas');
  var canvas_processed = document.getElementById('canvas_draw');
  var imageCan = document.getElementById('imgCanvas')
  var ctx_square = canvas_processed.getContext('2d');
  var planesCan = document.getElementById('Canvasplanes');
  var ctx_planes = planesCan.getContext('2d');
  var resbox = document.getElementById('res_box');
  var descbox = document.getElementById('desc_box');
  var socket = io.connect(window.location.protocol + '//' + document.domain + ':' + location.port);
  socket.on('connect', function () {
  console.log("Connected...!", socket.connected)
  console.log(location.port)

  });

  console.log(feed.src);
  imageCan.height = feed.naturalHeight;
  imageCan.width = feed.naturalWidth;
  canvas_processed.height = feed.naturalHeight;
  canvas_processed.width = feed.naturalWidth;
  console.log(imageCan.width);
  resbox.style.width = imageCan.width/2+"px";
  descbox.style.width = imageCan.width/2+"px";
  var bgctx = imageCan.getContext('2d');
  //console.log(imageCan.width)
  bgctx.drawImage(bgImg,0,0,imageCan.width,imageCan.height);
  ctx_square.drawImage(aImg,0,0,canvas_processed.width, canvas_processed.height);
  ctx_planes.drawImage(planesImg,0,0,planesCan.width,planesCan.height);
  var checkbox = document.getElementById('expert');
  checkbox.addEventListener('change',function(){
    var res = document.getElementById("res_box");
    var desc = document.getElementById("desc_box");
    var exp = document.getElementById("expert_box");
    if(checkbox.checked){
      res.style.display = "none";
      desc.style.display = "none";
      exp.style.display = "block";
    }
    else{
      res.style.display = "block";
      desc.style.display = "block";
      exp.style.display = "none";

    }
  })
  var socketCan = document.getElementById('socketCanvas');
  var context = socketCan.getContext('2d')
  console.log(FPS)
  setInterval(() => {
  socketCan.width = feed.naturalWidth;
  socketCan.height = feed.naturalHeight;
  context.drawImage(feed, 0, 0, socketCan.width, socketCan.height);
  var data = socketCan.toDataURL('image/jpeg', 0.5);
  context.clearRect(0, 0, socketCan.width, socketCan.height);
  socket.emit('buffer_image', data);
}, 1000 / FPS);

}
socket.on('captured_image', function(img){
  var imageCan = document.getElementById('imgCanvas');
  var imgctx = imageCan.getContext('2d');
  var canImg = new Image();
  canImg.src = img.value;
  imageCan.width = canImg.naturalWidth;
  imageCan.height = canImg.naturalHeight;
  imgctx.drawImage(img,0,0,imageCan.width, imageCan.height);

})




function get_img(){
  //var img = document.getElementById('feed');
  var img2 = document.getElementById('mask');

//  var canimg = document.getElementById('canImg')
  var imageCan = document.getElementById('imgCanvas')
  //var canvas = document.getElementById('canvas');
  var canvas_processed = document.getElementById('canvas_draw')
  //var ctx = canvas.getContext('2d');
  var ctx_square = canvas_processed.getContext('2d');
  var imgctx = imageCan.getContext('2d')
  imageCan.width = feed.naturalWidth;
  imageCan.height = feed.naturalHeight;
  //canvas.width = img.width/2;
  //canvas.height = img.height/2;
  canvas_processed.width = feed.width;
  canvas_processed.height = feed.height;
  imgctx.drawImage(feed,0,0,feed.width, feed.height);
  //ctx.drawImage(img,0,0,canvas.width, canvas.height);
  ctx_square.drawImage(feed,0,0,canvas_processed.width, canvas_processed.height);
  ctx_square.globalAlpha = 0.3;

  ctx_square.drawImage(img2,0,0,canvas_processed.width, canvas_processed.height);
  //draw_square(canvas_processed,ctx_square);
  random_percantage();
  imgData = imageCan.toDataURL('image/jpeg', 1.0);
  socket.emit('clientImage', imgData);

}
function capture_video(){
  var img = document.getElementById('mask');
  var canvas = document.getElementById('imgCanvas');
  var video = document.getElementById('video');
  var ctx = canvas.getContext('2d');
  var canvas_processed = document.getElementById('canvas_draw')
  var ctx_square = canvas_processed.getContext('2d');
  ctx.drawImage(video,0,0,canvas.width,canvas.height);
  ctx_square.drawImage(video,0,0,canvas_processed.width, canvas_processed.height);
  //ctx_square.globalAlpha = 0.3;

  ctx_square.drawImage(img,0,0,canvas_processed.width, canvas_processed.height);
}
function random_percantage(){
  var colors = ['#F75151','#a0e77d','yellow'];
  var labels = ['Heart','Head','Abdomen','Left foot','Right foot', 'Right hand', 'Left hand']
  var head_detected = 90+10*Math.random();
  var abdominal_planes = 80+20*Math.random();
  var somethingsomething = 20+80*Math.random();
  var something_detected = 10+90*Math.random();

  document.getElementById('imgQ').style.backgroundColor = colors[Math.floor(Math.random()*colors.length)];
  document.getElementById("headD").style.backgroundColor = '#a0e77d';
  document.getElementById("abdom").value = abdominal_planes.toFixed(2)+"%";
  document.getElementById("headD").value = head_detected.toFixed(2)+"%";
  document.getElementById("SD").value = something_detected.toFixed(2)+"%";
  document.getElementById("SS").value = labels[Math.floor(Math.random()*labels.length)];
  if(something_detected < 50){
    document.getElementById("SD").style.backgroundColor = '#F75151';
  }
  else if(something_detected > 50 && something_detected < 90){
    document.getElementById("SD").style.backgroundColor = 'yellow';
  }
  else{
    document.getElementById("SD").style.backgroundColor = '#a0e77d';
  }
  /*if(somethingsomething < 50){
    document.getElementById("SS").style.backgroundColor = '#F75151';
  }
  else if(somethingsomething> 50 && somethingsomething < 90){
    document.getElementById("SS").style.backgroundColor = 'yellow';
  }
  else{
    document.getElementById("SS").style.backgroundColor = '#a0e77d';
  }*/
  if(abdominal_planes < 50){
    document.getElementById("abdom").style.backgroundColor = '#F75151';
  }
  else if(abdominal_planes> 50 && abdominal_planes < 90){
    document.getElementById("abdom").style.backgroundColor = 'yellow';
  }
  else{
    document.getElementById("abdom").style.backgroundColor = '#a0e77d';
  }

}
function applyMask(){
  var img2 = document.getElementById('mask')
  var canvas_processed = document.getElementById('canvas_draw')
  //var ctx = canvas.getContext('2d');
  var ctx_square = canvas_processed.getContext('2d');
  ctx_square.globalAlpha = 0.5;

  ctx_square.drawImage(img2,0,0,canvas_processed.width, canvas_processed.height);

}
function draw_square(canvas,ctx){
  var r = parseInt(((canvas.height/4)*Math.random()));
  var x = parseInt((canvas.width*Math.random()))+r;
  var y = parseInt((canvas.height*Math.random()))+r;
  if(y > canvas.height){
    y=y-(r*2);
  }
  if(x > canvas.width){
    x = x-(r*2);
  }
  ctx.beginPath();
  ctx.strokeStyle = 'rgba(200,0,150,1)';
  ctx.arc(x,y,r,50,0,2*Math.PI);
  ctx.arc(x,y,r-10,50,0,2*Math.PI);
  ctx.fillStyle = 'green';
  ctx.fill("evenodd");
  ctx.lineWidth = 5;
  ctx.stroke();

}
function show_hide(b) {
  if(b==0){
    var x = document.getElementById("res_div");
    var y = document.getElementById("res_btn");
    var z = "results"


  }
  else{
    var x = document.getElementById("desc_div");
    var y = document.getElementById("desc_btn");
    var z = "description";

  }
  if (x.style.display === "none") {
    x.style.display = "block";
    y.innerHTML =     'Hide '+z+' <i class="fa-solid fa-minus"></i>'

  } else {
    x.style.display = "none";
    y.innerHTML = "Show "+z+" <i class='fa-solid fa-plus'></i>"
  }
}
