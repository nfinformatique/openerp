


openerp.nf_simple_move = function(instance){
	
	openerp.nf_simple_move.date_extend(instance);

    instance.web.account.reload = function(parent,action){
//    	debugger;
    	//parent.inner_widget.views.tree_account_move_line_simple.controller.reload_content();
    	
    	//UPDATE LIST 
    	var controller=parent.inner_widget.views.tree_account_move_line_simple.controller;
    	var record=undefined;
    	var id = undefined;
    	var index=0;
//    	debugger;
    	if (action.params && action.params['id_vals'] && action.params['id_vals']['deleted_line_ids']){
    		index=999;
    		for (var i=0;i<action.params['id_vals']['deleted_line_ids'].length; ++i){
    			id = action.params['id_vals']['deleted_line_ids'][i];
    			record = controller.records.get(id);
    			var tmpindex=controller.records.indexOf(record);
    			if (tmpindex>=0)
    				index=Math.min(index,tmpindex);
    			controller.records.remove(record);
    		}
    	}
    	if (index<0 || index==999) index=0;
    	
    	if (action.params && action.params['id_vals'] && action.params['id_vals']['created_line_ids']){
    		for (var i=0;i<action.params['id_vals']['created_line_ids'].length; ++i){
    			id = action.params['id_vals']['created_line_ids'][i];
    			record = controller.records.get(id);
                if (!record) {
                    // insert after the source record
                    record = controller.make_empty_record(id);
                    controller.records.add(record, {at: index});
                }
                controller.reload_record(record);
    		}
    		
    	}
    	if (action.params.close){
    	
    		parent.do_action({"type":"ir.actions.act_window_close"});
    	}else{
    		parent.dialog_widget.views.form.controller.load_defaults();
    		//parent.inner_widget.views.tree_account_move_line_simple.controller.open_wizard();
    	}
    }
    instance.web.client_actions.add('simple_move.reload', 'instance.web.account.reload');
	
    instance.web.views.add('tree_account_move_line_simple', 'instance.web.account.SimpleMoveListView');
    
    instance.web.account.SimpleMoveListView = instance.web.account.QuickAddListView.extend({
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
        	setTimeout(function(){
//            var test=this.$el.parent().parent().find('.oe_account_quickadd.ui-toolbar').prepend('<button type="button" class="oe_button oe_list_add oe_highlight">Create Simple Entries</button>');
//            var test=this.$el.parent().parent().parent().find('.oe_simple_move button, button.oe_list_add');//.find('.oe_simple_move button, button.oe_list_add');
        		self.$el.parent().parent().parent().find('.oe_simple_move button, button.oe_list_add').off().on('click', function (event) {
        			self.open_wizard();
        		});
        	},1000);
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


