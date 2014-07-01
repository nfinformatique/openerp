openerp.nf_simple_move = function(instance){
//	instance.web.client_actions.add('simple_move.open','instance.nf_simple_move.action');
//	instance.nf_simple_move.action = instance.web.account.QuickAddListView.extend({
	instance.web.account.QuickAddListView = instance.web.account.QuickAddListView.extend({
//		className: 'oe_simple_move',
		init: function(){
			this._super.apply(this, arguments);
//	    	return this._super();
		},
		start: function(){
            var tmp = this._super.apply(this, arguments);
			this.bind_simple_button();
            return tmp;
		},
	    open_wizard: function () {
	    	var self=this;
	    	if (self.current_journal && self.current_period){
		    	self.do_action({
	                type: 'ir.actions.act_window',
	                res_model: 'nf_simple_move.wiz.simple_move',
	//                res_id: self.get("value"),
	                views: [[false, 'form']],
	                target: 'new',
	                //context: self.build_context().eval(),
	                context: $.extend(self.dataset.context,{'current_journal':self.current_journal, 'current_period':self.current_period}),
	            });
		    	debugger;
	            return false;
	    	}
	    	return true;
	    },
	    
        bind_simple_button: function() {
            var self = this;
            var test=this.$el.parent().find('.oe_simple_move button');
            this.$el.parent().find('.oe_simple_move button').on('click', function (event) {
            	self.open_wizard();
            });
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