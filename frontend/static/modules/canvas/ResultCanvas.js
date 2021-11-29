/** @author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM **/
import {Canvas} from "./Canvas.js";

export function ResultCanvas() {
    Canvas.call(this, "result-modal-canvas");
    this.watchMouseHover = (onHover) => {
        this.canvas.onmousemove = event => {
            const context = this.canvas.getContext("2d");
            const x = event.offsetX;
            const y = event.offsetY;
            const imageData = context.getImageData(x, y, 1, 1).data;
            onHover({
                x: x,
                y: y,
                value: imageData[0]
            });
        }
    }

    return this;
}