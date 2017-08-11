export function download(src) {
 var $a = document.createElement('a');
        $a.setAttribute("href", src);
        $a.setAttribute("download", "");
        var evObj = document.createEvent('MouseEvents');
        evObj.initEvent('click', true, false);
        $a.dispatchEvent(evObj);
}
