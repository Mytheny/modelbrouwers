$(document).ready(function(){
    $('#popup').dialog({
		autoOpen: false,
		draggable: true,
		//dialogClass: "",
		height: 300,
		width: 400,
		modal: false,
		resizable: true,
		title: "Online gebruikers",
		buttons: {
		    Sluiten: function() {
		        $(this).dialog("close");
		    }
		}
    });
    
    $.get('/ou/ous/', function(response){
        if (response != '0'){
            $('#popup').html(response);
            $('#popup').dialog('open');
        }
    });
    
    $.get('/forum_tools/mods/get_data/', function(json){
        if (json.open_reports > 0){
            html = '&nbsp;<span id=\"open_reports\">('+json.text_reports+')</span>';
            $('#pageheader p.linkmcp a').after(html);
        }
    });
});
