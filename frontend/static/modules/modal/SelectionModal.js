export function SelectionModal(title, callbacks) {
    this.defaultSelectionSizeFields = (valueX, valueY) => {
        document.getElementById("modal-selection-x").value = valueX;
        document.getElementById("modal-selection-y").value = valueY;
    }

    this.defaultWindowFields = (valueMin, valueMax) => {
        document.getElementById("modal-window-min").value = valueMin;
        document.getElementById("modal-window-max").value = valueMax;
    }

    const appendCallbacks = (onFinish, onAbort, onWindowChange, onSelectionSizeChange) => {
        document.getElementById("selection-modal-ok-button").onclick = onFinish;
        document.getElementById("selection-modal-close-button").onclick = onAbort;
        document.getElementById("selection-modal-close-button-top").onclick = onAbort;
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
                configureSelectionSizeFields(false);
            }
        } else {
            configureSelectionSizeFields(true);
        }
    }

    const configureSelectionSizeFields = (deactivate) => {
        document.getElementById("modal-selection-x").disabled = deactivate;
        document.getElementById("modal-selection-y").disabled = deactivate;
        document.getElementById("modal-selection-size-button").disabled = deactivate;
    }

    const setTitle = (title) => {
        document.getElementById("selection-modal-title").innerHTML = title;
    }

    setTitle(title);
    appendCallbacks(
        callbacks.onFinish,
        callbacks.onAbort,
        callbacks.onWindowChange,
        callbacks.onSelectionSizeChange
    );

    this.open = () => {
        const modal = new bootstrap.Modal(document.getElementById("selection-modal"));
        modal.show();
        return Promise.resolve(this);
    }

    return this;
}