// Este archivo servira para centrar todo el body de la plantilla login.html agregando la clase textcenter 


//esta funcion servira para que las lineas de arriba se carguen cuando el documento login.html se haya cargado 
(function(){
    const body=document.querySelector("body");// se gurdara en una constante el selector atravez de nombre de etiquetas
    body.classList.add("text-center");//agregare la clase text-center a body
})();