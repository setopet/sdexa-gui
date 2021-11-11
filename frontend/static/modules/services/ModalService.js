export function ModalService() {
    'use strict';

    this.openFullscreen = (title, onFinish, onAbort) => {
        const modal = new bootstrap.Modal(document.getElementById("fullscreen-modal"));
        document.getElementById("fullscreen-modal-title").innerHTML = title;
        document.getElementById("fullscreen-modal-ok-button").onclick = onFinish;
        document.getElementById("fullscreen-modal-close-button").onclick = onAbort;
        document.getElementById("fullscreen-modal-close-button-top").onclick = onAbort;
        modal.show();
        return Promise.resolve(this);
    }

    return this;
}