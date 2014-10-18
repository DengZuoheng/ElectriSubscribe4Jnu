$(function() {
	$("input:password").each(function() {
		$(this).caps(function(a) {
			if (jQuery.browser.safari) {
				return
			}
			if (a) {
				$.cursorMessage("注意：大写键开启了")
			} else {}
		})
	})
});
jQuery.fn.caps = function(a) {
	return this.keypress(function(f) {
		var b = f.which ? f.which: (f.keyCode ? f.keyCode: -1);
		var d = f.shiftKey ? f.shiftKey: (f.modifiers ? !!(f.modifiers & 4) : false);
		var g = ((b >= 65 && b <= 90) && !d) || ((b >= 97 && b <= 122) && d);
		a.call(this, g)
	})
};
if (jQuery) { (function(a) {
		a.cursorMessageData = {};
		a(window).ready(function(b) {
			if (a("#cursorMessageDiv").length == 0) {
				a("body").append('<div id="cursorMessageDiv">&nbsp;</div>');
				a("#cursorMessageDiv").hide()
			}
			a("body").mousemove(function(c) {
				a.cursorMessageData.mouseX = c.pageX;
				a.cursorMessageData.mouseY = c.pageY;
				if (a.cursorMessageData.options != undefined) {
					a._showCursorMessage()
				}
			})
		});
		a.extend({
			cursorMessage: function(c, b) {
				if (b == undefined) {
					b = {}
				}
				if (b.offsetX == undefined) {
					b.offsetX = 5
				}
				if (b.offsetY == undefined) {
					b.offsetY = 5
				}
				if (b.hideTimeout == undefined) {
					b.hideTimeout = 1000
				}
				a("#cursorMessageDiv").html(c).fadeIn("slow");
				if (jQuery.cursorMessageData.hideTimeoutId != undefined) {
					clearTimeout(jQuery.cursorMessageData.hideTimeoutId)
				}
				if (b.hideTimeout > 0) {
					jQuery.cursorMessageData.hideTimeoutId = setTimeout(a.hideCursorMessage, b.hideTimeout)
				}
				jQuery.cursorMessageData.options = b;
				a._showCursorMessage()
			},
			hideCursorMessage: function() {
				a("#cursorMessageDiv").fadeOut("slow")
			},
			_showCursorMessage: function() {
				a("#cursorMessageDiv").css({
					top: (a.cursorMessageData.mouseY + a.cursorMessageData.options.offsetY) + "px",
					left: (a.cursorMessageData.mouseX + a.cursorMessageData.options.offsetX)
				})
			}
		})
	})(jQuery)
};