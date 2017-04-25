var lista = [];
lista[0] = "home";
lista[1] = 'curso';
lista[2] = 'professor';
lista[3] = 'disciplina';

function open(opc){
    for( i=0 ; i < 4; i++){
        a = document.getElementById(lista[i]);
        if (a.classList.contains('block')){
            console.log(a);
            a.classList.remove('block');
            a.classList.add('none');
        }
    }
    document.getElementById(opc).classList.remove('none');
    document.getElementById(opc).classList.add('block');
}

var currentBackground = 0;
var backgrounds = [];
backgrounds[0] = '/img/img01.png';
backgrounds[1] = '/img/img02.png';
backgrounds[2] = '/img/img03.png';
backgrounds[3] = '/img/img04.png';
backgrounds[4] = '/img/img05.png';

function changeBackground() {
    a = document.getElementById('#background');
    for( i=0 ; i < 5; i++){
        if (a.classList.contains('img-0' + i)){
            console.log(i);
            a.classList.remove('img-0' + i);
        }
    }
    currentBackground++;
    if(currentBackground > 4){
        currentBackground = 0;
    }
    a.classList.add("img-0"+currentBackground);
    setTimeout(changeBackground(), 2000);
}

$(document).ready(
    function() {
    setTimeout(changeBackground, 2000);        
});

function openMenu(){
    $("my_menu").document.display = "block";
}