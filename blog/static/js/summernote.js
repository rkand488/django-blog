(function($) {
    $(document).ready(function() {
        if ($('#id_text').length > 0) {
            $('#id_text').summernote({
                placeholder: 'Write here...',
                height: 300
            });
        }
    });
})(jQuery);