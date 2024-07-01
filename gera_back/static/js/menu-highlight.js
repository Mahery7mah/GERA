// menu-highlight.js
$(document).ready(function () {
    // Récupérez l'URL de la page actuelle
    var currentUrl = window.location.pathname;

    // Ajoutez la classe "active" à l'élément de menu correspondant
    $('#sidebar-ul a').each(function () {
        var menuUrl = $(this).attr('href');

        if (currentUrl === menuUrl) {
            $(this).addClass('active');
            // Ajoutez la classe "show" pour empêcher la fermeture du sous-menu
            $(this).parents('.collapse').addClass('show');
        }
    });

    // Gérez l'ouverture et la fermeture des sous-menus au survol
    $('#sidebar-ul .nav-link[data-toggle="collapse"]').on('mouseenter', function () {
        var targetCollapse = $($(this).attr('href'));
        targetCollapse.addClass('show');

        // Fermez les autres sous-menus s'ils sont ouverts
        $('.collapse').not(targetCollapse).removeClass('show');
    });

    // Ajoutez une gestion du clic sur les liens de sous-menus
    $('#sidebar-ul .collapse a').on('click', function (e) {
        e.stopPropagation(); // Empêche la propagation du clic au parent (le lien de toggle)
    });
});