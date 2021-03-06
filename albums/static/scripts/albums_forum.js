$.fn.extend({
  insertAtCaret: function(myValue){
  var obj;
  if( typeof this[0].name !='undefined' ) obj = this[0];
  else obj = this;

  if ($.browser.msie) {
    obj.focus();
    sel = document.selection.createRange();
    sel.text = myValue;
    obj.focus();
    }
  else if ($.browser.mozilla || $.browser.webkit) {
    var startPos = obj.selectionStart;
    var endPos = obj.selectionEnd;
    var scrollTop = obj.scrollTop;
    obj.value = obj.value.substring(0, startPos)+myValue+obj.value.substring(endPos,obj.value.length);
    obj.focus();
    obj.selectionStart = startPos + myValue.length;
    obj.selectionEnd = startPos + myValue.length;
    obj.scrollTop = scrollTop;
  } else {
    obj.value += myValue;
    obj.focus();
   }
 }
})


var sidebar_html = "<div id=\"albums-sidebar\" class=\"opened initial\"></div>";
var restore_icon = '/static/images/icons/open.png';
var close_icon = '/static/images/icons/close.png';
var prev_width = 0;
var sidebar_button = ' <input id="hideSidebar" type="button" class="btnbbcode" accesskey="s" value="Fotobalk verbergen" onclick="toggleSidebar(true);toggleSidebar();" /><span style="color:red;font-weight:bold;font-size:1em;"><sup>nieuw!</sup></span>';

$(document).ready(function(){
    // sidebar loading etc.
    if ($('textarea[name="message"]').length){
        loadSidebar();
    }
});

function loadSidebar(){
    $('textarea[name="message"]').attr('id','id-textarea-post');
    $('#wrapfooter').after(sidebar_html);
    var sidebar = $("#albums-sidebar");
    $('input.btnbbcode:last').after(sidebar_button);
    
    $.get(
        '/albums/sidebar/',
        function(response){
            sidebar.html(response);
            toggleSidebar(); // hide sidebar after loading
            sidebar.removeClass('initial');
            sidebar.resizable({
                ghost: true,
                handles: "e",
                maxWidth: 800
            });
            
            $('label').remove();
            selected_album = $('#id_album').val();
            window_height = $('body').height();
            
            $('#id_album').change(function(){
                album_id = $(this).val();
                loadPhotos(album_id);
            });
            // trigger change
            $('#id_album').change();
            
            $('#autocomplete-album').css('color', '#888');
            $('#autocomplete-album').focus(function () {
                $(this).val('');
                $(this).css('color', 'auto');
                $(this).autocomplete({
                    source: "/albums/search_own_albums/",
                    autoFocus: true,
                    minLength: 2,
                    delay: 0,
                    select:  function(e, ui) {
                        loadPhotos(ui.item.album_id);
                    }
               });
           });
           $('#autocomplete-album').blur(function () {
               if ($(this).val() == ''){
                    $(this).css('color', '888');
                    $(this).val('Albums doorzoeken');
               }
           });
       }
    );
    
    // options...
    $.get(
       '/albums/sidebar_options/',
        function (json){
            if (json != ''){
                json = $.parseJSON(json);
                if (json["background_color"]){
                    bg_url = '/static/images/backgrounds/';
                    if (json["transparent"]){
                        bg_url += 'transparent_';
                    }
                    bg_url += json.background_color + '.png';
                    sidebar.css('background', 'url('+bg_url+')');
                }
                if (json["text_color"]){
                    sidebar.css('color', json["text_color"]);
                }
                if (!json["collapse"])
                {
                    if (json["width"]){
                        sidebar.width(json["width"]);
                    }
                    toggleSidebar();
                }
                if (json["hide"]){
                    toggleSidebar(true);
                }
            }
        }
    );
    
    $('a.photo').live('click', function(e){
        if(e.preventDefault) {
            e.preventDefault();
        } else {
            e.returnValue = false;
        }
        var BBCode = $(this).data('bbcode')+"\n";
        $('#id-textarea-post').insertAtCaret(BBCode);
        $(this).addClass('selected');
        return false;
    });
    
    $('button#insert-all').live('click', function(e){
        // trigger click events
        $('a.photo').click();
    });
}
function loadPhotos(album_id){
    $.get(
        '/albums/get_photos/'+album_id+'/',
        function (response){
            photos_list = $('#photos-list');
            photos_list.prev('div.helptext').remove();
            photos_list.replaceWith(response);
            //$("#albums-sidebar").tinyscrollbar();
            fixVerticalCenter();
        }
    );
}
function fixVerticalCenter(){
    var $a = $('a.album, a.photo');
    $.each($a, function(){
        var a_height = $(this).height();
        var img = $(this).children('img.thumb')[0];
        var img_height = $(img).attr('height');
        if (img_height > 0 && img_height != a_height){
            padding = (a_height - img_height) / 2;
            $(img).css('padding-top', padding);
            $(img).css('padding-bottom', padding);
        }
    });
}
function toggleSidebar(hide_completely){
    var sidebar = $('#albums-sidebar');
    if (hide_completely){
    	if (!sidebar.hasClass('hidden')){
			sidebar.addClass('hidden');
			sidebar.hide();
            $('#hideSidebar').val('Fotobalk tonen');
		} else {
		    sidebar.removeClass('hidden');
		    sidebar.show();
            $('#hideSidebar').val('Fotobalk verbergen');
		}
    }
    if (sidebar.hasClass('opened')){
        sidebar.removeClass('opened');
        sidebar.addClass('closed');
        prev_width = parseInt(sidebar.width(), 10);
        sidebar.width('10');
        $('#control_icon').attr('src', restore_icon);
    } else {
        sidebar.removeClass('closed');
        sidebar.addClass('opened');
        sidebar.width('300');
        if (prev_width != 0 && prev_width != 10){
            sidebar.width(prev_width);
        } else {
            sidebar.css('width', '240px');
        }
        $('#control_icon').attr('src', close_icon);
    }
    return false;
}
/*function insertAtCaret(areaId,text) {
    var txtarea = document.getElementById(areaId);
    var scrollPos = txtarea.scrollTop;
    var strPos = 0;
    var br = ((txtarea.selectionStart || txtarea.selectionStart == '0') ? 
        "ff" : (document.selection ? "ie" : false ) );
    if (br == "ie") { 
        txtarea.focus();
        var range = document.selection.createRange();
        range.moveStart ('character', -txtarea.value.length);
        strPos = range.text.length;
    }
    else if (br == "ff") strPos = txtarea.selectionStart;

    var front = (txtarea.value).substring(0,strPos);  
    var back = (txtarea.value).substring(strPos,txtarea.value.length); 
    txtarea.value=front+text+back;
    strPos = strPos + text.length;
    if (br == "ie") { 
        txtarea.focus();
        var range = document.selection.createRange();
        range.moveStart ('character', -txtarea.value.length);
        range.moveStart ('character', strPos);
        range.moveEnd ('character', 0);
        range.select();
    }
    else if (br == "ff") {
        txtarea.selectionStart = strPos;
        txtarea.selectionEnd = strPos;
        txtarea.focus();
    }
    txtarea.scrollTop = scrollPos;
}*/
