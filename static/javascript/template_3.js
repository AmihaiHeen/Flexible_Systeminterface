window.onload = function(){
  var canvas_processed = document.getElementById('canvas_draw');
  var imageCan = document.getElementById('frozenCanvas')
  var ctx_square = canvas_processed.getContext('2d');
  var planesCan = document.getElementById('Canvasplanes');
  var ctx_planes = planesCan.getContext('2d');
  var bgctx = imageCan.getContext('2d');
  //console.log(imageCan.width)
  bgctx.drawImage(bgImg,0,0,imageCan.width,imageCan.height);
  ctx_square.drawImage(aImg,0,0,canvas_processed.width, canvas_processed.height);
  ctx_planes.drawImage(planesImg,0,0,planesCan.width,planesCan.height);
}


function change(msg){
  var frozen = document.getElementById('frozen');
  frozen.src = msg.value;

}
function draw_frozen_image(){
  var frozen = document.getElementById('frozen');
  var frozenCanvas = document.getElementById('frozenCanvas');
  var frozen_ctx = frozenCanvas.getContext('2d');
  console.log(frozen.height);
  frozen_ctx.drawImage(frozen,0,0,frozenCanvas.width, frozenCanvas.height);
}
