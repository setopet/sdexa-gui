import {Canvas} from "./Canvas.js";

export function SelectionCanvas(id, image) {
    Canvas.call(this, id); // Inheritance from Canvas

    this.selectionCanvas = document.createElement('canvas');
    this.image = image;
    this.lineWidth = 6;
    let posX = 0;
    let posY = 0;

    this.getX = () => posX;
    this.getY = () => posY;

    const drawRectangle = (width, height, posX, posY) => {
        const spacing = this.lineWidth/2;
        const context = this.canvas.getContext("2d");
        const rectangle = this.selectionCanvas.getContext("2d");
        rectangle.beginPath();
        rectangle.lineWidth = this.lineWidth
        rectangle.strokeStyle = 'red';
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
            .then(() => drawRectangle(512, 512, posX, posY))
    };

    this.canvas.onmousedown = event => {
        posX = event.offsetX;
        posY = event.offsetY;
        redraw();
    };

    this.init = () => {
        this.drawImage(this.image).then(() => {
            this.selectionCanvas.width = this.width;
            this.selectionCanvas.height = this.height;
            return drawRectangle(512, 512, posX, posY);
            }
        );
    }

    return this;
}