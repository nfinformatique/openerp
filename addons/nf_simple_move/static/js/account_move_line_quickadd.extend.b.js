openerp.nf_simple_move = function(instance){
	instance.web.account.QuickAddListView = instance.web.account.QuickAddListView.extend({
		init: function(){
			this._super.apply(this, arguments);
		},
		start: function(){
            var tmp = this._super.apply(this, arguments);
			this.bind_simple_button();
            return tmp;
		},
	    open_wizard: function () {
	    	var self=this;
	    	self.dataset.context=$.extend(self.dataset.context,{'current_journal':self.current_journal,'current_period':self.current_period})
	    	var newwindow=undefined;
	    	if (self.current_journal && self.current_period){
	    		newwindow=self.do_action({
		    		name: _("Simple move"),
	                type: 'ir.actions.act_window',
	                res_model: 'nf_simple_move.wiz.simple_move',
	//                res_id: self.get("value"),
	                views: [[false, 'form']],
	                target: 'new',
	                context: self.dataset.get_context(),
	            });
	    		debugger;
	    		self.ViewManager.views.tree_account_move_line_quickadd.reload_content();
	            //SET Tabindex attribute to -1 on unuseful links
	    		$('.oe_form table.wiz_simple_move .oe_form_uri, a.ui-dialog-titlebar-close, select.oe_debug_view').attr("tabindex","-1");
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
