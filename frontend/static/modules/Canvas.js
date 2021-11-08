export function Canvas(id) {
    this.canvas = document.getElementById(id);

    const setSize = element => {
        if(element.width < 512) {
                this.width = 512;
                this.canvas.width = 512;
        } else {
            this.width = element.width;
            this.canvas.width = element.width;
        }

        if (element.height < 512) {
            this.height = 512;
            this.canvas.height = 512;
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


