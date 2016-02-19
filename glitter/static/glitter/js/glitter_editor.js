var GlitterEditor = window.GlitterEditor || {};


(function($) {
    "use strict";

    // Page tabs/panes, which can also deactivate
    $.fn.tabs = function() {
        var active_tab,
            active_pane,
            tabs = $(this).find(".glitter-tab"),
            active_class = "glitter-active";

        tabs.on("click", function() {
            var target_id = $(this).data("target");

            if (active_tab !== undefined) {
                active_tab.removeClass(active_class);
                active_pane.removeClass(active_class);
            }

            if ($(this).is(active_tab)) {
                $(this).trigger("tabs.beforehidden", [active_tab, active_pane]);

                $(target_id).parent().removeClass(active_class);

                active_tab = undefined;
                active_pane = undefined;
            } else {
                $(this).addClass(active_class);
                $(target_id).addClass(active_class);
                $(target_id).parent().addClass(active_class);

                active_tab = $(this);
                active_pane = $(target_id);

                $(this).trigger("tabs.activate", [active_tab, active_pane]);
            }
        });

        return this;
    };
}(jQuery));

/* Put jQuery in our own namespace */
/*global jQuery:true */
GlitterEditor.jQuery = jQuery.noConflict(true);

(function(GlitterEditor) {
    "use strict";

    // Get the local namespaced utils
    var $ = GlitterEditor.jQuery;

    var csrf_token,
        add_block_url;

    GlitterEditor.store_csrf_token = function(token) {
        csrf_token = token;
    };

    GlitterEditor.set_add_block_url = function(url) {
        add_block_url = url;
    };


    GlitterEditor.update_column = function(column_name, column_content, close_popup) {
        $("#glitter_column_"+column_name).replaceWith(column_content);

        if (close_popup !== undefined) {
             GlitterEditor.close_popup();
        }
    };


    GlitterEditor.close_popup = function() {
        $("#glitter-lightbox").remove();
        $(document.body).removeClass("glitter-lightbox-active");
    };


    GlitterEditor.redirect_page = function(url) {
        window.location = url;
    };


    $().ready(function() {
        var cookie_name = "glitter_sidebar",
            cookie_options = {
                path: "/",
                expires: 1
            };


        // Version number pagination
        var version_per_page = 10,
            version_container = $("#glitter-versionlist"),
            version_list = version_container.find("tr"),
            version_viewing = version_list.filter(".glitter-current"),
            version_index = version_list.index(version_viewing),
            page_viewing = Math.floor(version_index / version_per_page) + 1;

        var version_pagination_page = function(page_number) {
            version_list.filter(".glitter-active").removeClass("glitter-active");
            var start = (page_number - 1) * version_per_page,
                end = start + version_per_page;
            version_list.slice(start, end).addClass("glitter-active");
        };

        $("#glitter-version-pagination").pagination({
            items: version_list.length,
            itemsOnPage: version_per_page,
            currentPage: page_viewing,
            cssStyle: "",
            onPageClick: version_pagination_page,
            displayedPages: 3,
            onInit: function() {
                version_pagination_page(page_viewing);
            }
        });


        // Multiple sets of tabs
        $("#glitter-page-actions").tabs();
        $("#glitter-edit-menu").tabs();


        // Special case for top row styling
        $("#glitter-page-actions").on("tabs.activate", function() {
            $("#glitter-menu").addClass("glitter-active");
        });

        $("#glitter-page-actions").on("tabs.beforehidden", function() {
            $("#glitter-menu").removeClass("glitter-active");
        });


        // Show active panes needed on load
        var panes_on_load = function(id) {
            if (id === undefined) {
                return;
            }

            var elem = $(id);

            // Can't find element / different page => don't bother trying
            if (!elem.length) {
                $.removeCookie(cookie_name, cookie_options);
                return;
            }

            var state_off = elem.data("stateOff");

            // Recursively show top levels first
            if (state_off !== undefined) {
                panes_on_load(state_off);
            }

            $(id).click();
        };

        panes_on_load($.cookie(cookie_name));


        // Store the active tab in a cookie
        $(document).on("tabs.activate", function(event, tab) {
            $.cookie(cookie_name, tab.data("stateOn"), cookie_options);
        });

        $(document).on("tabs.beforehidden", function(event, tab) {
            var state = tab.data("stateOff");

            if (state === undefined) {
                $.removeCookie(cookie_name, cookie_options);
            } else {
                $.cookie(cookie_name, state, cookie_options);
            }
        });


        var add_block_click = function(block_type) {
            var column_name = $(this).parents(".glitter-column").data("columnName"),
                block_top = $(this).parents(".glitter-button-row").data("blockTop");

            $.ajax(add_block_url, {
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csrf_token,
                    column: column_name,
                    block_type: block_type,
                    top: block_top
                },
                dataType: "json",
                success: function(data) {
                    if (data.column === undefined) {
                        // If no column is returned, user probably tried to move a block too far
                        return;
                    }

                    GlitterEditor.update_column(data.column, data.content);
                }
            });
        };

        $(document).on("click", ".glitter-add-block", function() {
            var block_type = $(this).data("blockType");

            // Avoid span with the same class
            if (block_type === undefined) {
                return;
            }

            add_block_click.call(this, block_type);
        });

        $(document).on("change", ".glitter-add-block-select", function() {
            var block_type = $(this).val();

            add_block_click.call(this, block_type);
        });

        $(document).on("click", "#glitter-discard-version, .glitter-delete-block, .glitter-edit-block", function() {
            var iframe_url = $(this).data("popupUrl");
            $(document.body).addClass("glitter-lightbox-active").append('<div id="glitter-lightbox" class="glitter-lightbox"><iframe class="glitter-lightbox-iframe" src="' + iframe_url  + '" allowTransparency="true"></iframe></div>');
        });

        $(document).on("change", ".glitter-move-block-select", function() {
            var url = $(this).parents(".glitter-move-block").data("moveUrl"),
                direction = $(this).val();

            $.ajax(url, {
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csrf_token,
                    move: direction
                },
                dataType: "json",
                success: function(data) {
                    if (data.column === undefined) {
                        /* If no column is returned, user probably tried to move a block too far */
                        return;
                    }

                    GlitterEditor.update_column(data.column, data.content);
                }
            });
        });

        $(document).on("change", ".glitter-move-column-select", function() {
            var url = $(this).parents(".glitter-move-column").data("moveUrl"),
                column = $(this).val();

            $.ajax(url, {
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csrf_token,
                    move: column
                },
                dataType: "json",
                success: function(data) {
                    if (data.source_column === undefined) {
                        /* If no data is returned, something went wrong! */
                        return;
                    }

                    GlitterEditor.update_column(data.source_column, data.source_content);
                    GlitterEditor.update_column(data.dest_column, data.dest_content);
                }
            });
        });


        // Special case for edit off
        $("#glitter-version-edit-toggle-off").on("click", function() {
            // If templates pane is visible - it'll disappear
            if ($.cookie(cookie_name) === "#glitter-tab-template") {
                // So set the state to edit instead
                $.cookie(cookie_name, $("#glitter-tab-template").data("stateOff"), cookie_options);
            }
        });
    });
})(GlitterEditor);
