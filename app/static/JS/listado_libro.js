//esta funcion servira para que las lineas de arriba se carguen cuando el documento login.html se haya cargado 
(function () {
    const btnsComprarLibro = document.querySelectorAll('.btnComprarLibro');// Esta varible constante hara la seleccion de todos los botones atravez del metodo document.querySelectorAll que nos permite seleccionar todos los elementos de la clase que declaramos btnComprarLibro en la plantilla listado_libros.html la cual se le pasa como argumento
    let isbnLibroSeleccionado = null;
    const csrf_token = document.querySelector("[name='csrf-token']").value;

    //Se recorrera el conjunto de botones que se han capturado mediante un forEach de esta manera agrear a cada boton un evento de escucha que es el btn.addEventListener('click', function(){}) donde se le pasa el evento click y una funcion anonima confirmarCompra() para cada uno de los botones para despues llamar una funcion confirmarCompra() 
    btnsComprarLibro.forEach((btn) => {
        btn.addEventListener('click', function () {
            isbnLibroSeleccionado = this.id;
            confirmarCompra();
        })
    })

    //En esta funcion haremos uso de la FetchAPI que es una funcionalidad de javascript para poder hacer el consumo de APIs atravez de Javascript puro sin librerias o frameworks solamente utilizando javascript, Ademas usaremos dos metodo async y await que nos permiten controlar el flujo de ejecucion en procesamientos asincronos
    const confirmarCompra = () => {
        Swal.fire({
            title: "¿Confirmar la compra del libro seleccionado ?",
            inputAttributes: {
                autocapitalize: 'off'
            },
            showCancelButton: true,
            confirmButtonText: 'Comprar',
            showLoaderOnConfirm: true,
            preConfirm: async () => {
                console.log(window.origin);
                //return await fetch('http://127.0.0.1:5000/comprarLibro', {
                return await fetch(`${window.origin}/comprarLibro`, {
                    method: 'POST',
                    mode: 'same-origin',
                    credentials: 'same-origin',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-TOKEN': csrf_token//Se envia el token en la peticion del libro 
                    },
                    body: JSON.stringify({//Se envia como cuerpo de la peticion el isbn del libro
                        'isbn': isbnLibroSeleccionado
                    })
                }).then(response => {
                    if (!response.ok) {
                        notificacionSwal('Error', response.statusText, 'error', 'Cerrar');
                    }
                    return response.json();
                }).then(data => {
                    if (data.exito){
                        notificacionSwal('!Exito ¡', 'Libro comprado', 'success', '!Aceptar¡');
                    } else {
                        notificacionSwal('!Alerta ¡', data.mensaje, 'Warning', 'OK');
                    }
                }).catch(error => {
                    notificacionSwal('Error', error, 'error', 'Cerrar');
                });
            },
            allowOutsideClick: () => false,
            allowEscapeKey: () => false
        });
    };
})();