


openerp.nf_simple_move = function(instance){
	
    instance.web.account.reload = function(parent,action){
    	parent.inner_widget.views.tree_account_move_line_quickadd.controller.reload_content();
    	parent.do_action({"type":"ir.actions.act_window_close"});
    	if (! action.params.close){
    		 parent.inner_widget.views.tree_account_move_line_quickadd.controller.open_wizard();
    	}
    }
    instance.web.client_actions.add('simple_move.reload', 'instance.web.account.reload');
	
	instance.web.account.QuickAddListView = instance.web.account.QuickAddListView.extend({
		init: function(){
			this._super.apply(this, arguments);
		},
		start: function(){
            var tmp = this._super.apply(this, arguments);
			this.bind_simple_button();
            return tmp;
		},
	    open_wizard: function (move_line_record_id) {
	    	var self=this;
//	    	self.dataset.get_context.add({'current_journal':self.current_journal,'current_period':self.current_period})
	    	var newwindow=undefined;
	    	if (self.current_journal && self.current_period){
	    		newwindow=self.do_action({
		    		name: _("Simple move"),
	                type: 'ir.actions.act_window',
	                res_model: 'nf_simple_move.wiz.simple_move',
	//                res_id: self.get("value"),
	                views: [[false, 'form']],
	                target: 'new',
	                context: self.dataset.get_context().add({'move_line_record_id':move_line_record_id?move_line_record_id:false}),
	            }).then(function(){
		            //SET Tabindex attribute to -1 on unuseful links
		    		$('.oe_form table.wiz_simple_move .oe_form_uri, a.ui-dialog-titlebar-close, select.oe_debug_view').attr("tabindex","-1");
	            });
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
	    
	
	});
	
	instance.web.ListView.List.include(/** @lends instance.web.ListView.List# */{
        row_clicked: function (event) {
        	if (this.view.open_wizard){
	        	var record_id = $(event.currentTarget).data('id');
	        	this.view.open_wizard(record_id);
	        	return false;
        	}else{
        		return this._super.apply(this, arguments);
        	}
        },
/*        get_row_for: function (record) {
            var id;
            var $row = this.$current.children('[data-id=' + record.get('id') + ']');
            if ($row.length) {
                return $row;
            }
            return null;
        }
*/    });
	
	
	
}


