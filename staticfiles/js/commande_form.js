document.addEventListener('DOMContentLoaded', function () {
    // Obtenir une référence au champ de sélection du produit et au champ du prix du produit
    const produitSelect = document.getElementById('id_lignecommande_set-0-produit');
    const prixProduitInput = document.getElementById('id_PrixProduit');

    // Écouter les changements dans le champ de sélection du produit
    produitSelect.addEventListener('change', function () {
        const selectedOption = produitSelect.options[produitSelect.selectedIndex];
        
        // Mettre à jour le champ du prix du produit avec la valeur sélectionnée
        prixProduitInput.value = selectedOption.dataset.prix;
    });
});