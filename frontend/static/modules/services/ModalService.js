/** Opens modal dialogs **/
export function ModalService() {
    this.open = (title, callbacks) => {
        setTitle(title);
        appendCallbacks(
            callbacks.onFinish,
            callbacks.onAbort,
            callbacks.onWindowChange,
            callbacks.onSelectionSizeChange
        );
        return openModal();
    }

    this.defaultSelectionSizeFields = (valueX, valueY) => {
        document.getElementById("modal-selection-x").value = valueX;
        document.getElementById("modal-selection-y").value = valueY;
    }

    this.defaultWindowFields = (valueMin, valueMax) => {
        document.getElementById("modal-window-min").value = valueMin;
        document.getElementById("modal-window-max").value = valueMax;
    }


    const appendCallbacks = (onFinish, onAbort, onWindowChange, onSelectionSizeChange) => {
        document.getElementById("modal-ok-button").onclick = onFinish;
        document.getElementById("modal-close-button").onclick = onAbort;
        document.getElementById("modal-close-button-top").onclick = onAbort;
        document.getElementById("modal-window-button").onclick = () => {
            const min = document.getElementById("modal-window-min").value;
            const max = document.getElementById("modal-window-max").value;
            onWindowChange(min, max);
        }
        if(onSelectionSizeChange) {
            document.getElementById("modal-selection-size-button").onclick = () => {
                const sizeX = document.getElementById("modal-selection-x").value;
                const sizeY = document.getElementById("modal-selection-y").value;
                onSelectionSizeChange(sizeX, sizeY);
            }
        } else {
            disableSelectionSizeFields();
        }
    }

    const disableSelectionSizeFields = () => {
        document.getElementById("modal-selection-x").disabled = true;
        document.getElementById("modal-selection-y").disabled = true;
        document.getElementById("modal-selection-size-button").disabled = true;
    }

    const setTitle = (title) => {
        document.getElementById("modal-title").innerHTML = title;
    }

    const openModal = () => {
        const modal = new bootstrap.Modal(document.getElementById("modal"));
        modal.show();
        return Promise.resolve(this);
    }

    return this;
}