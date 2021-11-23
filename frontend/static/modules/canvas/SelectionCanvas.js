import {Canvas} from "./Canvas.js";

/** Draws a rectangle representing the selected area when the user clicks at the canvas. **/
export function SelectionCanvas(image, selectionSizeX, selectionSizeY) {
    Canvas.call(this, "selection-modal-canvas", 530);  // Inheritance from Canvas

    this.selectionCanvas = document.createElement('canvas');
    this.image = image;
    this.lineWidth = 6; // take an even number
    this.selectionSizeX = selectionSizeX;
    this.selectionSizeY = selectionSizeY;
    this.posX = 0;
    this.posY = 0;

    this.updateImage = blob => {
        this.image = blob;
        return redraw();
    }

    this.updateSelectionSize = (sizeX, sizeY) => {
        this.selectionSizeX = sizeX;
        this.selectionSizeY = sizeY;
        return redraw();
    }

    this.canvas.onmousedown = event => {
        this.posX = event.offsetX;
        this.posY = event.offsetY;
        return redraw();
    }

    const drawRectangle = (width, height, posX, posY) => {
        const spacing = this.lineWidth/2;
        const context = this.canvas.getContext("2d");
        const rectangle = this.selectionCanvas.getContext("2d");
        rectangle.beginPath();
        rectangle.lineWidth = this.lineWidth
        rectangle.strokeStyle = 'orange';
        rectangle.rect(posX+spacing, posY+spacing, width-this.lineWidth, height-this.lineWidth);
        rectangle.stroke();
        context.drawImage(this.selectionCanvas, 0, 0);
        return Promise.resolve(this);
    }

    const erase = () => {
        const context2 = this.selectionCanvas.getContext("2d");
        context2.clearRect(0, 0, this.width, this.height);
        context2.drawImage(this.selectionCanvas, 0, 0);
        const context = this.canvas.getContext("2d");
        context.clearRect(0, 0, this.width, this.height);
        context.drawImage(this.canvas, 0, 0);
        return Promise.resolve(this);
    }

    const redraw = () => {
        return erase()
            .then(() => this.drawImage(this.image))
            .then(() => drawRectangle(this.selectionSizeX, this.selectionSizeY, this.posX, this.posY))
    };

    this.init = () => {
        return this.drawImage(this.image).then(() => {
            this.selectionCanvas.width = this.width;
            this.selectionCanvas.height = this.height;
            return drawRectangle(this.selectionSizeX, this.selectionSizeY, this.posX, this.posY);
            }
        );
    }

    return this;
}