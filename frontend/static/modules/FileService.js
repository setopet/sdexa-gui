export function FileService() {
    'use strict';

    this.downloadFile = (url, fileName) => {
        // Credits to https://stackoverflow.com/questions/32545632/how-can-i-download-a-file-using-window-fetch
        fetch(url, { method: 'GET'})
            .then(response => response.blob())
            .then(blob => {
                const link = document.createElement('a');
                link.href = window.URL.createObjectURL(blob);
                link.download = fileName;
                document.body.appendChild(link);
                link.click();
                link.remove();
            });
    }

    this.uploadFile = (file, route) => {
        const data = new FormData();
        data.append('file', file);
        return fetch(route, {
            method: 'POST',
            body: data
        });
    }

    return this;
}