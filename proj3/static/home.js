window.addEventListener('scroll', function () {
    const head=document.querySelector('.header');
    head.classList.toggle('sticky',window.scrollY>0);

    
    const bars=[
        document.querySelector('.head .headImg'),
        document.querySelector('.head #title0'),
        document.querySelector('.head .btn'),
        document.querySelector('.head p')
    ];
    for(let i=0;i<4;i++) {
        var r=.25;
        switch(i) {
            case 0: r=.1;  break;
            case 1: r=.25; break;
            case 2: r=.26; break;
            case 3: r=.27; default: break;
        }
        var rate=window.scrollY*r;
        
        if(i==0) {
            bars[i].style.opacity=1/rate*15; } 
        bars[i].style.transform='translate3d(0px,'+rate+'px,0px)'; 
    }
    
});/*
window.onload= function() {
    console.log("reload");
    let img=document.querySelector(".headIm");
    let dir="{{ url_for('static',filename='images/";
    let imgAr=[
         "{{ url_for('static',filename='images/f1.jpg') }}"
        ,"{{ url_for('static',filename='images/f2.png') }}"
        ,"{{ url_for('static',filename='images/f3.png') }}"
        ,"{{ url_for('static',filename='images/f4.png') }}"
        ,"{{ url_for('static',filename='images/f5.png') }}"];
    let index=Math.floor(Math.random()*imgAr.length);
    console.log(index);
    img.src=String(imgAr[index]);
};*/
const pos=document.documentElement;
    pos.addEventListener('mousemove',e=>{
        pos.style.setProperty('--x',e.clientX+"px");
        pos.style.setProperty('--y',e.clientY+"px");
    });

let scr3=0; 
const facilityCards=[
    document.querySelector('.training .card .cardRow  #fac1'),
    document.querySelector('.training .card .cardRow  #fac2'),
    document.querySelector('.training .card .cardRow  #fac3'),
    document.querySelector('.training .card .cardRow  #fac4'),
    document.querySelector('.training .card .cardRow  #fac5'),
    document.querySelector('.training .card .cardRow  #fac6'),
    document.querySelector('.training .card .cardRow  #fac7')
]; 

let inter=setInterval(()=>{
    
    let width=document.querySelector('.training .card .cardRow  #fac1').offsetWidth;
    element=document.querySelector('.training .card .cardRow');
    element.scroll({
        top: 0,
        left: width*(scr3++),
        behavior: 'smooth'
      });
    if(scr3==2) scr3=0;
},3000);
/*  scroll element on click
document.querySelector('.training .card .cardRow').addEventListener('click',()=>{
    /*
    console.log(document.querySelector('.training .card .cardRow  #fac1').offsetWidth);
    let width=document.querySelector('.training .card .cardRow  #fac1').offsetWidth;
    element=document.querySelector('.training .card .cardRow');
    element.scroll({
        top: 100,
        left: width*(i++),
        behavior: 'smooth'
      });
    if(i==8) i=0;
});*/

var login=document.querySelector('.header li .active');
var loginpg=document.querySelector('.login');
login.addEventListener('click', function(){
    var txt=login.textContent;
    console.log(txt.localeCompare("Dashboard"));
    if(txt.localeCompare("Dashboard")==0) {
        window.location.href="/dash";
        console.log('redirect');
    }
    else  {
        loginpg.classList.add('switchon');  
    }
});
loginpg.addEventListener('click',function(e){
    if(e.target.classList.contains('login'))
    loginpg.classList.remove('switchon');
});


function axe() {
    document.querySelector('.anim').classList.add('load');
}