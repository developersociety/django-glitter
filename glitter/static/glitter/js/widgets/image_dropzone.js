$(document).ready(function(){
  Dropzone.autoDiscover = false;
  var glitterDropzone = new Dropzone("form", {
      url: DROP_IMAGE_URL,
      maxFiles: 1,
      uploadMultiple: false,
      autoProcessQueue: true,
      previewsContainer: '.dropzonePreview',
      previewTemplate: '<div class="img-preview"></div>',
      acceptedFiles: ".jpeg,.jpg,.png,.gif",
      thumbnailHeight: 300,
      // This removes any wrong mime type file and displays the error.
      error: function(file, message) {
          this.removeFile(file);
          $('form').find('.errornote').remove();
          // Do not display message if the max file reached we just replace it with a new one.
          if (message != this.options.dictMaxFilesExceeded){
              $('form').prepend('<p class="errornote">'+ message +'</p>');
          }
      },
      init: function() {
        this.on('success', function(file, responseText){
            $('form').find('.errornote').remove();
            $('#id_image').append($('<option>', {
                value: responseText.image_id,
                text: responseText.filename,
            }));
            $('#id_image option[value='+ responseText.image_id +']').prop('selected', true);
        });

        this.on('thumbnail', function(file, dataUrl){
            file.previewElement = Dropzone.createElement(this.options.previewTemplate);
            $(this.options.previewsContainer).html('<img src="'+ dataUrl +'" />');
        });

        this.on('addedfile', function(file){
            if (this.files.length > 1) {
                this.removeFile(this.files[0]);
            }
        });

      },
  });
});
