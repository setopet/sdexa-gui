/** Opens modal dialogs **/
export function ModalService() {
    'use strict';

    /** Opens a fullscreen modal dialog and appends callbacks to the buttons. **/
    this.openFullscreen = (title, onFinish, onAbort, onWindowChange) => {
        const modal = new bootstrap.Modal(document.getElementById("fullscreen-modal"));
        document.getElementById("fullscreen-modal-title").innerHTML = title;
        document.getElementById("fullscreen-modal-ok-button").onclick = onFinish;
        document.getElementById("fullscreen-modal-close-button").onclick = onAbort;
        document.getElementById("fullscreen-modal-close-button-top").onclick = onAbort;
        document.getElementById("fullscreen-modal-window-button").onclick = () => {
            const min = document.getElementById("fullscreen-modal-window-min").value;
            const max = document.getElementById("fullscreen-modal-window-max").value;
            onWindowChange({ min: min, max: max });
        }
        modal.show();
        return Promise.resolve(this);
    }

    return this;
}