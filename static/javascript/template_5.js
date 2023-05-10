var sqr1 = document.getElementById('sqr1')
var sqr2 = document.getElementById('sqr2')
var sqr3 = document.getElementById('sqr3')
var sqr4 = document.getElementById('sqr4')

window.onload = function(){
  createCardNav(img_plc);
  createCanvas(img_plc);
  createCanvas(an_plc);
  if(res_plc==desc_plc){
    b = createRow(desc_plc)
    createRes(res_plc,b);
    createDesc(desc_plc,b);
  }
  else{
    a = 'sqr'+res_plc+''
    b = 'sqr'+desc_plc+''

    createRes(res_plc,a);
    createDesc(desc_plc,b);
  }
  //createButton();

  //createRes(res_plc);

  draw_images();


  $('#ImageList a').on('click', function (e) {
    e.preventDefault()
    $(this).tab('show')
  })
}

socket.on('output', function(output){
  console.log(output.res)
  var outR = output.res;
  var newImg = new Image();
  newImg.src = "data:image/jpeg;base64,"+outR[img_index];
  var canvas_processed = document.getElementById('canvas_draw');
  var ctx_square = canvas_processed.getContext('2d');
  setTimeout(function() {
    ctx_square.drawImage(newImg,0,0,canvas_processed.width, canvas_processed.height);
  }, 100);
  createResList(outR[labels_index],outR[resIndex])
  createDescText(outR[desc_index])
  document.getElementById('analyzedLink').click()
  //var returnArr = output.value;
})
socket.on('nextimg', function(msg){
  console.log('recieved: '+msg.value);
  draw_frozen_image(msg);
  document.getElementById('imageLink').click()

})

function disconnect(){
  socket.disconnect();
}
window.onunload = function(){
  disconnect();
}
window.onbeforeunload = function(){
  disconnect();
}
function createCardNav(pos){
  // create div with class "card bg-secondary"
const card = document.createElement('div');
card.classList.add('card', 'bg-secondary');

// create card header
const cardHeader = document.createElement('div');
cardHeader.classList.add('card-header','bg-dark');

// create unordered list with class "nav nav-tabs card-header-tabs"
const ul = document.createElement('ul');
ul.classList.add('nav', 'nav-tabs', 'card-header-tabs');
ul.setAttribute('id', 'ImageList');
ul.setAttribute('role', 'tablist');

// create first list item with class "nav-item"
const li1 = document.createElement('li');
li1.classList.add('nav-item','w-50');

// create first anchor with class "nav-link active"
const a1 = document.createElement('a');
a1.classList.add('nav-link', 'active','text-light');
a1.setAttribute('id','imageLink')
a1.setAttribute('href', '#capImageDiv');
a1.setAttribute('role', 'tab');
a1.setAttribute('aria-controls', 'capImageDiv');
a1.setAttribute('aria-selected', 'true');
a1.textContent = 'Captured image';

// create second list item with class "nav-item"
const li2 = document.createElement('li');
li2.classList.add('nav-item','w-50');

// create second anchor with class "nav-link"
const a2 = document.createElement('a');
a2.classList.add('nav-link','text-light');
a2.setAttribute('id', 'analyzedLink')
a2.setAttribute('href', '#analyzedImageDiv');
a2.setAttribute('role', 'tab');
a2.setAttribute('aria-controls', 'analyzedImageDiv');
a2.setAttribute('aria-selected', 'false');
a2.textContent = 'Analyzed image';

// append anchors to list items, and list items to unordered list
li1.appendChild(a1);
li2.appendChild(a2);
ul.appendChild(li1);
ul.appendChild(li2);

// append unordered list to card header
cardHeader.appendChild(ul);

// create card body
const cardBody = document.createElement('div');
cardBody.classList.add('card-body');

// create tab content div with class "tab-content mt-3"
const tabContent = document.createElement('div');
tabContent.classList.add('tab-content', 'mt-3');

// create first tab pane with class "tab-pane active" and id "capImageDiv"
const tabPane1 = document.createElement('div');
tabPane1.classList.add('tab-pane', 'active');
tabPane1.setAttribute('id', 'capImageDiv');
tabPane1.setAttribute('role', 'tabpanel');

// create second tab pane with class "tab-pane" and id "analyzedImageDiv"
const tabPane2 = document.createElement('div');
tabPane2.classList.add('tab-pane');
tabPane2.setAttribute('id', 'analyzedImageDiv');
tabPane2.setAttribute('role', 'tabpanel');
tabPane2.setAttribute('aria-labelledby', 'history-tab');

// append tab panes to tab content
tabContent.appendChild(tabPane1);
tabContent.appendChild(tabPane2);

// append tab content to card body
cardBody.appendChild(tabContent);

// append card header and card body to card
card.appendChild(cardHeader);
card.appendChild(cardBody);
document.getElementById('sqr'+pos[1]).appendChild(card)
}

function createRow(plc){
  console.log('hi'+plc)
  var row = document.createElement('div');
  row.setAttribute('id','sqr'+plc+'1')
  row.setAttribute('class','row')
  document.getElementById('sqr'+plc+'').appendChild(row)
  return 'sqr'+plc+'1'
}

function createButton(){
  if(btnMode == true){
    var btn = document.createElement('button');
    var btntxt = document.createTextNode('Capture image');
    btn.setAttribute('type','button');
    btn.setAttribute('id','button');
    btn.setAttribute('onclick', 'get_img()');
    btn.appendChild(btntxt);
    document.getElementById('col_1_row_2').appendChild(btn);
  }

}
function createDescText(text){
  var desc = document.getElementById('desc_div');
  desc.innerHTML =''
  var descP = document.createElement('p');
  descP.setAttribute('class','text-justify p-2');
  var pTxt = document.createTextNode(text);
  descP.appendChild(pTxt);
  desc.appendChild(descP)

}

function createResList(labels,results){
  var res_list = document.getElementById('res_list');
  res_list.innerHTML =''
  for(i=0;i<results.length;i++){
    //console.log(resIndex[i]);
    var count = i;
    var rLi = document.createElement('li')
    rLi.setAttribute('class','list-group-item d-flex justify-content-between bg-secondary')
    var colorDiv = document.createElement('div')
    if(typeof(results[i]) == 'string'){
      colorDiv.classList.add('foo')
      var colorTxt = document.createTextNode( ' '+results[i]);
    }
    else{

      if(results[i]>0.8){
        colorDiv.classList.add('foo','bg-success','border')

      }
      else if(results[i] < 0.8 && results[i] > 0.5){
        colorDiv.classList.add('foo','bg-warning','border')
      }
      else{
        colorDiv.classList.add('foo','bg-danger')
      }
      var colorTxt = document.createTextNode( ' '+results[i].toFixed(2));
    }

    var rLiTxt = document.createTextNode(labels[i]+' ');
    console.log(typeof(results[i]))
    colorDiv.appendChild(colorTxt)
    rLi.appendChild(rLiTxt);
    rLi.appendChild(colorDiv);
    res_list.appendChild(rLi);
  }
}
function createCanvas(place){
  if(imgBool){
    console.log(place[1])
    var cCanvas = document.createElement('canvas');
    if(place[0] == 'Captured Image'){
      var nav_tab = document.getElementById('capImageDiv');
      cCanvas.setAttribute('id', 'imgCanvas');
    }
    else{
      var nav_tab = document.getElementById('analyzedImageDiv')

      cCanvas.setAttribute('id', 'canvas_draw');
    }
    //console.log('col'+place[1]+'');
    cCanvas.classList.add('w-100','rounded')
    h = window.innerHeight/2;
    w = window.innerWidth/2
    cCanvas.setAttribute('height',''+480+'px');
    cCanvas.setAttribute('width',''+640+'px');
    var title = document.createElement('h2');

    nav_tab.appendChild(cCanvas);
  }
}



function draw_images(){
  var capCan = document.getElementById('imgCanvas')
  var draw = document.getElementById('canvas_draw');
  var draw_ctx = draw.getContext('2d');
  var ctx = capCan.getContext('2d')
  draw_ctx.drawImage(aImg,0,0,draw.width,draw.height);
  ctx.drawImage(bgImg,0,0,capCan.width,capCan.height);
}

function draw_frozen_image(msg){
  var capCan = document.getElementById('imgCanvas')
  var ctx = capCan.getContext('2d')
  var img = new Image();
  img.src = msg.value;
  setTimeout(function() {
  ctx.drawImage(img,0,0,capCan.width,capCan.height);
  }, 100);
}

function createDesc(plc,b){
  if(descBool){
    var descbox = document.createElement('div');
    descbox.setAttribute('id','desc_box');
    if(res_plc == desc_plc){
      descbox.setAttribute('class', 'accordition col-6 col-sm-6  w-50 ');
    }
    else{
      descbox.setAttribute('class', 'accordition col');

    }
    var descCard = document.createElement('div');
    descCard.setAttribute('class', 'card bg-secondary');

    var descCH = document.createElement('div');
    descCH.setAttribute('class', 'card-header bg-secondary');
    descCH.setAttribute('id','headingOne');

    var descH = document.createElement('h5');
    descH.setAttribute('class','mb-0 w-100')


    var descBtnTxt = document.createTextNode('Toggle description');



    var descbtn = document.createElement('button');
    descbtn.setAttribute('class', 'btn btn-secondary w-100');
    descbtn.setAttribute('type', 'button');
    descbtn.setAttribute('id','desc_btn');
    descbtn.setAttribute('data-toggle','collapse');
    descbtn.setAttribute('data-target','#desc_div');
    descbtn.setAttribute('aria-expanded','false');
    descbtn.setAttribute('aria-controls','desc_div');
    descbtn.appendChild(descBtnTxt);

    descH.appendChild(descbtn)
    descCH.appendChild(descH)


    var descP = document.createElement('p');
    descP.setAttribute('class','text-justify p-2');

    var pTxt = document.createTextNode('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.');
    descP.appendChild(pTxt);

    var descdiv = document.createElement('div');
    descdiv.setAttribute('class', 'describtion_div collapse show multi-collapse');
    descdiv.setAttribute('id','desc_div');
    descdiv.setAttribute('style','overflow-y:scroll;max-height:15rem;')

    //descdiv.appendChild(descP);

    descCard.appendChild(descCH);
    descCard.appendChild(descdiv);

    descbox.appendChild(descCard)

    document.getElementById(b).appendChild(descbox);
  }
}
function createRes(plc,b){
  if(resBool){
    var resbox = document.createElement('div');
    resbox.setAttribute('id','res_box');
    if(res_plc == desc_plc){
      resbox.setAttribute('class', 'accordition col-6 col-sm-6 w-50');
    }
    else{
      resbox.setAttribute('class', 'accordition col');
    }
    var resCard = document.createElement('div');
    resCard.setAttribute('class', ' card bg-secondary');
    //resCard.setAttribute('style','max-width:20rem;')

    var resCH = document.createElement('div');
    resCH.setAttribute('class', 'card-header bg-secondary');
    resCH.setAttribute('id','headingOne');

    var resH = document.createElement('h5');
    resH.setAttribute('class','mb-0');

    var resBtnTxt = document.createTextNode('Toggle Results');


    var resbtn = document.createElement('button');
    resbtn.setAttribute('class', 'btn btn-secondary w-100');
    resbtn.setAttribute('type', 'button');
    resbtn.setAttribute('id','res_btn');
    resbtn.setAttribute('data-toggle','collapse');
    resbtn.setAttribute('data-target','#res_div');
    resbtn.setAttribute('aria-expanded','false');
    resbtn.setAttribute('aria-controls','res_div');
    resbtn.appendChild(resBtnTxt);

    resH.appendChild(resbtn)
    resCH.appendChild(resH)

    var resUl = document.createElement('ul');
    resUl.setAttribute('class','list-group list-group-flush');
    resUl.setAttribute('id','res_list')

    var resdiv = document.createElement('div');
    resdiv.setAttribute('class', 'describtion_div collapse show multi-collapse');
    resdiv.setAttribute('id','res_div');
    resdiv.setAttribute('style','overflow-y:scroll;max-height:15rem;')

    resdiv.appendChild(resUl);

    resCard.appendChild(resCH);
    resCard.appendChild(resdiv);

    resbox.appendChild(resCard);
    document.getElementById(b).appendChild(resbox);
  }
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

function get_img(){
  var feed = new Image();
  var imageCan = document.getElementById('imgCanvas')
  var imgctx = imageCan.getContext('2d')
  feed.src = url;
  setTimeout(function() {
    imageCan.width = feed.naturalWidth;
    imageCan.height = feed.naturalHeight;
    imgctx.drawImage(feed,0,0,feed.width, feed.height);
  }, 100);
}
