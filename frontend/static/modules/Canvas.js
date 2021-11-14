/** Draws an image on the canvas and adapts its size. **/
export function Canvas(id) {
    'use strict';
    this.canvas = document.getElementById(id);
    const minSize = 530;

    const setSize = element => {
        if(element.width < minSize) {
                this.width = minSize;
                this.canvas.width = minSize;
        } else {
            this.width = element.width;
            this.canvas.width = element.width;
        }

        if (element.height < minSize) {
            this.height = minSize;
            this.canvas.height = minSize;
        } else {
            this.height = element.height;
            this.canvas.height = element.height;
        }
    }

    this.drawImage = image => {
        const element = new Image();
        element.src = URL.createObjectURL(image);
        const context = this.canvas.getContext("2d");
        return new Promise(resolve => {
            element.onload = event => {
                setSize(element);
                context.drawImage(event.target, 0, 0);
                resolve(this);
            };
        });
    }

    return this;
}


