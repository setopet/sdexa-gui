export function ModalService() {
    this.openFullscreen = (modalName) => {
        const modal = new bootstrap.Modal(document.getElementById(modalName));
        modal.show();
        return modal;
    }

    return this;
}