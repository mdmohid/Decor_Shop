document.addEventListener("DOMContentLoaded", function () {

/*
open modal
*/

const modalLinks = document.querySelectorAll(
    ".footer-modal-link"
);

modalLinks.forEach(function (link) {

    link.addEventListener("click", function (event) {

        event.preventDefault();

        const modalId = link.dataset.modal;
        const modal = document.getElementById(modalId);

        if (modal) {
            modal.classList.add("is-active");
        }

    });

});


/*
close modal button
*/

const closeButtons = document.querySelectorAll(
    "[data-close-modal]"
);

closeButtons.forEach(function (button) {

    button.addEventListener("click", function () {

        const modalId = button.dataset.closeModal;
        const modal = document.getElementById(modalId);

        if (modal) {
            modal.classList.remove("is-active");
        }

    });

});


/*
close when clicking background
*/

const modalBackgrounds = document.querySelectorAll(
    ".decor-modal .modal-background"
);

modalBackgrounds.forEach(function (background) {

    background.addEventListener("click", function () {

        const modal = background.closest(".modal");

        if (modal) {
            modal.classList.remove("is-active");
        }

    });

});


/*
esc key
*/

document.addEventListener("keydown", function (event) {

    if (event.key === "Escape") {

        const activeModal = document.querySelector(
            ".decor-modal.is-active"
        );

        if (activeModal) {
            activeModal.classList.remove("is-active");
        }

    }

});
;
});
