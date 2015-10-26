
$(document).ready(function () {
    // script para menu acordeon
    $('nav > ul > li > a').on('click', function() {
        $(this).removeAttr('href');
        var element = $(this).parent('li');             // Busca de forma acendente al padre del elemento 'li' 
                                                        // desde el elemento de '#cssmenu li > a' donde se dio el click  (primer lista )
        //alert( element.text() );
        
        if ( element.hasClass('open') ) {               // La clase 'Open' reliza la funcion de una bandera boleana
            element.removeClass('open');                // Borra clase 'open' del objeto elemento.
            element.find('ul').slideUp()                // busca 'ul' proxima y la muestra desde el element'
        }else {
            element.addClass('open');                         // Agrega la clase 'open' del objeto elemento.
            element.children('ul').slideDown();               // muestra los hijos 'li' del elemento 'ul' del objeto elemento
            element.siblings('li').children('ul').slideUp();  // oculta todos los hermanos 'li' hijose de 'ul' del objeto elemento
            element.siblings('li').removeClass('open');       // Remueve la clase 'open' de todos los hermanos de 'li' del objeto elemento
        }
    });   
});