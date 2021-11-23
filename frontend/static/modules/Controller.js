import {baseUrl} from "./config.js";
import {ModalCanvas} from "./ModalCanvas.js";
import {LoadingAnimation} from "./LoadingAnimation.js";

/** Central control object, which is visible in the templates. **/
export function Controller(httpService, modalService, fileService, alertService) {
    const vm = this;

    vm.deleteImage = (route) => {
        httpService.delete(route)
            .then(reloadPage)
            .catch(alertService.error);
    }

    vm.switchImageView = (route) => {
        httpService.put(baseUrl + route)
            .then(reloadPage)
            .catch(alertService.error);
    }

    vm.downloadImage = (route, fileName) => {
        httpService
            .downloadFile(baseUrl + route, fileName)
            .catch(alertService.error);
    }

    vm.uploadScatter = (file) => {
        const animation = new LoadingAnimation("scatter-input-label");
        httpService
            .uploadFile(file, baseUrl + "surview/scatter")
            .then(() => getImage("surview"))
            .then(blob => initModalCanvas(blob, 50, 50))
            .then(animation.stop)
            .then(() => {
                modalService.defaultWindowFields("0", "2000");
                modalService.defaultSelectionSizeFields("50", "50");
                return modalService.open("Hello", {
                    onFinish: () => {
                        const region = {
                            posX: vm.modalCanvas.posX,
                            posY: vm.modalCanvas.posY,
                            dx: vm.modalCanvas.selectionSizeX,
                            dy: vm.modalCanvas.selectionSizeY
                        }
                        return httpService.put("surview/sdexa/soft-tissue-region", region)
                            .then(reloadPage);
                    },
                    onAbort: reloadPage,
                    onWindowChange: null, // TODO: putImage lädt danach das full image
                    onSelectionSizeChange: vm.modalCanvas.updateSelectionSize
                });
            })
            .catch(error => {
                animation.stop();
                alertService.error(error);
            });
    }

    vm.clickCalculate = () => {
        httpService.put("/surview/sdexa/calculation");
    }

    const uploadImage = (file, imageName, modalTitle) => {
        const animation = new LoadingAnimation(imageName + "-spinner");
        httpService.uploadFile(file, baseUrl + imageName)
            .then(() => getImage(imageName + "/full"))
            .then(blob => initModalCanvas(blob, 512, 512))
            .then(animation.stop)
            .then(() => openSelectionModal(imageName, modalTitle))
            .catch(error => {
                animation.stop();
                alertService.error(error);
            });
    }

    const putImagePosition = (url) => {
        const position = { 'posX': vm.modalCanvas.posX, 'posY': vm.modalCanvas.posY };
        httpService.put(url, position)
            .then(reloadPage)
            .catch(alertService.error);
    }

    const putImageWindow = (route) => (windowMin, windowMax) => {
        httpService.put(baseUrl + route + "/window", { min: windowMin, max: windowMax })
            .then(() => getImage(route + "/full"))
            .then(vm.modalCanvas.updateImage)
    }

    const openSelectionModal = (imageName, title) => {
        modalService.defaultSelectionSizeFields("512", "512");
        modalService.defaultWindowFields("0", "2000");
        return modalService.open(title, {
            onFinish: () => putImagePosition(baseUrl + imageName + "/position"),
            onAbort: () => vm.deleteImage(imageName),
            onWindowChange: putImageWindow(imageName)
        });
    }

    const initModalCanvas = (blob, selectionSizeX, selectionSizeY) =>  {
        vm.modalCanvas = new ModalCanvas(blob, selectionSizeX, selectionSizeY);
        return vm.modalCanvas.init();
    }

    const getImage = (route) => {
        return httpService.get(baseUrl + route)
            .then(response => response.blob())
    }

    const reloadPage = () => {
        location.href = '/';
        return Promise.resolve(this);
    }

    const init = () => {
        const surviewUploadCallback = file => uploadImage(file, "surview",
            "Move the rectangle by clicking on the surview image to select the area for segmenation. " +
            "Click the OK button when you are finished.");
        const projectionUploadCallback = file => uploadImage(file, "projection",
            "Move the rectangle by clicking on the projection image to select the area for registration. " +
            "Click the OK button when you are finished.");
        fileService.watchFileInput("surview-input", surviewUploadCallback);
        fileService.watchFileDrop("surview-drop", surviewUploadCallback);
        fileService.watchFileInput("projection-input", projectionUploadCallback);
        fileService.watchFileDrop("projection-drop", projectionUploadCallback);
        fileService.watchFileInput("scatter-input", vm.uploadScatter);
    }

    init();

    return vm;
}