document.querySelectorAll('.wysiwyg').forEach(item => {
    CKEDITOR.replace(item, {
        filebrowserBrowseUrl: '/admin/check-file',
        filebrowserImageUploadUrl: '/admin/upload-image'
    });
});