openerp.nf_simple_move = function(instance){
	instance.web.client_actions.add('simple_move.open','instance.nf_simple_move.action');
	instance.nf_simple_move.action = instance.web.Widget.extend({
		className: 'oe_simple_move',
		init: function(){
	//    	alert("Coolo1");
			this._super.apply(this, arguments);
            alert(this.$el.parent().find('.oe_simple_move'));
	    	return this._super();
		},
		start: function(){
//	    	alert("Coolo2");
            return this._super();
		},
		events:{
			'click .oe_simple_move button': 'open_wizard',
		},
	    open_wizard: function () {
	    	alert("Coolo3");
	    },
	
	})
}

/*openerp. = function (instance) {
    instance.web.client_actions.add('example.action', 'instance.web_example.Action');
    instance.web_example.Action = instance.web.Widget.extend({
        template: 'web_example.action',
        events: {
            'click .oe_web_example_start button': 'watch_start',
            'click .oe_web_example_stop button': 'watch_stop'
        },
        watch_start: function () {
            this.$el.addClass('oe_web_example_started')
                    .removeClass('oe_web_example_stopped');
        },
        watch_stop: function () {
            this.$el.removeClass('oe_web_example_started')
                    .addClass('oe_web_example_stopped');
        },
    });
};*/