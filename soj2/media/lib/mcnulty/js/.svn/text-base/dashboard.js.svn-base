/*
    Vertex admin interactive dashboard.
*/


var DASHBOARD_URL = "./dashboard/";

var SITEMAP_URL = DASHBOARD_URL + "sitemap/";

var MOVE_UP_URL = DASHBOARD_URL + "move-up/";

var MOVE_DOWN_URL = DASHBOARD_URL + "move-down/";

var sitemap_enabled = true;


$(function() {
    $("ul#sitemap ul li").addClass("closed");
});


// Toggles the sitemap children on and off.
function toggleChildren(control) {
    $(control).parent().toggleClass("closed");
}


// Disables all movement controls in the sitemap.
function disableMoveControls() {
    sitemap_enabled = false;
}


// Enables all movement controls in the sitemap.
function enableMoveControls() {
    sitemap_enabled = true;
}


// Displays an error message in the sitemap.
function displayError() {
    $("ul#sitemap").remove();
    $("div#sitemap-module").append("<p>The sitemap service is currently unavailable.</p>");
}


// Moves a page up.
function moveUp(control, page_id) {
    if (!sitemap_enabled) {
        return;
    }
    var li = $(control).parent().parent();
    var previous = li.prev();
    if (previous.length > 0) {
        disableMoveControls();
        li.fadeOut(function() {
            $.ajax({
                url: MOVE_UP_URL,
                type: "POST",
                data: {page_id: page_id},
                error: displayError,
                success: function(data) {
                    previous.before(li);
                    li.fadeIn();
                    enableMoveControls();
                },
                cache: false
            });
        });
    }
}

// Moves a page down.
function moveDown(control, page_id) {
    if (!sitemap_enabled) {
        return;
    }
    var li = $(control).parent().parent();
    var next = li.next();
    if (next.length > 0) {
        disableMoveControls();
        li.fadeOut(function() {
            $.ajax({
                url: MOVE_DOWN_URL,
                type: "POST",
                data: {page_id: page_id},
                error: displayError,
                success: function(data) {
                    next.after(li);
                    li.fadeIn();
                    enableMoveControls();
                },
                cache: false
            });
        });
    }
}

