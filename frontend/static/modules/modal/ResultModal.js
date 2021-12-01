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

    /** Displays aBMD value of the mouse position at the modal footer. **/
    this.updateImageData = (imageData) => {
        positionXElement.innerText = `X: ${imageData.x.toString().padStart(3, "0")}`;
        positionYElement.innerText = `Y: ${imageData.y.toString().padStart(3, "0")}`;
        const value = reverseNormalisation(imageData.value);
        positionValueElement.innerText = `Value: ${ value < 0 ? "0.00" : value}`;
    }

    /** Displays aBMD mean of the selected segment at the modal footer, if present **/
    this.updateSegmentationData = (segmentation) => {
        const element = document.getElementById("result-modal-segment-mean");
        if (segmentation.length) {
            const mean = segmentation.map(x => x.getValue()).reduce((sum, value) => sum+value)
                /segmentation.length;
            element.innerText = `Segment aBMD: ${reverseNormalisation(mean)}`;
        }
        else {
            element.innerText = "";
        }
    }

    /** Reverses the normalisation of the jpeg image to the original aBMD value. **/
    const reverseNormalisation = (value) => {
        const result = (value+ abmdMin) * ((abmdMax) / 255) ;
        return result.toFixed(2);
    }

    return this;
}