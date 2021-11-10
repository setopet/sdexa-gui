export function ModalService() {
    'use strict';

    this.openFullscreen = (title, onFinish) => {
        const modal = new bootstrap.Modal(document.getElementById("fullscreen-modal"));
        document.getElementById("fullscreen-modal-title").innerHTML = title;
        document.getElementById("fullscreen-modal-ok-button").onclick = onFinish;
        modal.show();
        return Promise.resolve(this);
    }

    return this;
}