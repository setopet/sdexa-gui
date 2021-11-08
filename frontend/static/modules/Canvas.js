export function Canvas(id, width, height) {
    this.element = document.getElementById(id);
    this.width = width;
    this.height = height;
    this.element.width = this.width;
    this.element.height = this.height;

    this.drawImage = (blob) => {
        const image = new Image();
        const imageSrc = URL.createObjectURL(blob);
        const context = this.element.getContext("2d");
        image.src = imageSrc;
        return new Promise(resolve => {
            image.onload = event => {
                context.drawImage(event.target, 0, 0);
                resolve();
            };
        });
    }

    this.drawRectangle = (width, height, posX, posY) => {
        const lineWidth = 6;
        const context = this.element.getContext("2d");
        const selectionCanvas = document.createElement('canvas');
        selectionCanvas.width = this.width;
        selectionCanvas.height = this.height;
        const rectangle = selectionCanvas.getContext("2d");
        rectangle.beginPath();
        rectangle.lineWidth = lineWidth
        rectangle.strokeStyle = 'red';
        rectangle.rect(posX, posY, width, height);
        rectangle.stroke();
        context.drawImage(selectionCanvas, 0, 0);
        return Promise.resolve();
    }

    return this;
}


