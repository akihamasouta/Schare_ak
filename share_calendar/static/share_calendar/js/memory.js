let mobile_today_memory_content_id = document.getElementById('mobile_today_memory_content'); 
let mobile_today_container = document.getElementById('mobile_today_container');

console.log('ok');
box01Width = mobile_today_memory_content_id.offsetWidth/3-10;

function changeBackColor(){
  let mobile_today_memory_content = document.getElementsByClassName('mobile_today_memory_content');    
  for(i=0;i<mobile_today_memory_content.length;i++){
    mobile_today_memory_content[i].style.height = box01Width + 'px';
  }
}
function mobile_today_container_1(){
  let mobile_today_container_1 = document.getElementsByClassName('mobile_today_container_1');    
  for(i=0;i<mobile_today_container_1.length;i++){
    mobile_today_container_1[i].style.height = box01Width + 'px';
  }
}
function mobile_today_container_2(){
  let mobile_today_container_2 = document.getElementsByClassName('mobile_today_container_2');    
  for(i=0;i<mobile_today_container_2.length;i++){
    mobile_today_container_2[i].style.height = box01Width + 'px';
  }
}
function mobile_today_container_3(){
  let mobile_today_container_3 = document.getElementsByClassName('mobile_today_container_3');    
  for(i=0;i<mobile_today_container_3.length;i++){
    mobile_today_container_3[i].style.height = box01Width + 'px';
  }
}
function changeBackColo(){
  let mobile_today_memory_content = document.getElementsByClassName('mobile_today_memory_content');    
  for(i=0;i<mobile_today_memory_content.length;i++){
    mobile_today_memory_content[i].style.backgroundColor = 'white';
  }
}

changeBackColor()
changeBackColo()




console.log(box01Width);



