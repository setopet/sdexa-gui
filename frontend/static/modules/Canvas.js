export function Canvas(id) {
    'use strict';
    this.canvas = document.getElementById(id);

    const setSize = element => {
        if(element.width < 530) {
                this.width = 530;
                this.canvas.width = 530;
        } else {
            this.width = element.width;
            this.canvas.width = element.width;
        }

        if (element.height < 530) {
            this.height = 530;
            this.canvas.height = 530;
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


