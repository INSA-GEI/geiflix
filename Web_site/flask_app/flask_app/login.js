
var logged=false;
let count = 0;


// Fonction de mise à 0 de log (variable de vérification de log)
function RAZ()
{
    sessionStorage.setItem("log",0);

}

// Fonction de validation du mot de passe
function validate()
{
    var username=document.getElementById("username").value;
    var password=document.getElementById("password").value;

    if(username=="INSA" && password=="Zilly")
    {
        sessionStorage.setItem("log",1);
        var div = document.getElementById("maDIV");
        div.style.display = "block";
        return false;
    }
    else
    {
        alert("login failed");
    }
}

// fonction permettant de vérifier si la personne s'est log avant d'acceder aux pages réservées
function test_log()
{
    if(sessionStorage.getItem("log")!=1)
    {
        alert("You are not login");
        window.location.href="index.html"
    }
}



function slideSuivante(){
 items = document.querySelectorAll('img');
 nbSlide = items.length;
 suivant = document.querySelector('.right');
 precedent = document.querySelector('.left');
    
    items[count].classList.remove('active');

    if(count < nbSlide - 1){
        count++;
    } else {
        count = 0;
    }

    items[count].classList.add('active');
    console.log(count);
    
}

function slidePrecedente(){
    items[count].classList.remove('active');

    if(count > 0){
        count--;
    } else {
        count = nbSlide - 1;
    }

    items[count].classList.add('active');
    // console.log(count);
    
}

function keyPress(e){
    console.log(e);
    
    if(e.keyCode === 37){
        slidePrecedente();
    } else if(e.keyCode === 39){
        slideSuivante();
    }
}
document.addEventListener('keydown', keyPress);
