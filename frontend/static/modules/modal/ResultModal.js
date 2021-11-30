/** @author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM **/
/** Opens a result modal, visualizing the result of the bone density calculation **/
export function ResultModal(result) {
    document.getElementById("abmd-mean-cell").innerText = result["abmd_mean"];
    document.getElementById("abmd-std-cell").innerText = result["abmd_std"];
    const abmdMin = parseFloat(result["abmd_min"]);
    const abmdMax = parseFloat(result["abmd_max"]);
    const positionXElement = document.getElementById("result-modal-position-x");
    const positionYElement = document.getElementById("result-modal-position-y");
    const positionValueElement = document.getElementById("result-modal-position-value");

    this.open = () => {
        const modal = new bootstrap.Modal(document.getElementById("result-modal"));
        modal.show();
        return Promise.resolve(this);
    }

    /** Displays image information at the modal page. **/
    this.updateImageData = (imageData) => {
        positionXElement.innerHTML = `X: ${imageData.x}`;
        positionYElement.innerHTML = `Y: ${imageData.y}`;
        positionValueElement.innerHTML = `Value: ${reverseNormalisation(imageData.value)}`;
    }

    const reverseNormalisation = (value) => {
        const result = (value+ abmdMin) * ((abmdMax) / 255) ;
        return result.toFixed(2);
    }

    return this;
}