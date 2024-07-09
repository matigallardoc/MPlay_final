$(document).ready(function() {
    // Consumir la API
    $.get('https://api.escuelajs.co/api/v1/products', function(data) {
        // Limpiar el contenedor de productos
        $('#fila-ropa').empty();
        
        // Iniciar una fila para los productos
        var fila = '<div class="row">';
        
        // Variable para contar los productos procesados
        var count = 0;

        // Obtener la cantidad total de productos
        var totalProducts = data.length;

        // Definir cuántos productos omitir al inicio y al final
        var skipStart = 6;
        var skipEnd = 3;

        // Iterar sobre cada producto en los datos recibidos
        $.each(data, function(i, item) {
            // Saltar los primeros productos que se deben omitir
            if (count < skipStart) {
                count++;
                return true; // Continuar con el siguiente producto
            }

            // Saltar los últimos productos que se deben omitir
            if (count >= totalProducts - skipEnd) {
                count++;
                return true; // Continuar con el siguiente producto
            }
            
            // Crear un nuevo elemento de tarjeta para cada producto
            var card = `
                <div class="col-xs-12 col-sm-6 col-md-6 col-lg-4 col-xl-3">
                    <div class="card pt-2" style="width: 18rem;">
                        <img src="${item.images}" class="card-img-top" alt="${item.title}">
                        <div class="card-body">
                            <h5 class="card-title">${item.title}</h5>
                            <p class="card-text">
                                <span class="disponible">${item.category.name}</span><br>
                                ${item.description}
                            </p>
                            <a href="https://www.amazon.com/s?k=${item.title}" class="btn btn-primary" target="_blank">Buscar en Amazon</a>
                        </div>
                    </div>
                </div>
            `;
            
            // Agregar la tarjeta al contenedor de productos
            fila += card;
            count++;
        });
        
        // Cerrar la fila
        fila += '</div>';
        
        // Agregar la fila al contenedor de ropa
        $('#fila-ropa').append(fila);
    });
});

// $(document).ready(function() {
//     // Consumir la API
//     $.get('https://api.escuelajs.co/api/v1/products', function(data) {
//         // Limpiar el contenedor de productos
//         $('#fila-ropa').empty();
        
//         // Iniciar una fila para los productos
//         var fila = '<div class="row">';
        
//         // Iterar sobre cada producto en los datos recibidos
//         $.each(data, function(i, item) {
//             // Crear un nuevo elemento de tarjeta para cada producto
//             var card = `
//                 <div class="col-xs-12 col-sm-6 col-md-6 col-lg-4 col-xl-3">
//                     <div class="card pt-2" style="width: 18rem;">
//                         <img src="${item.images}" class="card-img-top" alt="${item.title}">
//                         <div class="card-body">
//                             <h5 class="card-title">${item.title}</h5>
//                             <p class="card-text">
//                                 <span class="disponible">${item.category.name}</span><br>
//                                 ${item.description}
//                             </p>
//                             <a href="https://www.amazon.com/s?k=${item.title}" class="btn btn-primary" target="_blank">Buscar en Amazon</a>
//                         </div>
//                     </div>
//                 </div>
//             `;
            
//             // Agregar la tarjeta al contenedor de productos
//             fila += card;
//         });
        
//         // Cerrar la fila
//         fila += '</div>';
        
//         // Agregar la fila al contenedor de ropa
//         $('#fila-ropa').append(fila);
//     });
// });


// <div class="col-12 col-sm-6 col-md-4 col-lg-3 mb-3">
//                     <div class="card text-center">
//                         <img src="${item.image}" class="card-img-top" alt="${item.title}" style="width: 100px; margin: auto;">
//                         <div class="card-body">
//                             <h5 class="card-title">${item.title}</h5>
//                             <h6>${item.category}</h6>
//                             <p class="card-text">${item.description}</p>
//                             <a href="https://www.amazon.com/s?k=${item.title}" class="btn btn-primary" target="_blank">Buscar en Amazon</a>
//                         </div>
//                     </div>
//                 </div>
//                 --------------------------------