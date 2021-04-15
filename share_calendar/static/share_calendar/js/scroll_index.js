var today = new Date();
var id_today = String(today.getMonth()+1) + "-" + String(today.getDate());
var element = document.getElementById(id_today);

// 上端に来るようにスクロールさせたい
element.scrollIntoView(true);
window.scrollTo(0, 0);

