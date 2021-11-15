/** Opens modal dialogs **/
export function ModalService() {
    'use strict';

    /** Opens a modal dialog and appends callbacks to the buttons. **/
    this.open = (title, onFinish, onAbort, onWindowChange) => {
        const modal = new bootstrap.Modal(document.getElementById("modal"));
        document.getElementById("modal-title").innerHTML = title;
        document.getElementById("modal-ok-button").onclick = onFinish;
        document.getElementById("modal-close-button").onclick = onAbort;
        document.getElementById("modal-close-button-top").onclick = onAbort;
        document.getElementById("modal-window-button").onclick = () => {
            const min = document.getElementById("modal-window-min").value;
            const max = document.getElementById("modal-window-max").value;
            onWindowChange({ min: min, max: max });
        }
        modal.show();
        return Promise.resolve(this);
    }

    return this;
}