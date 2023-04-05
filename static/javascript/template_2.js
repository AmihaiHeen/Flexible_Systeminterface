

window.onload = function(){
  var img = document.getElementById('frozen');
  var canvas = document.getElementById('canvas');
  var canvas_processed = document.getElementById('canvas_draw');
  var socketCan = document.getElementById('socketCanvas');
  var context = socketCan.getContext('2d')
  var imageCan = document.getElementById('imgCanvas')
  var ctx_square = canvas_processed.getContext('2d');
  var planesCan = document.getElementById('Canvasplanes');
  var ctx_planes = planesCan.getContext('2d');
  img.height = img.naturalHeight;
  img.width = img.naturalWidth;

  var bgctx = imageCan.getContext('2d');
  //console.log(imageCan.width)
  bgctx.drawImage(bgImg,0,0,imageCan.width,imageCan.height);
  ctx_square.drawImage(aImg,0,0,canvas_processed.width, canvas_processed.height);
  ctx_planes.drawImage(planesImg,0,0,planesCan.width,planesCan.height);
  var checkbox = document.getElementById('expert');
  checkbox.addEventListener('change',function(){
    var res = document.getElementById("res_box");
    var desc = document.getElementById("desc_box");
    var anom = document.getElementById("anomaly");
    if(checkbox.checked){
      res.style.display = "none";
      desc.style.display = "none";
      anom.style.display = "block";
    }
    else{
      res.style.display = "block";
      desc.style.display = "block";
      anom.style.display = "none";

    }
  })
}

function change(msg){
  var frozen = document.getElementById('frozen');
  frozen.src = msg.value;

}
function draw_frozen_image(){
  var frozen = document.getElementById('frozen');
  //var img2 = document.getElementById('mask');

  var frozenCanvas = document.getElementById('imgCanvas');
  var canvas_processed = document.getElementById('canvas_draw')
  var ctx_square = canvas_processed.getContext('2d');
  var frozen_ctx = frozenCanvas.getContext('2d');
  console.log(frozen.naturalHeight);
  frozenCanvas.width = frozen.naturalWidth;
  frozenCanvas.height = frozen.naturalHeight;

  canvas_processed.width = frozen.naturalWidth;
  canvas_processed.height = frozen.naturalHeight;
  frozen_ctx.drawImage(frozen,0,0,frozenCanvas.width, frozenCanvas.height);

  //ctx.drawImage(img,0,0,canvas.width, canvas.height);
  ctx_square.drawImage(frozen,0,0,canvas_processed.width, canvas_processed.height);
  imgData = frozenCanvas.toDataURL('image/jpeg', 1.0);
  socket.emit('clientImage', imgData);
  //ctx_square.globalAlpha = 0.3;
  //ctx_square.drawImage(img2,0,0,canvas_processed.width, canvas_processed.height);
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
