
var path = String(location.pathname) ;
var ret = path.replace(/[^0-9]{1}/g, '');
var ret1 = path.replace(/\/share_calendar\/look_pic\/\d*/g, '');
var first = ret1.replace(/\d\/$/g,'')
var first2 = first.replace(/[^0-9]{1}/g, '');
var end = ret1.replace(/\/\d\//g,'');
var end2 = end.replace(/[^0-9]{1}/g, '');

var num3 = parseFloat(first2);
var num4 = parseFloat(end2);
var index_num = num3*4+num4+1;
var str_index_num = String(index_num);
var elem = document.getElementById(str_index_num);

console.log(ret);
console.log(ret1);
console.log(first2);
console.log(end2);
console.log(index_num);



elem.scrollIntoView();