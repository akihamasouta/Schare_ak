let mobile_today_memory_content_id = document.getElementById('pictures'); 

console.log('ok');
box01Width = mobile_today_memory_content_id.offsetWidth/4-10;

function changeBackColor(){
  let mobile_today_memory_content = document.getElementsByClassName('pictures');    
  for(i=0;i<mobile_today_memory_content.length;i++){
    mobile_today_memory_content[i].style.height = box01Width + 'px';
  }
}


changeBackColor()




console.log(box01Width);