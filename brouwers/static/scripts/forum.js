var rotation = 0;
var chat_opened = false;
var chat_moved = false;
var forum_id_key = 'f';

$(document).ready(function(){
	$.get('/ou/so/');
	$('#add-build-report').hide();
	
	// dead topics
	$('a#close_message').click(function(){
		$('div#blanket').hide();
		$('div#dead_topic').hide();
		$('body').css('overflow-y','auto');
		return false;
	});
	
	// oranje briefjes syncen
	$.get('/forum_tools/get_sync_data/', function(response){
		$.each(response, function(key, value){
			var source = $('#'+key);
			var cls = source.attr('class');
			var title = source.attr('title');
			$.each(value, function(key, value){
				$('#'+value).attr('class', cls).attr('title', title);
			});
		});
	});
	
	// chat in een popup window
	$('#chat-window').dialog({
		autoOpen: false,
		draggable: true,
		height: $(window).height()*0.75,
		width: $(window).width()/2,
		modal: false,
		resizable: true,
		// fixed position css
		create: function(event){
			$(event.target).parent().css('position', 'fixed');
		},
		close: function(event, ui){
			$(this).html('');
			chat_opened=false;
		},
		open: function(event, ui){
			$(event.target).parent().css('top', 'auto');
			$(event.target).parent().css('left', 'auto');
			$(event.target).parent().css('bottom', '0');
			$(event.target).parent().css('right', '0');
			chat_opened=true;
			init_popup();
		},
		resizeStop: function(event, ui){
			// reset de positie
			$(event.target).parent().css('position', 'fixed');
			if(!chat_moved){
				$(event.target).parent().css('top', 'auto');
				$(event.target).parent().css('left', 'auto');
				$(event.target).parent().css('bottom', '0');
				$(event.target).parent().css('right', '0');
			}
		},
		dragStart: function(event, ui){
			// fixen van position
			$(event.target).parent().css('position', 'fixed');
			$(event.target).parent().css('top', 'auto');
			$(event.target).parent().css('left', 'auto');
			$(event.target).parent().css('bottom', 'auto');
			$(event.target).parent().css('right', 'auto');
			chat_moved = true;
		}
	});
	
	$('#open-chat').click(function(e){
		e.preventDefault();
		if (!chat_opened){
			$.get('/forum_tools/get_chat/', function(json){
				$('#chat-window').html(json.html);
				// title zetten met extra gegevens
				title = json.title;
				title += "&nbsp;&bull; <a href=\""+$('#open-chat').attr('href')+"\" target=\"_blank\">FAQ</a>";
				applyHtmlToDialog($('#chat-window').dialog(), title);
				//$('#chat-window').dialog("option", "title", title);
				$('#chat-window').dialog('open');
			});
		}
		else{
			$('#chat-window').toggle();
		}
		return false;
	});
	
	// als de chat geopend is, zal die popup weg zijn als je op een link klikt
	// forceer dus het openen vna links in een nieuw venster/tab
	$('body').on('click', '#boardcontent a', function(){
		if(chat_opened){
			// get the content through an ajax call and replace the original content
			var url = $(this).attr('href');
			$.get(url, function(response){
				c = $(response);
				$('#boardcontent').html(c.find('#boardcontent').html());
				
				var title = c.find('#page-title').text();
				document.title = title;
				$(document).scrollTop(0);
				
				if(history.pushState){
					history.pushState({"id": history.length+1}, title, "url");
				}
			});
			return false;
		}
	});
	$('a').not('#boardcontent a').click(function(){
		if(chat_opened){
			html = '<p>De chat staat nog open. Indien je de pagina niet in een niew tabblad/venster opent, zal je chatsessie niet meer actief zijn.</p>';
			html += '<br /><p>Je kan de pagina in een nieuw venster of tabblad openen, of de chat sluiten en de pagina in dit venster openen.</p>';
			$('#popup').data('href', $(this).attr('href'));
			$('#popup').html(html);
			$('#popup').dialog('open');
			return false;
		}
	});
	/*$('body').on('click', ':not(#boardcontent) a', function(){
		if(chat_opened){
			window.open($(this).attr('href'));
			return false;
		}
	});*/
	$('body').on('click', '.ui-dialog-titlebar', function(){
		$(this).siblings('#chat-window').toggle();
	});
	// einde chat javascript


	// new-topic, new-reply buttons hiding
	// parse the current page URL for the forum_id
	var forum = $.url().param(forum_id_key);
	if (forum != undefined){
		$.get(
			'/forum_tools/get_post_perm/',
			{'forum': forum},
			function(json){
				restrictions = json.restrictions;
				if ($.inArray('T', restrictions) > -1){
					$('a.new-topic').remove();
				}
				if ($.inArray('T', restrictions) > -1){
					$('a.new-reply').remove();
				}
			}
		);
	}

	// retrieve sharing settings
	var user_ids = [];
	$('span.sharing').each(function(i, e){
		user_id = $(e).data('posterid');
		user_ids.push(user_id);
	});
	var ids = user_ids.join(",");
	if (ids){
		$.get(
			'/forum_tools/mods/get_sharing_perms/',
			{'poster_ids': ids},
			function(json_response){
				$.each(json_response, function(poster_id, html){
					$('span#sharing_' + poster_id).html(html);
				});
			});
	}

	// if we're on a viewtopic page, check if the 'Add build report' button may be shown
	var url = $.url();
	if(url.segment(-1) == 'viewtopic.php'){
		var forum_id = parseInt(url.param('f'), 10);
		$.getJSON('/forum_tools/get_build_report_forums/', function(json){
			if(json.forum_ids.indexOf(forum_id) > -1){ // good to go!
				$('#add-build-report button').text(json.text);
				$('#add-build-report').show();
			} else {
				$('#add-build-report button').remove();
			}
		});
	}
});


function applyHtmlToDialog(dialog, htmlTitle) {
	dialog.data("uiDialog")._title = function (title) { 
	title.html(this.options.title); };
	dialog.dialog('option', 'title', htmlTitle);
}

function rotate(){
	if (rotation < 180){
		rotation += 1;
		rotateScreen(rotation);
	}
}

function rotateScreen(degrees){
	$('body').css('-webkit-transform', 'rotate('+degrees+'deg)');
	$('body').css('-moz-transform', 'rotate('+degrees+'deg)');
	$('body').css('-ms-transform', 'rotate('+degrees+'deg)');
	$('body').css('-o-transform', 'rotate('+degrees+'deg)');
	$('body').css('transform', 'rotate('+degrees+'deg)');
}

// dead topics
function test_url(topic_id, a){
	$.get('./ajax/topic_dead.php', {t: topic_id}, function(data){
		if (data == ""){
			var url = "" + a.attr('href');
			window.location=url;
		} else {
			$('body').css('overflow-y','hidden');
			$('div#blanket').show();
			$('div#dead_topic').show();
			$('div#message_topic_dead').html(data);
		}
	});
}
function init_popup(){
	$('#popup').dialog({
		autoOpen: false,
		draggable: false,
		height: 'auto',
		width: '400px',
		modal: true,
		resizable: false,
		title: 'Opgepast!',
		buttons: {
			'Nieuw venster/tabblad': function(){
				window.open($(this).data('href'));
				$(this).dialog('close');
			},
			'Chat sluiten': function(){
				$(this).dialog('close');
				window.location = $(this).data('href');
			},
			'Annuleren': function(){
				$(this).dialog('close');
			}
		}
	});
}
