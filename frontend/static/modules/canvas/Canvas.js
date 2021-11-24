/** @author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM **/
/** Draws an image on the canvas and adapts its size. **/
export function Canvas(id, minimumCanvasSize) {
    this.canvas = document.getElementById(id);

    const adaptSize = element => {
        if(minimumCanvasSize && element.width < minimumCanvasSize) {
                this.width = minimumCanvasSize;
                this.canvas.width = minimumCanvasSize;
        } else {
            this.width = element.width;
            this.canvas.width = element.width;
        }

        if (minimumCanvasSize && element.height < minimumCanvasSize) {
            this.height = minimumCanvasSize;
            this.canvas.height = minimumCanvasSize;
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
                adaptSize(element);
                context.drawImage(event.target, 0, 0);
                resolve(this);
            };
        });
    }
 
    return this; 
} 