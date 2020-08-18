$(function () {
    $('#delete').submit(function () {
        if (!confirm('削除しますか')) {
            return false;
        }
    });
});