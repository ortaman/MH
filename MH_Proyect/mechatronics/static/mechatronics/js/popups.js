
$(document).ready(function() {
    // Script para ventana emergente popup para confirmar borrar equipo
    $('#js_popup').on('click', function() {
        $(this).removeAttr('href');
        $('.overlay-container1').fadeIn(function() {
            window.setTimeout(function() {
                $('.window-container1').addClass('window-container-visible1');
            }, 100);
        });
    });

    $('.close').click(function() {
        $('.overlay-container1').fadeOut().end().find('.window-container1').removeClass('window-container-visible1');
    });
});