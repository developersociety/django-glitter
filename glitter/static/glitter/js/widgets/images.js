(function($) {
    $(document).ready(function(){

        /**
         * Change height for all items in current row
         */
        function change_height(current_row, items_in_row, max_height, targets_ids){
            for(var k = current_row; k < (current_row + items_in_row); k++) {
                var current_item = k.toString();

                // Get object from targets_ids.
                obj = document.getElementById(targets_ids[k-1]);

                is_visible = obj.getAttribute('visible') == 'true';
                if (is_visible){
                    obj.setAttribute("style", "height: " + max_height + "px");
                } else {
                    obj.setAttribute("style", "display: none;");
                }
            }

        }

        /**
         *  Look for biggest height in a row and change curren row to it.
         */
        function match_height (items_in_row) {
            var grid = document.getElementById('image_grid');
                
            var grid_items_target = grid.getElementsByTagName('div');

            // Add visible div in to array for later looping.
            var targets_ids = Array();
            $(grid).children().each(function(){
                if ($(this).attr('visible') == 'true'){
                    targets_ids.push($(this).attr('id'));
                }
            });

            var target = document.querySelectorAll('.grid-item[visible="true"]');
            Array.prototype.forEach.call(target, function(element){
                element.removeAttribute('style');

            });
            var max_height = 0;
            for(var i = 1; i < targets_ids.length; i += items_in_row) {
                max_height = 0;
                current_row = i;
                var row_max = current_row ;
                for(var j = i; j < i+items_in_row; j++) {

                    if (j > targets_ids.length){
                        break;
                    }

                    var elem = j + current_row;
                    var elem_id = j.toString();

                    var item_height = document.getElementById(targets_ids[j - 1]).offsetHeight;

                    if (item_height > max_height) {
                        max_height = item_height;
                    }


                    // Check if there is reminded grids in row.
                    if (j > targets_ids.length - targets_ids.length % items_in_row){
                        reminder = targets_ids.length % items_in_row;
                        if (j == (current_row + (reminder - 1))) {
                            change_height(current_row, reminder, max_height, targets_ids);
                        }
                    } else {
                        if (j == (current_row + (items_in_row - 1))) {
                            change_height(current_row, items_in_row, max_height, targets_ids);
                        }
                    }

                }
            }
        }

        function check_window_size(){
            var window_size = window.innerWidth;
            if (window_size < 661) {
                match_height(2);
            } else if (window_size < 741 && window_size > 660) {
                match_height(3);
            } else if (window_size < 960 && window_size > 740) {
                match_height(4);
            } else {
                match_height(5);
            }
        }

        /**
         * Reveal images when when Broser is clicked.
         */
        function reveal_images(){
            $('.block-image-selector').show();

            $('.block-image-selector img').each(function(){
                var  image = new Image();
                var img = $(this)[0];
                $(img).load(function(){
                    $(this).parent().removeClass('spinner');
                });
                $(img).error(function(){
                    $(this).parent().removeClass('spinner');
                });
                img.src = $(this).attr('data-src');
            });


            check_window_size();

            var addEvent = function(object, type, callback) {
                if (object === null || typeof(object) == 'undefined') return;
                if (object.addEventListener) {
                    object.addEventListener(type, callback, false);
                } else if (object.attachEvent) {
                    object.attachEvent("on" + type, callback);
                } else {
                    object["on"+type] = callback;
                }
            };
            
            addEvent(window, "resize", function(event){
                var window_size = window.innerWidth;
                if (window_size < 661) {
                    match_height(2);
                } else if (window_size < 741 && window_size > 660) {
                    match_height(3);
                } else if (window_size < 960 && window_size > 740) {
                    match_height(4);
                } else {
                    match_height(5);
                }
            });
        }


        $('.browse-images').click(function(){
            reveal_images();
        });

        $('.clear-image').click(function(){
            $(this).parent().find('select').val('');
        });

        $('.block-image-selector img').click(function(){
            obj_id = $(this).attr('obj-id');
            $select_image = $(this).closest('.block-image-selector').parent().find('.image-related-field');
            $select_image.val(obj_id);
            $('.block-image-selector').hide();
        });

        $('.block-image-selector .close').click(function(){
            $(this).closest('.block-image-selector').hide();
        });

        /**
         * Display correct images when category is changed.
         */
        $('select#category').change(function(){
            $('.image-grid img').each(function(index, elem){
                $(elem).closest('.grid-item').show();
                $(elem).closest('.grid-item').attr('visible', 'true');
            });

            var category_id = $(this).val();
            if (category_id == "0"){
                $('.image-grid img').each(function(index, elem){
                     $(elem).closest('.grid-item').show();
                     $(elem).closest('.grid-item').attr('visible', 'true');
                });

            } else {
                $('.image-grid img[data-category-id!='+category_id+']').each(function(index, elem){
                     $(elem).closest('.grid-item').hide();
                     $(elem).closest('.grid-item').attr('visible', 'false');
                });
            }
            check_window_size();
        });
    });


})(django.jQuery);


